"""Worker A: consumes tasks from default queue."""
from dramatiq import actor
import dramatiq
from dramatiq_project import tasks

# This script starts a worker listening for tasks. Run with:
# python worker_a.py

if __name__ == "__main__":
    # Use dramatiq's worker entrypoint programmatically
    worker = dramatiq.Worker(dramatiq.get_broker(), worker_name="worker-a")
    print("Starting worker A (default queues)...")
    worker.run()
