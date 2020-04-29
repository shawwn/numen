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

def numen_stringify(v):
  if v.get('error?'):
    r = "{}\n\n".format(v['vals'][0]['str'])
    for val in v['vals'][1:]:
      r += "  {}\n".format(numen_stringify(val))
    return r
  if 'null' in v:
    return v['null']
  if 'str' in v:
    return repr(v['str'])
  if 'sym' in v:
    return v['sym']
  if 'num' in v:
    return str(v['num'])
  if 'fn' in v:
    return '{}:{}:{} {}'.format(
        v.get('script', 'unknown'),
        v.get('line', 0),
        v.get('column', 0),
        v['fn'])
  if 'keys' in v:
    n = max([len(x) for x in v['keys']]) + 1
    return '\n'.join(
        ["{} {}".format(k.ljust(n), numen_stringify(v))
          for k, v in zip(v['keys'], v['vals'])])
  if 'vals' in v:
    r = "["
    c = ""
    for v in v['vals']:
      s = numen_stringify(v)
      r += c + s
      c = ", "
    r += "]"
    return r
  return "Unknown value"

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
    res = send(line, numen_input, numen_output)
    pp(res)
    if 'evaluation' in res:
      print(numen_stringify(res['evaluation']['value']))
