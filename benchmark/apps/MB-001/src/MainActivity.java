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
