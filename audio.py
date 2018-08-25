import threading
import pyaudio
import wave
import time


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
KEEP_RECORDING = False


class Record_Thread(threading.Thread):
    def __init__(self, p):
        # init super
        threading.Thread.__init__(self)
        self.flag = True
        self.p = p

    def record(self):
        frames = []

        # open record stream
        stream = self.p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

        # writing loop
        while True:
            if self.flag == True:
                data = stream.read(CHUNK)
                frames.append(data)
                print('TRUE')
            else:
                print('FALSE')
                break

        # stop recording and save
        stream.stop_stream()
        stream.close()
        self.p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def run(self):
        print('doing stuff')
        self.record()


class Audio():
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None

    def start(self):
        self.rec_thread = Record_Thread(self.p)
        self.rec_thread.start()

    def stop(self):
        self.rec_thread.flag = False
        self.rec_thread.join()
