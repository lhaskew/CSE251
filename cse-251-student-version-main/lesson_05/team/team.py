"""
Course: CSE 251 
Lesson: L05 Team Activity
File:   team.py
Author: <Lucy Haskew>

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools.
- Follow the graph from the `../canvas/teams.md` instructions.
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it.
"""

import time
import threading
import multiprocessing as mp
import random
from os.path import exists

from cse251 import *

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def create_data_txt(filename):
    """Create data file if it does not exist"""
    if not exists(filename):
        with open(filename, 'w') as f:
            for i in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + '\n')

def read_thread(filename, queue, prime_process_count):
    """Reading Thread: Reads numbers from the data file and places them onto a queue."""
    with open(filename, 'r') as f:
        for line in f:
            number = int(line.strip())
            queue.put(number)
    for number in range(prime_process_count):
        queue.put(None)

def prime_process(queue, primes, lock):
    """Prime Process: Processes numbers from the queue to check if they are prime and adds them to a shared list if they are."""
    while True:
        number = queue.get()
        if number is None:
            break
        if is_prime(number):
            with lock:
                primes.append(number)

def main():
    """Main function"""

    filename = 'data.txt'
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    prime_process_count = 4 # Start with one prime process

    queue = mp.Queue()
    manager = mp.Manager()
    primes = manager.list()
    lock = manager.Lock()

    # Create and start the reading thread
    reader_thread = threading.Thread(target=read_thread, args=(filename, queue, prime_process_count))
    reader_thread.start()

    # Create and start the prime checking processes
    processes = []
    for i in range(prime_process_count):
        process = mp.Process(target=prime_process, args=(queue, primes, lock))
        processes.append(process)
        process.start()

    # Wait for the reading thread to finish
    reader_thread.join()

    # Wait for all the processes to finish
    for process in processes:
        process.join()

    log.stop_timer(f'All primes have been found using {prime_process_count} process(es)')

    # Display the list of primes
    print(f'There are {len(primes)} primes found:')
    for prime in primes:
        print(prime)

if __name__ == '__main__':
    main()
