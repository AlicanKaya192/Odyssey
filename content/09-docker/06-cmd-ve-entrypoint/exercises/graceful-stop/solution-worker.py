import signal
import time

running = True


def stop(signum, frame):
    global running
    running = False


signal.signal(signal.SIGTERM, stop)

while running:
    time.sleep(0.2)

print("saved, bye", flush=True)
