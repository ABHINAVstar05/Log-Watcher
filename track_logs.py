"""Module to utilize time in code"""
import time
import logging
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S %Z')

class FileWatcherBinding:

    def __init__(self, sampling_frequency) -> None:
        self.sampling_frequency = sampling_frequency
        self.observer = Observer()

    def watch_file_dir(self, file_name, file_dir_event_handler) -> None:
        
        class Helper(FileSystemEventHandler):

            def on_created(self, event):
                val = info(event.src_path)
                key = 1
                file_dir_event_handler(val[0], val[2], val[1], key)

            def on_deleted(self, event):  
                val = info(event.src_path)
                key = 2
                file_dir_event_handler(val[0], val[2], val[1], key)

            def on_modified(self, event):
                val = info(event.src_path)
                key = 3
                file_dir_event_handler(val[0], val[2], val[1], key)

        event_handler = Helper()
        path = "."
        self.observer.schedule(event_handler, path, recursive = True)
        self.observer.start()

        try:
            while True:
                time.sleep(self.sampling_frequency)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


def file_dir_event_handler(file_type, file_name, src_dir, key) -> None:
        if key == 1:
            logging.info(f"'{file_type}' '{file_name}' is created at location '{src_dir}'")

        elif key == 2:
            logging.info(f"'{file_name}' is deleted at location '{src_dir}'")

        elif key == 3:
            logging.info(f"'{file_type}' '{file_name}' is modified at location '{src_dir}'")

        else:
            logging.error("Unknown behavior occured")

def info(s) -> () :
    file_type = None
    if os.path.isdir(s):
        file_type = 'Directory'
    elif os.path.isfile(s):
        file_type = 'File'

    val = (file_type, s.rsplit('\\', 1)[0], s.rsplit('\\', 1)[1])
    return val


if __name__ == "__main__":

    print("[+] Tracking logs...\n")
   
    SAMPLING_FREQUENCY = 5.0

    file_watcher = FileWatcherBinding(SAMPLING_FREQUENCY)

    FILE_NAME = "."

    file_watcher.watch_file_dir(FILE_NAME, file_dir_event_handler)

    print("\nObserver stopped!")
