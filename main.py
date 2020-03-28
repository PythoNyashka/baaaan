import multiprocessing
import time
import string

from decryptor import decrypt

printable = set(string.printable)

with open('encrypted', 'r') as file:
    data = file.read()

find = b'flag{'


class Brute(multiprocessing.Process):
    def __init__(self, start, stop, event):
        self.start_range = start
        self.stop_range = stop
        self.event = event
        super(Brute, self).__init__()

    def run(self) -> None:
        counter = 0
        for i in range(self.start_range, self.stop_range):
            if i % 1000000 == 0:
                if self.event.is_set():
                    break
            dec_data = decrypt(data, i)
            if set(dec_data) in printable:
                print(i, dec_data)
                self.event.set()
                break


def main():
    processes = []

    n_cpus = multiprocessing.cpu_count() - 1

    a = int(input('server: '))

    if a == 1:
        start = 0 
        stop = int(time.time()) // 4
    elif a == 2:
        start = int(time.time()) // 4
        stop = int(time.time()) // 2
    elif a == 3:
        start = int(time.time()) // 2
        stop = 3 * int(time.time()) // 4
    elif a == 4:
        start = 3*int(time.time()) // 4
        stop = int(time.time())


    step = (stop - start) // n_cpus

    stop_event = multiprocessing.Event()
    for i in range(n_cpus):
        proc = Brute(i * step+start, (i+1) * step+start, stop_event)
        print(proc.start_range, proc.stop_range, f'proc({i})')
        proc.start()

    for proc in processes:
        proc.join()


if __name__ == '__main__':
    main()

