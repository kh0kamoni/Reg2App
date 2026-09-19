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
