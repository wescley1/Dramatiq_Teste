import inspect
import dramatiq

def main():
    print('dramatiq version', getattr(dramatiq, '__version__', 'unknown'))
    print('Worker signature:', inspect.signature(dramatiq.Worker.__init__))

if __name__ == '__main__':
    main()
