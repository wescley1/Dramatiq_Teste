"""Worker A: consumes tasks from default queue."""
from dramatiq import actor
import dramatiq
from dramatiq_project import tasks

# This script starts a worker listening for tasks. Run with:
# python worker_a.py

if __name__ == "__main__":
    import logging
    import os as _os

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    # Diagnostics to help understand why the worker might exit
    print("DEBUG: DRAMATIQ_BROKER_URL=", _os.environ.get("DRAMATIQ_BROKER_URL"))
    try:
        br = dramatiq.get_broker()
    except Exception as _e:  # pragma: no cover - diagnostic
        print("DEBUG: dramatiq.get_broker() raised:", _e)
        br = None
    print("DEBUG: broker=", br)

    # Use dramatiq's Worker with the correct signature for installed dramatiq.
    worker = dramatiq.Worker(dramatiq.get_broker(), queues=None)
    print(f"Starting worker A (pid={_os.getpid()})...")
    worker.start()
    try:
        worker.join()
    except KeyboardInterrupt:
        worker.stop()
