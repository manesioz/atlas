from time import sleep
import sys

t = int(sys.argv[1])

sleep(t)
print(sys.argv[2])

try:
    x = sys.argv[3]
except IndexError:
    raise
