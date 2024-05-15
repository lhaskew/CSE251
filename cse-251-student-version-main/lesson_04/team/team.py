"""
Course: CSE 251 
Lesson: L04 Team Activity
File:   team.py
Author: Lucy Haskew

Purpose: Practice concepts of Queues, Locks, and Semaphores.

Instructions:

- Review instructions in Canvas.

Question:

- Is the Python Queue thread safe? (https://en.wikipedia.org/wiki/Thread_safety)
"""

import threading
from queue import Queue
import requests
import json

# Include cse 251 common Python files
from cse251 import load_json_file

RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(data_queue, log):  
    """ Process values from the data_queue """

    while True:
        # Check to see if anything is in the queue
        if not data_queue.empty():
            # Process the value retrieved from the queue
            value = data_queue.get()
            
            # Make Internet call to get characters name and log it
            # Placeholder for Internet call and logging
            log.write(f"Retrieved value from queue: {value}")

        else:
            # If queue is empty, break the loop
            break

def file_reader(data_queue, log): 
    """ This thread reads the data file and places the values in the data_queue """

    # Open the data file "urls.txt" and place items into a queue
    with open("/Users/lucyhaskew/Desktop/CSE251/cse-251-student-version-main", "r") as file:
        for line in file:
            data_queue.put(line.strip())

    log.write('finished reading file')

    # Signal the retrieve threads one more time that there are "no more values"
    for _ in range(RETRIEVE_THREADS):
        data_queue.put(NO_MORE_VALUES)

def main():
    """ Main function """

    log = Log(show_terminal=True)

    data_queue = Queue(maxsize=0)

    file_reader_thread = threading.Thread(target=file_reader, args=(data_queue, log))
    retrieve_threads = [threading.Thread(target=retrieve_thread, args=(data_queue, log)) for _ in range(RETRIEVE_THREADS)]

    log.start_timer()

    for thread in retrieve_threads:
        thread.start()
    file_reader_thread.start()

    for thread in retrieve_threads:
        thread.join()
    file_reader_thread.join()

    log.stop_timer('Time to process all URLS')

if __name__ == '__main__':
    main()




