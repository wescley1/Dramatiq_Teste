"""Worker B: demonstrates a worker with different name/identity."""
import dramatiq
from dramatiq_project import tasks

if __name__ == "__main__":
    import logging
    import os as _os

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    print("DEBUG: DRAMATIQ_BROKER_URL=", _os.environ.get("DRAMATIQ_BROKER_URL"))
    try:
        br = dramatiq.get_broker()
    except Exception as _e:  # pragma: no cover - diagnostic
        print("DEBUG: dramatiq.get_broker() raised:", _e)
        br = None
    print("DEBUG: broker=", br)

    worker = dramatiq.Worker(dramatiq.get_broker(), queues=None)
    print(f"Starting worker B (pid={_os.getpid()})...")
    worker.start()
    try:
        worker.join()
    except KeyboardInterrupt:
        worker.stop()
