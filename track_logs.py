"""Module to utilize time in code"""
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileWatcherBinding:

    def __init__(self, sampling_frequency) -> None:
        self.sampling_frequency = sampling_frequency
        self.observer = Observer()

    def watch_file(self, file_name, file_event_handler) -> None:
        
        class Helper(FileSystemEventHandler):
             pass
        pass

    def watch_dir(self, directory_name, dir_event_handler) -> None:
        pass


def file_event_handler(file_name) -> None:
        pass

def dir_event_handler(dir_name) -> None:
        pass


if __name__ == "main":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S %Z')
    
    SAMPLING_FREQUENCY = 5.0
