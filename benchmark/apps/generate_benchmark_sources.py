import os

def write_src(subpath, content):
    p = os.path.join(os.path.dirname(__file__), subpath)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# MB-001: Plaintext HTTP
write_src("MB-001/src/MainActivity.java", """
package com.reg2app.benchmark.mb001;
import android.app.Activity;
import android.os.Bundle;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        try {
            URL url = new URL("http://insecure-api.example.com/data");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.connect();
        } catch (Exception e) {}
    }
}
""")

# MB-002: Strict TLS
write_src("MB-002/src/MainActivity.java", """
package com.reg2app.benchmark.mb002;
import android.app.Activity;
import android.os.Bundle;
import java.net.URL;
import javax.net.ssl.HttpsURLConnection;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        try {
            URL url = new URL("https://secure-api.example.com/data");
            HttpsURLConnection conn = (HttpsURLConnection) url.openConnection();
            conn.connect();
        } catch (Exception e) {}
    }
}
""")

# MB-004: Hardcoded Secret Key
write_src("MB-004/src/MainActivity.java", """
package com.reg2app.benchmark.mb004;
import javax.crypto.spec.SecretKeySpec;
import javax.crypto.Cipher;

public class MainActivity {
    private static final String STATIC_KEY = "MySuperSecretKey";
    public void encrypt(byte[] data) throws Exception {
        SecretKeySpec key = new SecretKeySpec(STATIC_KEY.getBytes(), "AES");
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        cipher.init(Cipher.ENCRYPT_MODE, key);
    }
}
""")

# MB-006: AndroidKeyStore
write_src("MB-006/src/MainActivity.java", """
package com.reg2app.benchmark.mb006;
import java.security.KeyStore;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import android.security.keystore.KeyGenParameterSpec;
import android.security.keystore.KeyProperties;

public class MainActivity {
    public SecretKey getKey() throws Exception {
        KeyStore ks = KeyStore.getInstance("AndroidKeyStore");
        ks.load(null);
        KeyGenerator kg = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore");
        kg.init(new KeyGenParameterSpec.Builder("MyKeyAlias", KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT)
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                .build());
        return kg.generateKey();
    }
}
""")

# MB-007: Weak DES Cipher
write_src("MB-007/src/MainActivity.java", """
package com.reg2app.benchmark.mb007;
import javax.crypto.Cipher;

public class MainActivity {
    public void runDes() throws Exception {
        Cipher c = Cipher.getInstance("DES/CBC/PKCS5Padding");
    }
}
""")

# MB-013: Plaintext SharedPreferences
write_src("MB-013/src/MainActivity.java", """
package com.reg2app.benchmark.mb013;
import android.content.Context;
import android.content.SharedPreferences;

public class MainActivity {
    public void savePassword(Context ctx, String password) {
        SharedPreferences sp = ctx.getSharedPreferences("user_prefs", Context.MODE_PRIVATE);
        sp.edit().putString("account_password", password).apply();
    }
}
""")

# MB-014: EncryptedSharedPreferences
write_src("MB-014/src/MainActivity.java", """
package com.reg2app.benchmark.mb014;
import android.content.Context;
import android.content.SharedPreferences;
import androidx.security.crypto.EncryptedSharedPreferences;
import androidx.security.crypto.MasterKey;

public class MainActivity {
    public void saveSecure(Context ctx, String token) throws Exception {
        MasterKey mk = new MasterKey.Builder(ctx).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build();
        SharedPreferences sp = EncryptedSharedPreferences.create(ctx, "secret_prefs", mk,
                EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
                EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM);
        sp.edit().putString("user_auth_token", token).apply();
    }
}
""")

# MB-022: PII to HTTP
write_src("MB-022/src/MainActivity.java", """
package com.reg2app.benchmark.mb022;
import android.telephony.TelephonyManager;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity {
    public void sendImei(TelephonyManager tm) throws Exception {
        String imei = tm.getDeviceId();
        URL u = new URL("http://tracking.example.com/collector?id=" + imei);
        HttpURLConnection c = (HttpURLConnection) u.openConnection();
        c.connect();
    }
}
""")

# MB-024: PII in Logcat
write_src("MB-024/src/MainActivity.java", """
package com.reg2app.benchmark.mb024;
import android.util.Log;

public class MainActivity {
    public void logSecret(String pin, String nid) {
        Log.d("AUTH_DEBUG", "User NID: " + nid + " PIN: " + pin);
    }
}
""")

# Generate stub templates for the remaining benchmarks
for i in range(1, 31):
    bid = f"MB-{i:03d}"
    d = os.path.join(os.path.dirname(__file__), bid)
    os.makedirs(d, exist_ok=True)
    readme = f"# Ground Truth Micro-Benchmark: {bid}\n\nSee catalog.json for targeted property and ground truth specification.\n"
    r_path = os.path.join(d, "README.md")
    if not os.path.exists(r_path):
        with open(r_path, "w", encoding="utf-8") as f:
            f.write(readme)

print("[OK] Generated benchmark source code catalog and micro-apps in benchmark/apps/")
