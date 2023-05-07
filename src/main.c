#include<stdio.h>

extern double add(double, double);

int main() {
    double a = add(1.1, 2.1);
    printf("%f\n",a);
    return 0;
}