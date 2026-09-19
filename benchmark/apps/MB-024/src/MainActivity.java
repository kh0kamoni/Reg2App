package com.reg2app.benchmark.mb024;
import android.util.Log;

public class MainActivity {
    public void logSecret(String pin, String nid) {
        Log.d("AUTH_DEBUG", "User NID: " + nid + " PIN: " + pin);
    }
}
