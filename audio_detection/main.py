import speech_recognition as sr
import os
from openai import OpenAI
from threading import Thread
from queue import Queue
import time

os.environ['https_proxy'] = 'localhost:1080'

class AudioDetectionRunner():
    def __init__(self, baseDir) -> None:
        self.baseDir = baseDir
        self.audio_queue = Queue()
        self.sentence = ""
        return
    
    def recognize_worker(self):
        # this runs in a background thread
        while True:
            audio = self.audio_queue.get()  # retrieve the next audio processing job from the main thread
            if audio is None: break  # stop processing if the main thread is done

            print("recognizing")
            data = audio.get_flac_data()
            f = open("output.flac", "wb")
            f.write(data)
            f.close()
            f = open("api_key", "r")
            api_key = f.readline()
            client = OpenAI(api_key=api_key)
            audio_file = open("output.flac", "rb")
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="text",
                language="zh",
            )
            print(transcription)
            self.sentence += transcription

            self.audio_queue.task_done()  # mark the audio processing job as completed in the queue

    def listen_worker(self):
        recognize_thread = Thread(target=self.recognize_worker)
        recognize_thread.daemon = True
        recognize_thread.start()
        r = sr.Recognizer()

        # with sr.Microphone() as source:
        for i in range(0, 10):  # repeatedly listen for phrases and put the resulting audio on the audio processing job queue
            print(i)
            with sr.Microphone() as source:
            # with sr.AudioFile('chinese.flac') as source:
                self.audio_queue.put(r.listen(source))
            time.sleep(3)
        self.audio_queue.join()  # block until all current audio processing jobs are done
        self.audio_queue.put(None)  # tell the recognize_thread to stop
        recognize_thread.join()  # wait for the recognize_thread to actually stop

    def start_regonize(self):
        self.listen_thread = Thread(target=self.listen_worker)
        self.listen_thread.daemon = True
        self.listen_thread.start()
    
    def get_sentence(self):
        result = self.sentence
        self.sentence = ""
        return result

if __name__ == "__main__":
    audioDetectionRunner = AudioDetectionRunner(".")
    audioDetectionRunner.start_regonize()
    try:
        # time.sleep(10)
        # print(audioDetectionRunner.get_sentence())
        audioDetectionRunner.listen_thread.join()
        print(audioDetectionRunner.get_sentence())
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        # audioDetectionRunner.listen_thread.()
        print(audioDetectionRunner.get_sentence())
