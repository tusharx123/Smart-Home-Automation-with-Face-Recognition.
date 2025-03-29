import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import sounddevice as sd
from scipy.io.wavfile import write
from creatingData import extract_mfcc
from sklearn.metrics import confusion_matrix
import time
import pyttsx3



engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 180)

def predictor():
    df = pd.read_csv("data\\csv\\complete_data.csv")  # target variable is boolean : 1 means sahil, 0 means unknown

    Y = df["speaker"]

    X = df.drop(columns=["speaker", "Unnamed: 0"])

    print(X.shape, "\n")

    # scaling pending

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.15, random_state=1)

    # MLPClassifier
    classifier = MLPClassifier(solver='adam', alpha=0.001,
                               random_state=1, max_iter=500,
                               hidden_layer_sizes=100, activation="logistic")
    classifier.fit(X_train, Y_train)
    pred_mlp = classifier.predict(X_test)
    cm_mlp = confusion_matrix(Y_test, pred_mlp)
    # print("Score of MLPClassifier: ",classifier.score(X_test, Y_test))
    print("cm of mlp: \n", cm_mlp)



def verifyUser():
    fs = 44100
    duration = 3

    engine.say("Speak gjai Jinendra when the recording starts!")
    print("speak Jai Jinendra when the recording starts")

    # wait = sd.rec(5, samplerate=fs, channels=1)
    # sd.wait()
    time.sleep(3)
    print("recording started")

    rec = sd.rec(int((duration * fs)), samplerate=fs, channels=1)

    sd.wait()

    print("recording stopped")

    file = "data\\history\\last_try.wav"
    write(filename=file, rate=fs, data=rec)

    mfcc = extract_mfcc(file, n_mfcc=40)

    input = pd.DataFrame(columns=range(0, 40))

    lst = list(mfcc)
    input.loc[len(input)] = lst

    df = pd.read_csv("data\\csv\\complete_data.csv")  # target variable is boolean : 1 means sahil, 0 means unknown

    Y = df["speaker"]
    X = df.drop(columns=["speaker", "Unnamed: 0"])

    # MLPClassifier
    classifier = MLPClassifier(solver='adam', alpha=0.001,
                               random_state=1, max_iter=500,
                               hidden_layer_sizes=100, activation="logistic")
    classifier.fit(X, Y)
    pred_mlp = classifier.predict(input)
    print("the MLP CLASSIFIER speaker is ", pred_mlp)









