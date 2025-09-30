"""Simple producer that enqueues a mix of quick and slow tasks."""
import time
from dramatiq_project import tasks


def produce_samples():
    print("Enqueuing tasks...")
    for i in range(5):
        tasks.quick_task.send(f"quick-{i}")
    for i in range(3):
        tasks.slow_task.send(f"slow-{i}", duration=3.0)
    print("Done enqueuing")


if __name__ == "__main__":
    produce_samples()
