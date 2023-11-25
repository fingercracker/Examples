#!/bin/bash

gcc -fPIC -c Swig/C/example.c -o Swig/C/example.o
swig -python -o Swig/C/example_wrap.c Swig/C/example.i
gcc -fPIC -c Swig/C/example.c -o Swig/C/example.o
gcc -Xlinker -export-dynamic -shared Swig/C/example.o Swig/C/example_wrap.o -o Swig/C/_example.so
