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
