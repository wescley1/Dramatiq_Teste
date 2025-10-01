import pika
import traceback

def main():
    try:
        creds = pika.PlainCredentials('guest', 'guest')
        params = pika.ConnectionParameters(host='dramatiq_teste-rabbitmq-1', port=5672, virtual_host='/', credentials=creds)
        conn = pika.BlockingConnection(params)
        print('OK from container')
        conn.close()
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    main()
