#include "config.h"
#include <stdio.h>
#include <stdlib.h>

int print_success() {
    printf("SYSTEM_SUCCESS is %i\n", SUCCESSFUL);
}

int print_failure() {
    printf("SYSTEM_INTERNAL_ERROR is %i\n", INTERNAL_ERROR);
}

fsw_type do_something(){
    printf("this seems to work\n");
}

int main() {
    setenv("RTOS", "RTEMS", 1);
    print_failure();
    print_success();
    do_something();
    int y = some_func(1);
    printf("y is %i\n", y);
    return 1;
}
