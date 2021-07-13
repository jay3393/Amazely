import init
import time

if __name__ == '__main__':
    print("Program Started")
    while True:
        old_time = time.time()
        init.init()
        print(f"Time taken: {time.time()- old_time}")
        print("Running next generation")
        time.sleep(3)