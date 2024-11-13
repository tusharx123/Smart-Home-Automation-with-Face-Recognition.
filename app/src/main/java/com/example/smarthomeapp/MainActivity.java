package com.example.smarthomeapp;

import android.Manifest;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.widget.Button;
import android.widget.Toast;
import android.util.Log;
import android.widget.TextView;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Set;
import java.util.UUID;

public class MainActivity extends AppCompatActivity {

    private static final int PERMISSION_REQUEST_CODE = 1;
    private static final String TAG = "MainActivity";
    private TextView recognizedTextView;
    private TextView confirmationTextView;

    private BluetoothAdapter bluetoothAdapter;
    private BluetoothSocket bluetoothSocket;
    private BluetoothDevice device;

    // ActivityResultLauncher for Bluetooth enabling
    private final ActivityResultLauncher<Intent> enableBluetoothLauncher = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            result -> {
                if (result.getResultCode() == RESULT_OK) {
                    initializeBluetooth();
                } else {
                    Toast.makeText(this, "Bluetooth must be enabled for this app to function.", Toast.LENGTH_SHORT).show();
                }
            }
    );

    // ActivityResultLauncher for voice recognition
    private final ActivityResultLauncher<Intent> voiceRecognitionLauncher = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            result -> {
                if (result.getResultCode() == RESULT_OK) {
                    Intent data = result.getData();
                    if (data != null) {
                        ArrayList<String> results = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                        if (results != null && !results.isEmpty()) {
                            String command = results.get(0);
                            recognizedTextView.setText(command);
                            sendCommandToArduino(command);
                        }
                    }
                }
            }
    );

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        confirmationTextView = findViewById(R.id.confirmationTextView);
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialize Bluetooth adapter
        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        recognizedTextView = findViewById(R.id.recognizedTextView);
        if (bluetoothAdapter == null) {
            Toast.makeText(this, "Bluetooth is not supported on this device", Toast.LENGTH_SHORT).show();
            return;
        }

        // Check and request permissions
        if (checkPermissions()) {
            initializeBluetooth();
        } else {
            requestPermissions();
        }

        // Set up the button to start voice recognition
        Button voiceCommandButton = findViewById(R.id.voiceCommandButton);
        voiceCommandButton.setOnClickListener(v -> startVoiceRecognition());
    }

    private boolean checkPermissions() {
        return ContextCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH) == PackageManager.PERMISSION_GRANTED &&
                ContextCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH_CONNECT) == PackageManager.PERMISSION_GRANTED &&
                ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED;
    }

    private void requestPermissions() {
        ActivityCompat.requestPermissions(this,
                new String[]{
                        Manifest.permission.BLUETOOTH,
                        Manifest.permission.BLUETOOTH_CONNECT,
                        Manifest.permission.RECORD_AUDIO
                }, PERMISSION_REQUEST_CODE);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_REQUEST_CODE) {
            boolean allPermissionsGranted = true;
            for (int result : grantResults) {
                if (result != PackageManager.PERMISSION_GRANTED) {
                    allPermissionsGranted = false;
                    break;
                }
            }
            if (allPermissionsGranted) {
                initializeBluetooth();
            } else {
                Toast.makeText(this, "Bluetooth and audio permissions are required for this app to function.", Toast.LENGTH_SHORT).show();
            }
        }
    }

    private void initializeBluetooth() {
        // Ensure Bluetooth is enabled
        if (!bluetoothAdapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            enableBluetoothLauncher.launch(enableBtIntent);  // Use ActivityResultLauncher
        } else {
            connectToDevice("HC-05"); // HC-05 Bluetooth module name
        }
    }

    private void startVoiceRecognition() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED) {
            Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
            intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Say the command");
            try {
                voiceRecognitionLauncher.launch(intent);
            } catch (ActivityNotFoundException e) {
                Toast.makeText(this, "Speech recognition not supported on this device.", Toast.LENGTH_SHORT).show();
            }
        } else {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.RECORD_AUDIO}, PERMISSION_REQUEST_CODE);
        }
    }

    private void connectToDevice(String deviceName) {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
            Toast.makeText(this, "Bluetooth connect permission is required to connect to the device.", Toast.LENGTH_SHORT).show();
            return; // Exit the method if permission is not granted
        }

        Set<BluetoothDevice> pairedDevices = bluetoothAdapter.getBondedDevices();
        for (BluetoothDevice pairedDevice : pairedDevices) {
            if (pairedDevice.getName().equals(deviceName)) {
                device = pairedDevice;
                UUID uuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"); // HC-05 SPP UUID
                try {
                    bluetoothSocket = device.createRfcommSocketToServiceRecord(uuid);
                    bluetoothSocket.connect();
                    listenForData();
                    Toast.makeText(this, "Connected to " + deviceName, Toast.LENGTH_SHORT).show();
                } catch (IOException e) {
                    Log.e(TAG, "Error connecting to device", e);
                    Toast.makeText(this, "Error connecting to device", Toast.LENGTH_SHORT).show();
                }
                break;
            }
        }
    }

    private void sendCommandToArduino(String command) {
        if (bluetoothSocket != null) {
            try {
                bluetoothSocket.getOutputStream().write(command.getBytes());
                Toast.makeText(this, "Command sent: " + command, Toast.LENGTH_SHORT).show();
            } catch (IOException e) {
                Log.e(TAG, "Error sending command", e);
                Toast.makeText(this, "Error sending command", Toast.LENGTH_SHORT).show();
            }
        }
    }

    private volatile boolean listening = true;
    private void listenForData() {
        new Thread(() -> {
            try {
                InputStream inputStream = bluetoothSocket.getInputStream();
                byte[] buffer = new byte[1024]; // buffer store for the stream
                int bytes; // bytes returned from read()

                // Read from the InputStream
                while (listening && bluetoothSocket != null) {
                    bytes = inputStream.read(buffer);
                    String receivedData = new String(buffer, 0, bytes);
                    Log.d(TAG, "Received data: " + receivedData);

                    // Update UI or handle received data
                    runOnUiThread(() -> {
                        recognizedTextView.setText(receivedData); // Display the recognized command
                        confirmationTextView.setText("Confirmation: " + receivedData); // Display confirmation
                    });
                }
            } catch (IOException e) {
                Log.e(TAG, "Error reading from Bluetooth", e);
            }
        }).start();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        listening = false;
        if (bluetoothSocket != null) {
            try {
                bluetoothSocket.close();
            } catch (IOException e) {
                Log.e(TAG, "Error closing Bluetooth socket", e);
            }
        }
    }
}
