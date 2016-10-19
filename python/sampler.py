#!/usr/bin/env python3
import argparse
import csv
from concurrent.futures import ThreadPoolExecutor
import importlib
import logging
import sys
import time
import traceback


def sample(func, writer):
    start = time.time()
    try:
        func()
    except Exception as e:
        logging.error(repr(e))
        logging.error(''.join(traceback.format_tb(e.__traceback__)))
        writer.writerow((1, time.time() - start))
    else:
        writer.writerow((0, time.time() - start))


def sampler(num_samples, num_workers, func):
    writer = csv.writer(sys.stdout)
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for _ in range(num_samples):
            executor.submit(sample, func, writer)


def load_callable(module, method):
    module = importlib.import_module(module)
    return getattr(module, method)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('num_samples', type=int)
    parser.add_argument('num_workers', type=int)
    parser.add_argument('module')
    parser.add_argument('method', nargs='?', default='test')
    args = parser.parse_args()
    sampler(args.num_samples,
            args.num_workers,
            load_callable(args.module, args.method))


if __name__ == "__main__":
    main()
