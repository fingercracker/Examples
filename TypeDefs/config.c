#include "config.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int some_func(int x) {
    printf("The RTOS is %s\n", getenv("RTOS"));
    if (strcmp(getenv("RTOS"), "RTEMS") == 0) {
        return system_some_func(x);
    } else {
        return -1;
    }
}