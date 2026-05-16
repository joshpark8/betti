#!/usr/bin/env python3
# monitor.py
import threading
import time
import os

LOG_FILES = [f"/tmp/betti_{i}.log" for i in range(1, 6)]


def tail_file(path, index, counts, lock):
    while not os.path.exists(path):
        time.sleep(0.1)
    with open(path, "r") as f:
        f.seek(0, 2)  # seek to end
        while True:
            line = f.readline()
            if line:
                line = line.strip()
                if line.isdigit():
                    with lock:
                        counts[index] = int(line)
            else:
                time.sleep(0.05)


def main(stdscr):
    curses.curs_set(0)
    counts = [0] * len(LOG_FILES)
    lock = threading.Lock()

    for i, path in enumerate(LOG_FILES):
        t = threading.Thread(
            target=tail_file, args=(path, i, counts, lock), daemon=True
        )
        t.start()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"{'Process':<12} {'Count':>10}")
        stdscr.addstr(1, 0, "-" * 24)
        with lock:
            snapshot = counts[:]
        for i, count in enumerate(snapshot):
            stdscr.addstr(2 + i, 0, f"betti_{i+1}.m2  {count:>10,}")
        stdscr.addstr(2 + len(LOG_FILES) + 1, 0, "press q to quit")
        stdscr.refresh()
        stdscr.timeout(200)
        if stdscr.getch() == ord("q"):
            break


curses.wrapper(main)
