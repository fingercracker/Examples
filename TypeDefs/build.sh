#!/bin/bash

gcc system_file.c config.c -c
gcc system_file.o config.o example.c -o example.out
