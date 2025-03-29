import sounddevice as sd
import librosa
import numpy as np
from scipy.io.wavfile import write
import pandas as pd
import os

# Set up constants for easier modification and reuse
FS = 44100  # Sample rate
DURATION = 4  # Duration of recording in seconds
OUTPUT_DIR = "D:\works\Voice-Biometrics-main\data"
COMPLETE_CSV = os.path.join(OUTPUT_DIR, "complete_data.csv")


# Record your voice 'n' times, where 'n' is the input by the user
def record_audio():
    print("How many recordings? ")
    n = int(input())

    for i in range(n):
        print(f"Recording {i + 1} of {n} started...")

        rec = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
        sd.wait()

        file_name = os.path.join(OUTPUT_DIR, f"Ayush_{i}.wav")
        write(filename=file_name, rate=FS, data=rec)

        print(f"Recording {i + 1} saved as {file_name}")
        if i < n - 1:  # Ask for more recordings if it's not the last one
            print("Record again? 1 for yes, 0 for no")
            choice = int(input())
            if choice == 0:
                break


# Used in model.py / Returns 40 MFCCs of a particular audio file
def extract_mfcc(file, n_mfcc=40):
    audio, sr = librosa.load(file, sr=None)  # Keep original sample rate
    mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc).T, axis=0)
    return mfccs


# Extract MFCCs for all recordings and create a CSV
def create_mfcc_csv():
    df = pd.DataFrame(columns=range(40))  # Predefine column names 0-39 for 40 MFCCs
    for i in range(21):  # Modify range if needed for more recordings
        file_name = os.path.join(OUTPUT_DIR, f"Ayush_{i}.wav")
        if os.path.exists(file_name):
            mfccs = extract_mfcc(file_name)
            df.loc[len(df)] = mfccs
        else:
            print(f"File not found: {file_name}")

    output_file = os.path.join(OUTPUT_DIR, "Ayush.csv")
    df.to_csv(output_file, index=False)
    print(f"MFCC data saved to {output_file}")


# Append individual CSV (e.g., Ayush.csv) to complete_data.csv
def append_individual_to_complete_csv():
    ayush_csv = os.path.join(OUTPUT_DIR, "Ayush.csv")
    if not os.path.exists(COMPLETE_CSV):
        print(f"{COMPLETE_CSV} not found, creating a new one...")
        pd.DataFrame(columns=range(40)).to_csv(COMPLETE_CSV, index=False)

    df_complete = pd.read_csv(COMPLETE_CSV)
    df_ayush = pd.read_csv(ayush_csv)

    df_combined = pd.concat([df_complete, df_ayush], ignore_index=True)
    df_combined.to_csv(COMPLETE_CSV, index=False)
    print(f"Data from {ayush_csv} appended to {COMPLETE_CSV}")

# Uncomment and call these functions as needed
record_audio()
create_mfcc_csv()
append_individual_to_complete_csv()
