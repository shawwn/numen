import sys
import json
import os
from pprint import pprint as pp

def send(x, numen_input, numen_output):
  s = json.dumps({'evaluate': x});
  numen_input.write('{} {}'.format(len(s), s));
  numen_input.flush()
  line = numen_output.readline();
  res = json.loads(line[line.find('{'):])
  return res

if __name__ == "__main__":
  if not os.path.exists("stdin") or not os.path.exists("stdout"):
    sys.stderr.write("Server not running\n");
    sys.stderr.flush()
    sys.exit(1)
  numen_input = open("stdin", "w")
  numen_output = open("stdout", "r")
  while True:
    sys.stdout.write("> ")
    sys.stdout.flush()
    line = sys.stdin.readline()
    line = line.rstrip()
    pp(send(line, numen_input, numen_output))
