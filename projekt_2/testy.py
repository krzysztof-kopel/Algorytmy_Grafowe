# testy.py

import sys
import threading
from copy import deepcopy
import time

TIMER = True
RERAISE = True
ALLOWED_TIME = 1

def print_err(*a):
    print(*a, file=sys.stderr)

# format testów
# TESTS = [ {"arg":arg0, "hint": hint0}, {"arg":arg1, "hint": hint1}, ... ]

def list2str(L):
    s = ""
    for x in L:
        s += str(x) + ", "
    s = s.strip()
    if len(s) > 0:
        s = s[:-1]
    return s

def limit(L, lim=120):
    x = str(L)
    if len(x) < lim:
        return x
    else:
        return x[:lim] + "[za dlugie]..."

class TimeOut(Exception):
    def __init__(self):
        pass

def timeout_handler():
    raise TimeOut()

class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

def run_with_timeout(func, args, timeout):
    result = [None]
    exception = [None]

    def wrapper():
        try:
            result[0] = func(*args)
        except Exception as e:
            exception[0] = e

    thread = StoppableThread(target=wrapper)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        thread.stop()
        raise TimeOut()
    if exception[0]:
        raise exception[0]
    return result[0]

def internal_runtests(printarg, printhint, printsol, check, TESTS, f):
    passed = 0
    total = len(TESTS)
    total_time = 0
    for i, d in enumerate(TESTS):
        print("-----------------")
        print("Test", i)
        arg = deepcopy(d["arg"])
        hint = deepcopy(d["hint"])
        printarg(*arg)
        printhint(hint)
        try:
            time_s = time.time()
            sol = run_with_timeout(f, arg, ALLOWED_TIME + 1) if TIMER else f(*arg)
            time_e = time.time()
            printsol(sol)
            res = check(*arg, hint, sol)
            if res:
                passed += 1
            print("Orientacyjny czas: %.2f sek." % float(time_e - time_s))
            total_time += float(time_e - time_s)
        except TimeOut:
            print("!!!!!!!! PRZEKROCZONY DOPUSZCZALNY CZAS")
        except KeyboardInterrupt:
            print("Obliczenia przerwane przez operatora")
        except Exception as e:
            print("WYJATEK:", e)
            if RERAISE:
                raise e

    print("-----------------")
    print("Liczba zaliczonych testów: %d/%d" % (passed, total))
    print("Orientacyjny łączny czas : %.2f sek." % total_time)

    print_err(sys.argv[0].replace("_", " ").replace(".py", ""), passed, total, "%.2f" % total_time)