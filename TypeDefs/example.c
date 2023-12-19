#include "config.h"
#include <stdio.h>

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
    print_failure();
    print_success();
    do_something();
    return 1;
}