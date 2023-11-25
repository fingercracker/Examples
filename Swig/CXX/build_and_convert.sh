#!/bin/bash

g++ -fPIC -c Swig/CXX/example.cpp -o Swig/CXX/example.o
swig -c++ -python -o Swig/CXX/example_wrap.cxx Swig/CXX/example.i
g++ -fPIC -I/usr/include/python3.10 -c Swig/CXX/example_wrap.cxx -o Swig/CXX/example_wrap.o
g++ -Xlinker -export-dynamic -shared Swig/CXX/example.o Swig/CXX/example_wrap.o -o Swig/CXX/_example.so
