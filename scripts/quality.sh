#! /bin/sh

black .
mypy --strict --disallow-untyped-defs -p imgopt
