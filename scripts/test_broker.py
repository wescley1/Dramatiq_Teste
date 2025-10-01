try:
    from dramatiq.brokers.rabbitmq import RabbitmqBroker
except Exception:
    try:
        from dramatiq.brokers.rabbitmq import RabbitmqBroker
    except Exception:
        RabbitmqBroker = None
from dramatiq.message import Message
import traceback

def main():
    try:
        if RabbitmqBroker is None:
            raise RuntimeError('RabbitmqBroker not available in installed dramatiq package')
        b = RabbitmqBroker(url='amqp://guest:guest@localhost:5672//')
        # Message signature: (queue_name, actor_name, args, kwargs, options, ...)
        msg = Message('default', 'test_actor', (), {}, {})
        b.enqueue(msg)
        print('enqueued')
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    main()
