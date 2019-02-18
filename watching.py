# coding: utf-8

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from google.cloud import vision
from google.cloud.vision import types
import os, time, io

target_dir = "./"

class ChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)

        if filename.find(".jpg") > -1:
            file_path = os.path.join(os.path.dirname(__file__), filename)
            detect_text(file_path)

    def on_modified(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        #print('%sを変更しました' % filename)

    def on_deleted(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        #print('%sを削除しました' % filename)

def detect_text(file_path):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    with io.open(file_path, 'rb') as image_file:
        content = image_file.read()

    try:
        image = types.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        description = texts[0].description.encode("utf-8")
        description = description.replace("\n", "").replace("≫", "").replace("「", "").replace("」", "").replace(".", "").replace("、", "").replace("。", "").replace("　", "").replace("？", "").replace("！", "").replace("♬", "").replace("〜", "").replace(" ", "").replace("＞", "").replace("＜", "").replace("…", "")
        print(description)
        with open("description.txt", "w") as f:
            f.write(description)

    except:
        pass

if __name__ in '__main__':
    while True:
        event_handler = ChangeHandler()
        observer = Observer()
        observer.schedule(event_handler, target_dir, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
