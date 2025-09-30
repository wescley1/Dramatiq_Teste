"""Worker B: demonstrates a worker with different name/identity."""
import dramatiq
from dramatiq_project import tasks

if __name__ == "__main__":
    worker = dramatiq.Worker(dramatiq.get_broker(), worker_name="worker-b")
    print("Starting worker B...")
    worker.run()
