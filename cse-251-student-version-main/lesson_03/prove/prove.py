"""
Course: CSE 251 
Lesson: L03 Prove
File:   prove.py
Author: <Lucy Haskew>

Purpose: Video Frame Processing

Instructions:

- Follow the instructions found in Canvas for this assignment.
- No other packages or modules are allowed to be used in this assignment.
  Do not change any of the from and import statements.
- Only process the given MP4 files for this assignment.
- Do not forget to complete any TODO comments.
"""

import os
from matplotlib.pylab import plt
from setup import setup as ensure_assignment_is_setup
from PIL import Image
import numpy as np
import timeit
import multiprocessing as mp
from cse251 import Log

CPU_COUNT = mp.cpu_count() + 4
FRAME_COUNT = 300

RED = 0
GREEN = 1
BLUE = 2

def create_new_frame(image_file, green_file, process_file):
    print(f'{process_file[-7:-4]}', end=',', flush=True)
    try:
        image_img = Image.open(image_file)
        green_img = Image.open(green_file)
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        return

    np_img = np.array(green_img)
    mask = (np_img[:, :, BLUE] < 120) & (np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)
    mask_img = Image.fromarray((mask*255).astype(np.uint8))
    image_new = Image.composite(image_img, green_img, mask_img)
    image_new.save(process_file)

def process_frames(cpu_count):
    start_time = timeit.default_timer()
    with mp.Pool(cpu_count) as pool:
        pool.starmap(
            create_new_frame,
            [(f'elephant/image{image_number:03d}.png', f'green/image{image_number:03d}.png', f'processed/image{image_number:03d}.png')
             for image_number in range(1, FRAME_COUNT + 1)]
        )
    return timeit.default_timer() - start_time

def main():
    all_process_time = timeit.default_timer()
    log = Log(show_terminal=True)

    xaxis_cpus = []
    yaxis_times = []

    for cpu in range(1, CPU_COUNT + 1):
        print(f'Processing with {cpu} CPU cores...')
        process_time = process_frames(cpu)
        xaxis_cpus.append(cpu)
        yaxis_times.append(process_time)
        log.write(f'Time for {FRAME_COUNT} frames using {cpu} processes: {process_time}')

    log.write(f'Total Time for ALL processing: {timeit.default_timer() - all_process_time}')

    plt.plot(xaxis_cpus, yaxis_times, label=f'{FRAME_COUNT}')
    plt.title('CPU Core yaxis_times VS CPUs')
    plt.xlabel('CPU Cores')
    plt.ylabel('Seconds')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(f'Plot for {FRAME_COUNT} frames.png')
    plt.show()

if __name__ == "__main__":
    ensure_assignment_is_setup()
    main()
