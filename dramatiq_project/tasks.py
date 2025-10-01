try:
    import dramatiq
except Exception:  # pragma: no cover - optional dependency in tests
    dramatiq = None

try:
    # Try first location
    from dramatiq.rabbitmq import RabbitmqBroker
except Exception:
    try:
        # Some older/newer versions expose under dramatiq.brokers.rabbitmq
        from dramatiq.brokers.rabbitmq import RabbitmqBroker
    except Exception:
        RabbitmqBroker = None

import os
import time

# Read broker URL from env for flexibility in dev/prod.
BROKER_URL = os.environ.get("DRAMATIQ_BROKER_URL", "amqp://guest:guest@localhost:5672//")

if dramatiq is not None and RabbitmqBroker is not None:
    broker = RabbitmqBroker(url=BROKER_URL)
    dramatiq.set_broker(broker)
else:
    # If dramatiq is present but RabbitmqBroker isn't, we still allow actors to
    # be created (they will error when trying to send if broker is not configured).
    broker = None


def do_quick(name: str) -> None:
    """Pure function that performs quick work. Tests can call this directly."""
    print(f"[do_quick] Start: {name}")
    time.sleep(0.5)
    print(f"[do_quick] Done: {name}")


def do_slow(name: str, duration: float = 2.0) -> None:
    """Pure function that performs slower work. Tests can call this directly."""
    print(f"[do_slow] Start: {name} (will take {duration}s)")
    time.sleep(duration)
    print(f"[do_slow] Done: {name}")


if dramatiq is not None:
    # Create actors that wrap the pure functions. If the broker was not
    # configured because RabbitmqBroker wasn't available, sending will fail at
    # runtime; that's intentional to surface configuration issues.
    quick_task = dramatiq.actor(do_quick)
    slow_task = dramatiq.actor(do_slow)
else:  # Provide placeholders so importing doesn't fail in minimal test env
    def _missing_actor(*args, **kwargs):
        raise RuntimeError("Dramatiq is not installed; install requirements to use actors")

    quick_task = _missing_actor
    slow_task = _missing_actor
