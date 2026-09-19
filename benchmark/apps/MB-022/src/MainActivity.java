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
