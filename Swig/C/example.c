#include "example.h"

long factorial(unsigned long n) {
    if (n == 0) {
        return 1;
    }
    
    long res = 1;
    for (unsigned long i=1; i<=n; i++) {
        res *= i;
    }

    return res;
}

double series(double x, unsigned int n){
    double res = 0;
    for (unsigned int i=0; i<n; i++) {
        res += pow(x, i) / factorial(i);
    }
    return res;
}
