/*
float __attribute__((overloadable)) sum(float x, float y)
{
    return x + y;
}


int __attribute__((overloadable)) sum(int x, int y)
{
    return x + y;
}

void freeArray(char** array, int rows) {
    for (int i = 0; i < rows; i++) {
        free(array[i]);
    }
    free(array);
}
*/

#define STR_MAX_SIZE 20

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

void print_row_or_column(char array[][STR_MAX_SIZE], int rows, int is_column)
{
    for (int i = 0; i < rows; i++)
    {
        is_column ? printf("%s\n", array[i]) : printf("%s\t", array[i]);
    }
    if (!is_column)
        printf("\n");
}

void print_table(char matrix[][STR_MAX_SIZE], int rows, int columns)
{
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < columns; j++)
        {
            printf("%s\t", matrix[j + rows * i]);
        }
        printf("\n");
    }
}

double read_number()
{
    double numb;
    scanf("Enter your number:%lf", &numb);
    return numb;
}

const char *read_string()
{
    static char str[STR_MAX_SIZE];
    printf("Enter string:");
    scanf("%s", str);
    printf("%s", str);
    return str;
}
