import inspect
from dramatiq import message

def main():
    print('Message init signature:', inspect.signature(message.Message.__init__))
    print('Message doc:', message.Message.__doc__)

if __name__ == '__main__':
    main()
