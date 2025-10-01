"""Simple producer that enqueues a mix of quick and slow tasks.

This script will wait for RabbitMQ to accept TCP connections before
attempting to enqueue messages. That avoids race conditions when the
broker is still starting inside Docker.
"""
import time
import os
from urllib.parse import urlparse

import pika
from dramatiq_project import tasks


def wait_for_broker(url: str, timeout: float = 30.0, interval: float = 1.0) -> None:
    """Block until a TCP connection to the broker host:port succeeds or timeout.

    The function parses an AMQP URL like amqp://user:pass@host:5672// and
    attempts to open a short-lived TCP connection using pika until it
    succeeds or the timeout is reached.
    """
    parsed = urlparse(url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 5672

    deadline = time.time() + timeout
    while True:
        try:
            # Use pika BlockingConnection with a short socket timeout to test reachability
            conn_params = pika.ConnectionParameters(host=host, port=port, socket_timeout=3)
            conn = pika.BlockingConnection(conn_params)
            conn.close()
            print(f"Broker reachable at {host}:{port}")
            return
        except Exception as exc:  # noqa: BLE001 - broad exception for retry loop
            now = time.time()
            if now >= deadline:
                raise RuntimeError(f"Timed out waiting for broker at {host}:{port}: {exc}") from exc
            print(f"Broker not ready at {host}:{port}: {exc}; retrying in {interval}s")
            time.sleep(interval)


def produce_samples():
    print("Enqueuing tasks...")
    for i in range(5):
        tasks.quick_task.send(f"quick-{i}")
    for i in range(3):
        tasks.slow_task.send(f"slow-{i}", duration=3.0)
    print("Done enqueuing")


if __name__ == "__main__":
    broker_url = os.environ.get("DRAMATIQ_BROKER_URL", "amqp://guest:guest@localhost:5672//")
    # Wait a short while for the broker to be ready when running under compose
    try:
        wait_for_broker(broker_url, timeout=30.0, interval=1.0)
    except RuntimeError as e:
        print(f"Warning: {e}; proceeding to enqueue may fail")
    produce_samples()
