""" module to utilize time in code """
import time

""" module to log events """
import logging

""" module used to determine whether the event occurs with a file or directory """
import os

""" module used to observe given directory and notify the event handler about file system events """
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO,
                    format='[+] %(asctime)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S %Z')

class FileWatcherBinding:
    """ a class to show blueprint of the Log Watcher attributes and methods (functionalities) """

    def __init__(self, sampling_frequency) -> None:
        self.sampling_frequency = sampling_frequency
        self.observer = Observer()

    def watch_file_dir(self, event_handler) -> None:
        """ a function to start the observer on various file system events """

        class Helper(FileSystemEventHandler):
            """ a helper function to utilize FileSystemEventHandler functionalities """

            def on_created(self, event):
                val = info(event.src_path)
                key = 1
                event_handler(val[0], val[2], val[1], key)

            def on_deleted(self, event):
                val = info(event.src_path)
                key = 2
                event_handler(val[0], val[2], val[1], key)

            def on_modified(self, event):
                val = info(event.src_path)
                key = 3
                event_handler(val[0], val[2], val[1], key)

        handler = Helper()
        path = "."
        self.observer.schedule(handler, path, recursive = True)
        self.observer.start()

        try:
            while True:
                time.sleep(self.sampling_frequency)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


def file_dir_event_handler(file_type, file_name, src_dir, key) -> None:
        """ function to log file and directory events """        

        if key == 1:
            logging.info(f"{file_type} - {file_name} - created at - {src_dir}")

        elif key == 2:
            logging.info(f"{file_name} - deleted at - {src_dir}")

        elif key == 3:
            logging.info(f"{file_type} - {file_name} - modified at - {src_dir}")

        else:
            logging.error("Unknown behavior occured")

def info(s) -> () :
    """ function to extract info from event.src_path passed as string s as an argument """

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

    file_watcher.watch_file_dir(file_dir_event_handler)

    print("\nObserver stopped!")
