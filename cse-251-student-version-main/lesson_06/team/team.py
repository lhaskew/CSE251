"""
Course: CSE 251 
Lesson: L06 Team Activity
File:   team.py
Author: Lucy Haskew

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe
- Note, while getting your program to work, you can create a smaller text file instead of
  the ones given.  For example, create a text file with one line of text and get it to work
  with your program, then add another line of text and so on.
- After you can copy a text file word by word exactly, change the program (any way you want) to be
  faster (still using the processes).
"""

import multiprocessing as mp
from multiprocessing import Value, Process, Pipe
import filecmp
import os

# Include cse 251 common Python files
from cse251 import *

def sender(conn, filename, counter):
    """ function to send messages to other end of pipe """
    with open(filename, 'r') as file:
        for line in file:
            for char in line:
                conn.send(char)
                counter.value += 1
    conn.send('EOF')  # Sending EOF to indicate end of file
    conn.close()


def receiver(conn, filename, counter):
    """ function to print the messages received from other end of pipe """
    with open(filename, 'w') as file:
        while True:
            char = conn.recv()
            if char == 'EOF':
                break
            file.write(char)
            counter.value += 1
    conn.close()


def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow=False)


def copy_file(log, filename1, filename2):
    parent_conn, child_conn = Pipe()
    counter = Value('i', 0)

    # Creating processes
    sender_process = Process(target=sender, args=(parent_conn, filename1, counter))
    receiver_process = Process(target=receiver, args=(child_conn, filename2, counter))

    log.start_timer()
    start_time = log.get_time()

    # Starting processes
    sender_process.start()
    receiver_process.start()

    # Waiting for processes to finish
    sender_process.join()
    receiver_process.join()

    stop_time = log.get_time()
    elapsed_time = stop_time - start_time

    log.stop_timer(f'Total time to transfer content = {elapsed_time}')
    log.write(f'items / second = {counter.value / elapsed_time}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__":
    log = Log(show_terminal=True)

    copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')

    # After you get the gettysburg.txt file working, uncomment this statement
    copy_file(log, 'bom.txt', 'bom-copy.txt')
