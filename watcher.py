import sys
import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import  FileSystemEventHandler
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s', 
    filename="logs/general.log",
    level=logging.INFO)

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        logging.info(f"Created - {event.src_path}")

    def on_deleted(self, event):
        logging.info(f"Deleted - {event.src_path}")

    def on_moved(self, event):
        logging.info(f"Moved - {event.src_path} to {event.dest_path}]")
        
    def on_modified(self, event):
        logging.info(f"Modified - {event.src_path}")
        
if __name__ == "__main__":
    with open("directories.json", "r") as f:
        directories = json.load(f)["directories"]
    
    observer = Observer()
    for directory in directories:
        observer.schedule(Handler(), path=directory, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()