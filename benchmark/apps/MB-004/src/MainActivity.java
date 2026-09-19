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
