#define STR_MAX_SIZE 20

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

void print_row_or_column(char array[][STR_MAX_SIZE], int rows, int is_column)
{
    printf("[");
    for (int i = 0; i < rows; i++)
    {
        is_column ? printf("%s\n|", array[i]) : printf("%s\t|", array[i]);
    }
    if (!is_column)
        printf("\n");
    printf("]\n");
}

void print_table(char matrix[][STR_MAX_SIZE], int rows, int columns)
{
    printf("[[");
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < columns; j++)
        {
            printf("%s\t|", matrix[j + rows * i]);
        }
        printf("]\n");
    }
    printf("]\n");
}

const char *read_string()
{
    static char str[STR_MAX_SIZE];
    printf("Enter string:");
    scanf("%s", str);
    printf("%s", str);
    return str;
}

char **delete_el(char **arr, int index, int size)
{

    free(arr[index]);

    for (int i = index; i < size - 1; i++)
    {
        arr[i] = arr[i + 1];
    }

    arr[size - 1] = NULL;
    return arr;
}

char **insertElement(char **arr, int *size, int index, char *element)
{

    *size += 1;
    arr = realloc(arr, *size * sizeof(char *));

    for (int i = *size - 1; i > index; i--)
    {
        arr[i] = arr[i - 1];
    }

    arr[index] = malloc(strlen(element) + 1);
    strcpy(arr[index], element);
    return arr;
}

int findStringIndex(const char **arr, int size, char *target)
{
    for (int i = 0; i < size; i++)
    {
        if (strcmp(arr[i], target) == 0)
        {
            return i;
        }
    }

    return -1;
}
