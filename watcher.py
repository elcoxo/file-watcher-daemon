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

def directory_import():
    try:
        with open("directories.json", "r") as f:
                directories = json.load(f)["directories"]
                if not directories:
                    logging.error(f"List are empty: ready for directories");
                else:
                    return directories
    except FileNotFoundError:
            logging.error(f"Drictories file not found");

class Watcher:
    def __init__(self):
        self.directories = directory_import()
        self.base_file ='directories.json'
        
        self.observer = Observer()
        
    def run(self):
        observer = Observer()
        observer.schedule(DirectoryHandler(), path=self.base_file, recursive=False)
        
        for directory in self.directories:
            observer.schedule(Handler(), path=directory, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        
    def update(self, new_dir):
        new_set_dir = set(new_dir)
        old_set_dir = set(self.directories)
        
        added = new_set_dir - old_set_dir
        removed = old_set_dir - new_set_dir
        
        self.observer.schedule(DirectoryHandler(), path=self.base_file, recursive=True)
            
        if added:
            logging.info(f"Directory list modified - Added: {added}")
        if removed:
            logging.info(f"Directory list modified - Removed: {removed}")
        
        self.directories = new_set_dir

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        logging.info(f"Created - {event.src_path}")

    def on_deleted(self, event):
        logging.info(f"Deleted - {event.src_path}")

    def on_moved(self, event):
        logging.info(f"Moved - {event.src_path} to {event.dest_path}]")
        
    def on_modified(self, event):
        logging.info(f"Modified - {event.src_path}")
        
class DirectoryHandler(FileSystemEventHandler, Watcher):
    def on_modified(self, event):
        new_dict = directory_import()
        self.update(new_dict)
        
if __name__ == "__main__":
    watcher = Watcher()
    watcher.run()