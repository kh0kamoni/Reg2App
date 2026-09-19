package com.reg2app.benchmark.mb013;
import android.content.Context;
import android.content.SharedPreferences;

public class MainActivity {
    public void savePassword(Context ctx, String password) {
        SharedPreferences sp = ctx.getSharedPreferences("user_prefs", Context.MODE_PRIVATE);
        sp.edit().putString("account_password", password).apply();
    }
}
