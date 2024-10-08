#!/usr/bin/env python3
import os
import sys
import csv
import glob
import time
from datetime import datetime

from manticore.wasm import ManticoreWASM

def progress(msg, i, t, prev=0):
    curr_int = round((i / t) * 100)
    prog_str = f'[{curr_int:3}%] {msg}'
    sys.stdout.write('\r')
    sys.stdout.write(' ' * prev)
    sys.stdout.write('\r')
    sys.stdout.write(prog_str)
    sys.stdout.flush()
    return 7 + len(msg)

def gen_2o1u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    h = state.new_symbolic_value(32, 'h')
    return [a, b, h]

def gen_2o2u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    h = state.new_symbolic_value(32, 'h')
    i = state.new_symbolic_value(32, 'i')
    return [a, b, h, i]

def gen_2o3u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    h = state.new_symbolic_value(32, 'h')
    i = state.new_symbolic_value(32, 'i')
    j = state.new_symbolic_value(32, 'j')
    return [a, b, h, i, j]

def gen_3o1u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    h = state.new_symbolic_value(32, 'h')
    return [a, b, c, h]

def gen_3o2u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    h = state.new_symbolic_value(32, 'h')
    i = state.new_symbolic_value(32, 'i')
    return [a, b, c, h, i]

def gen_3o3u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    h = state.new_symbolic_value(32, 'h')
    i = state.new_symbolic_value(32, 'i')
    j = state.new_symbolic_value(32, 'j')
    return [a, b, c, h, i, j]

def gen_4o1u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    d = state.new_symbolic_value(32, 'd')
    h = state.new_symbolic_value(32, 'h')
    return [a, b, c, d, h]

def gen_4o2u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    d = state.new_symbolic_value(32, 'd')
    h = state.new_symbolic_value(32, 'h')
    i = state.new_symbolic_value(32, 'i')
    return [a, b, c, d, h, i]

def gen_4o3u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    d = state.new_symbolic_value(32, 'd')
    h = state.new_symbolic_value(32, 'h')
    i = state.new_symbolic_value(32, 'i')
    j = state.new_symbolic_value(32, 'j')
    return [a, b, c, d, h, i, j]

def gen_5o1u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    d = state.new_symbolic_value(32, 'd')
    e = state.new_symbolic_value(32, 'e')
    h = state.new_symbolic_value(32, 'h')
    return [a, b, c, d, e, h]

def gen_5o2u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    d = state.new_symbolic_value(32, 'd')
    e = state.new_symbolic_value(32, 'e')
    h = state.new_symbolic_value(32, 'h')
    i = state.new_symbolic_value(32, 'i')
    return [a, b, c, d, e, h, i]

def gen_5o3u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    d = state.new_symbolic_value(32, 'd')
    e = state.new_symbolic_value(32, 'e')
    h = state.new_symbolic_value(32, 'h')
    i = state.new_symbolic_value(32, 'i')
    j = state.new_symbolic_value(32, 'j')
    return [a, b, c, d, e, h, i, j]

def gen_6o1u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    d = state.new_symbolic_value(32, 'd')
    e = state.new_symbolic_value(32, 'e')
    f = state.new_symbolic_value(32, 'f')
    h = state.new_symbolic_value(32, 'h')
    return [a, b, c, d, e, f, h]

def gen_6o2u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    d = state.new_symbolic_value(32, 'd')
    e = state.new_symbolic_value(32, 'e')
    f = state.new_symbolic_value(32, 'f')
    h = state.new_symbolic_value(32, 'h')
    i = state.new_symbolic_value(32, 'i')
    return [a, b, c, d, e, f, h, i]

def gen_6o3u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    d = state.new_symbolic_value(32, 'd')
    e = state.new_symbolic_value(32, 'e')
    f = state.new_symbolic_value(32, 'f')
    h = state.new_symbolic_value(32, 'h')
    i = state.new_symbolic_value(32, 'i')
    j = state.new_symbolic_value(32, 'j')
    return [a, b, c, d, e, f, h, i, j]

def gen_7o1u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    d = state.new_symbolic_value(32, 'd')
    e = state.new_symbolic_value(32, 'e')
    f = state.new_symbolic_value(32, 'f')
    g = state.new_symbolic_value(32, 'g')
    h = state.new_symbolic_value(32, 'h')
    return [a, b, c, d, e, f, g, h]

def gen_7o2u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    d = state.new_symbolic_value(32, 'd')
    e = state.new_symbolic_value(32, 'e')
    f = state.new_symbolic_value(32, 'f')
    g = state.new_symbolic_value(32, 'g')
    h = state.new_symbolic_value(32, 'h')
    i = state.new_symbolic_value(32, 'i')
    return [a, b, c, d, e, f, g, h, i]

def gen_7o3u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    d = state.new_symbolic_value(32, 'd')
    e = state.new_symbolic_value(32, 'e')
    f = state.new_symbolic_value(32, 'f')
    g = state.new_symbolic_value(32, 'g')
    h = state.new_symbolic_value(32, 'h')
    i = state.new_symbolic_value(32, 'i')
    j = state.new_symbolic_value(32, 'j')
    # ordered variables
    # state.constrain(a != b)
    # state.constrain(c != a)
    # state.constrain(c != b)
    # state.constrain(d != a)
    # state.constrain(d != b)
    # state.constrain(d != c)
    # state.constrain(e != a)
    # state.constrain(e != b)
    # state.constrain(e != c)
    # state.constrain(e != d)
    # state.constrain(f != a)
    # state.constrain(f != b)
    # state.constrain(f != c)
    # state.constrain(f != d)
    # state.constrain(f != e)
    # state.constrain(g != a)
    # state.constrain(g != b)
    # state.constrain(g != c)
    # state.constrain(g != d)
    # state.constrain(g != e)
    # state.constrain(g != f)
    # state.constrain(a > b)
    # state.constrain(b > c)
    # state.constrain(c > d)
    # state.constrain(d > e)
    # state.constrain(e > f)
    # state.constrain(f > g)
    # unordered variables
    # state.constrain(h != a)
    # state.constrain(h != b)
    # state.constrain(h != c)
    # state.constrain(h != d)
    # state.constrain(h != e)
    # state.constrain(h != f)
    # state.constrain(h != g)
    # state.constrain(i != a)
    # state.constrain(i != b)
    # state.constrain(i != c)
    # state.constrain(i != d)
    # state.constrain(i != e)
    # state.constrain(i != f)
    # state.constrain(i != g)
    # state.constrain(i != h)
    # state.constrain(j != a)
    # state.constrain(j != b)
    # state.constrain(j != c)
    # state.constrain(j != d)
    # state.constrain(j != e)
    # state.constrain(j != f)
    # state.constrain(j != g)
    # state.constrain(j != h)
    # state.constrain(j != i)
    return [a, b, c, d, e, f, g, h, i, j]

def gen_8o1u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    d = state.new_symbolic_value(32, 'd')
    e = state.new_symbolic_value(32, 'e')
    f = state.new_symbolic_value(32, 'f')
    g = state.new_symbolic_value(32, 'g')
    x = state.new_symbolic_value(32, 'x')
    h = state.new_symbolic_value(32, 'h')
    return [a, b, c, d, e, f, g, x, h]

def gen_8o2u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    d = state.new_symbolic_value(32, 'd')
    e = state.new_symbolic_value(32, 'e')
    f = state.new_symbolic_value(32, 'f')
    g = state.new_symbolic_value(32, 'g')
    x = state.new_symbolic_value(32, 'x')
    h = state.new_symbolic_value(32, 'h')
    i = state.new_symbolic_value(32, 'i')
    # ordered variables
    return [a, b, c, d, e, f, g, x, h, i]

def gen_9o1u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    d = state.new_symbolic_value(32, 'd')
    e = state.new_symbolic_value(32, 'e')
    f = state.new_symbolic_value(32, 'f')
    g = state.new_symbolic_value(32, 'g')
    x = state.new_symbolic_value(32, 'x')
    y = state.new_symbolic_value(32, 'y')
    h = state.new_symbolic_value(32, 'h')
    return [a, b, c, d, e, f, g, x, y, h]

def gen_9o2u(state):
    a = state.new_symbolic_value(32, 'a')
    b = state.new_symbolic_value(32, 'b')
    c = state.new_symbolic_value(32, 'c')
    d = state.new_symbolic_value(32, 'd')
    e = state.new_symbolic_value(32, 'e')
    f = state.new_symbolic_value(32, 'f')
    g = state.new_symbolic_value(32, 'g')
    x = state.new_symbolic_value(32, 'x')
    y = state.new_symbolic_value(32, 'y')
    h = state.new_symbolic_value(32, 'h')
    i = state.new_symbolic_value(32, 'i')
    return [a, b, c, d, e, f, g, x, y, h, i]

MAPPING = {
    'datasets/btree/native/2o1u.wasm' : gen_2o1u,
    'datasets/btree/native/2o2u.wasm' : gen_2o2u,
    'datasets/btree/native/2o3u.wasm' : gen_2o3u,
    'datasets/btree/native/3o1u.wasm' : gen_3o1u,
    'datasets/btree/native/3o2u.wasm' : gen_3o2u,
    'datasets/btree/native/3o3u.wasm' : gen_3o3u,
    'datasets/btree/native/4o1u.wasm' : gen_4o1u,
    'datasets/btree/native/4o2u.wasm' : gen_4o2u,
    'datasets/btree/native/4o3u.wasm' : gen_4o3u,
    'datasets/btree/native/5o1u.wasm' : gen_5o1u,
    'datasets/btree/native/5o2u.wasm' : gen_5o2u,
    'datasets/btree/native/5o3u.wasm' : gen_5o3u,
    'datasets/btree/native/6o1u.wasm' : gen_6o1u,
    'datasets/btree/native/6o2u.wasm' : gen_6o2u,
    'datasets/btree/native/6o3u.wasm' : gen_6o3u,
    'datasets/btree/native/7o1u.wasm' : gen_7o1u,
    'datasets/btree/native/7o2u.wasm' : gen_7o2u,
    'datasets/btree/native/7o3u.wasm' : gen_7o3u,
    'datasets/btree/native/8o1u.wasm' : gen_8o1u,
    'datasets/btree/native/8o2u.wasm' : gen_8o2u,
    'datasets/btree/native/9o1u.wasm' : gen_9o1u,
    'datasets/btree/native/9o2u.wasm' : gen_9o2u,
}

def main():
    def run(test, arg_gen, output):
        start = time.time()
        m = ManticoreWASM(test, workspace_url=output)
        m.main(arg_gen)
        m.finalize()
        return time.time() - start

    now = datetime.now().strftime("%Y%m%d_%Hh%Mm%Ss")
    output = f'results-mcore-{now}'
    if not os.path.exists(output):
        os.makedirs(output)

    csvtbl = os.path.join(output, 'results.csv')
    with open(csvtbl, 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(['test', 'time_elapsed', 'n-paths'])

    i, prev, total = 0, 0, len(list(MAPPING.items()))
    for test, gen in MAPPING.items():
        prev = progress(f'Running \'{test}\'...', i + 1, total,
                        prev=prev)
        output_dir = os.path.join(output, os.path.basename(test))
        runtime = run(test, gen, output_dir)

        test_suite = glob.glob(os.path.join(output_dir, 'test*.input'))
        with open(csvtbl, 'a') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow([
            os.path.basename(test),
            runtime,
            len(list(test_suite))
        ])

        i += 1
    print(f'\nAll Done!')

if __name__ == '__main__':
    main()
    sys.exit(0)
