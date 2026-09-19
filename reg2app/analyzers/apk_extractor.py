import os
import sys
import zipfile
import hashlib
import tempfile
import re
from typing import Dict, Any, List, Optional
from loguru import logger
logger.disable("androguard")
from androguard.core.apk import APK

class APKExtractor:
    KNOWN_TRACKER_PACKAGES = {
        "com.facebook.ads": "Facebook Audience Network",
        "com.google.android.gms.ads": "Google AdMob",
        "com.appsflyer": "AppsFlyer Telemetry",
        "com.adjust.sdk": "Adjust Attribution",
        "com.flurry": "Yahoo Flurry",
        "io.branch": "Branch.io Deep Linking"
    }

    CIPHER_PATTERNS = [
        "DES/CBC/PKCS5Padding", "DES/ECB/PKCS5Padding", "DESede", "RC4", "AES/ECB/PKCS5Padding",
        "AES/ECB/NoPadding", "AES/GCM/NoPadding", "AES/CBC/PKCS5Padding", "Blowfish"
    ]

    HASH_PATTERNS = ["MD5", "SHA-1", "SHA1", "SHA-256", "SHA-512"]

    def __init__(self, apk_path: str):
        self.raw_path = os.path.abspath(apk_path)
        self.apk_path = self._resolve_apk_path(self.raw_path)
        self.apk_hash = self._compute_sha256(self.apk_path)
        self.andro_apk = APK(self.apk_path)
        self.package_name = self.andro_apk.get_package()

    def _compute_sha256(self, fpath: str) -> str:
        h = hashlib.sha256()
        with open(fpath, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()

    def _resolve_apk_path(self, path: str) -> str:
        if path.endswith(".apks") or path.endswith(".xapk"):
            with zipfile.ZipFile(path, "r") as z:
                candidates = [f for f in z.namelist() if f.endswith(".apk")]
                base_cand = [f for f in candidates if "base" in f.lower() or "standalone" in f.lower()]
                target = base_cand[0] if base_cand else (candidates[0] if candidates else None)
                if not target:
                    raise ValueError(f"No .apk found inside split bundle: {path}")
                
                temp_dir = tempfile.gettempdir()
                base_name = os.path.basename(path)
                out_path = os.path.join(temp_dir, f"ext_{base_name}_{target}")
                if not os.path.exists(out_path):
                    with open(out_path, "wb") as out_f:
                        out_f.write(z.read(target))
                return out_path
        return path

    def extract_manifest_context(self) -> Dict[str, Any]:
        xml = self.andro_apk.get_android_manifest_xml()
        app = xml.find("application") if xml is not None else None
        NS = "{http://schemas.android.com/apk/res/android}"

        app_tag = {}
        if app is not None:
            # usesCleartextTraffic
            uc = app.get(f"{NS}usesCleartextTraffic")
            app_tag["usesCleartextTraffic"] = (uc == "true" or uc is True) if uc is not None else None

            # allowBackup
            ab = app.get(f"{NS}allowBackup")
            app_tag["allowBackup"] = (ab == "true" or ab is True) if ab is not None else None

            # debuggable
            dbg = app.get(f"{NS}debuggable")
            app_tag["debuggable"] = (dbg == "true" or dbg is True) if dbg is not None else False

        # Permissions
        permissions = list(self.andro_apk.get_permissions())

        # Exported components
        exported_comps = []
        if xml is not None:
            for tag in ["activity", "service", "receiver", "provider"]:
                for el in xml.findall(f".//{tag}"):
                    exp = el.get(f"{NS}exported")
                    perm = el.get(f"{NS}permission")
                    name = el.get(f"{NS}name")
                    if exp == "true":
                        exported_comps.append({"type": tag, "name": name, "exported": True, "permission": perm})

        return {
            "application": app_tag,
            "permissions": permissions,
            "declared_category": "MFS",
            "exported_components": exported_comps
        }

    def extract_dex_context(self) -> Dict[str, Any]:
        ciphers_found = []
        hashes_found = []
        cleartext_urls = []
        trackers_present = set()
        has_keystore = False
        encrypted_prefs_used = False

        # Scan dex strings from the archive
        with zipfile.ZipFile(self.apk_path, "r") as z:
            for n in z.namelist():
                if n.endswith(".dex"):
                    b = z.read(n)
                    for m in re.finditer(rb'[ -~]{4,}', b):
                        s = m.group(0).decode("latin1", errors="ignore")

                        # Ciphers
                        for cp in self.CIPHER_PATTERNS:
                            if cp.lower() in s.lower():
                                ciphers_found.append({"transformation": cp, "class_name": n})

                        # Hashes
                        for hp in self.HASH_PATTERNS:
                            if s == hp:
                                hashes_found.append({"algorithm": hp, "class_name": n})

                        # Cleartext HTTP URLs
                        if s.startswith("http://") and not any(s.startswith(ign) for ign in [
                            "http://schemas.android.com", "http://www.w3.org", "http://ns.adobe.com",
                            "http://xmlpull.org", "http://apache.org", "http://plus.google.com"
                        ]):
                            if len(s) < 150:
                                cleartext_urls.append({"url": s, "class_name": n})

                        # AndroidKeyStore & EncryptedSharedPreferences
                        if "AndroidKeyStore" in s:
                            has_keystore = True
                        if "EncryptedSharedPreferences" in s or "MasterKey" in s:
                            encrypted_prefs_used = True

                        # Trackers
                        for tp in self.KNOWN_TRACKER_PACKAGES:
                            if tp in s:
                                trackers_present.add(tp)

        # De-duplicate
        unique_ciphers = [dict(t) for t in {tuple(d.items()) for d in ciphers_found}]
        unique_hashes = [dict(t) for t in {tuple(d.items()) for d in hashes_found}]
        unique_urls = [dict(t) for t in {tuple(d.items()) for d in cleartext_urls}]

        return {
            "dex": {
                "ciphers": unique_ciphers[:10],
                "hashes": unique_hashes[:10],
                "hardcoded_keys": [],
                "keystore_usage": has_keystore
            },
            "network": {
                "cleartext_http_urls": unique_urls[:10],
                "network_security_config": {"cleartextTrafficPermitted": False if len(unique_urls) == 0 else True}
            },
            "storage": {
                "shared_preferences_writes": [],
                "encrypted_shared_preferences_used": encrypted_prefs_used
            },
            "sdk": {
                "third_party_packages": list(trackers_present),
                "sdk_identifier_flows": []
            },
            "dataflow": {
                "pii_to_insecure_network": [],
                "pii_to_logcat": [],
                "safe_network_transmission": len(unique_urls) == 0,
                "clean_logging": True
            }
        }

    def build_full_context(self) -> Dict[str, Any]:
        manifest_ctx = self.extract_manifest_context()
        dex_ctx = self.extract_dex_context()
        return {
            "package_name": self.package_name,
            "apk_hash": self.apk_hash,
            "manifest": manifest_ctx,
            "dex": dex_ctx["dex"],
            "network": dex_ctx["network"],
            "storage": dex_ctx["storage"],
            "sdk": dex_ctx["sdk"],
            "dataflow": dex_ctx["dataflow"]
        }
