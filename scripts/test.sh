#! /bin/sh

./build.sh
pytest --doctest-modules --ignore examples
