#define STR_MAX_SIZE 20
#define ARR_MAX_SIZE 20

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

void print_row_or_column(char ** array, double rows, double is_column)
{
    printf("[");
    for (int i = 0; i < rows; ++i)
    {
        is_column ? printf("%s|\n", array[i]) : printf("%s|", array[i]);
    }
    if (!is_column)
        printf("\n");
    printf("]\n");
}

char ** toDynamic2(double n, char strings[ARR_MAX_SIZE][STR_MAX_SIZE])
{
    char ** arr = malloc(n * sizeof(char*));
    for(int i = 0; i < n; ++i)
    {
        int size = strlen(strings[i]);
        arr[i] = malloc((size + 1) * sizeof(char));
        strcpy(arr[i], strings[i]);
    }
    return arr;
}

char * toDynamicStr(char string[STR_MAX_SIZE])
{
    char * arr = malloc(STR_MAX_SIZE * sizeof(char));
    strcpy(arr, string);
    return arr;
}

void print_table(char ** matrix, double rows, double columns)
{
    int rows_cast = (int) rows;
    int columns_cast = (int) columns;
    printf("[[");
    for (int i = 0; i < rows_cast; ++i)
    {
        for (int j = 0; j < columns_cast; ++j)
        {
            printf("%s\t|", matrix[j + i]);
        }
        printf("]\n");
    }
    printf("]\n");
}

char * read_string()
{
    char * str = malloc(STR_MAX_SIZE * sizeof(char));
    printf("Enter string:");
    fgets(str, STR_MAX_SIZE, stdin);
    return str;
}

char **delete_el(char **arr, double index, double size)
{
    int index_cast = (int) index;
    free(arr[index_cast]);

    for (int i = index_cast; i < size - 1; ++i)
    {
        arr[i] = arr[i + 1];
    }

    arr[index_cast - 1] = NULL;
    return arr;
}


char **reshape(char ** table, int nrows_before, int ncols_before, int nrows_after, int ncols_after)
{
    int prev_size = ncols_before * nrows_before;
    int new_size = ncols_after * nrows_after;
    char ** new_table = malloc(new_size * sizeof(char *));
    if (prev_size <= new_size)
    {
        for (int i = 0; i < prev_size; ++i)
        {
            strncpy(new_table[i], table[i], STR_MAX_SIZE);
        }
    }
    else
    {
        for (int i = 0; i < new_size; ++i)
        {
            strncpy(new_table[i], table[i], STR_MAX_SIZE);
        }
    }
    return new_table;
}

char **insert_element(char **arr, int *size, int index, char *element)
{

    *size += 1;
    arr = realloc(arr, *size * sizeof(char *));

    for (int i = *size - 1; i > index; --i)
    {
        arr[i] = arr[i - 1];
    }

    arr[index] = malloc(strlen(element) + 1);
    strcpy(arr[index], element);
    return arr;
}

int find_string_index(const char **arr, int size, char *target)
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

const char **mul_tables(const char **first_table, int n_rows_first, int n_columns_first, const char **second_table, int n_rows_second, int n_columns_second)
{
    if (n_rows_first != n_rows_second)
    {
        printf("Rows number in first table and rows numb in second table are not equal");
        exit(1);
    }
    int n_column_res = n_columns_first + n_columns_second;
    int n_row_res = n_rows_first;
    const char **res_table = malloc(n_column_res * n_row_res * STR_MAX_SIZE);
    for (int row_index = 0; row_index < n_row_res; ++row_index)
    {
        for (int col_index = 0; col_index < n_column_res; ++col_index)
        {
            res_table[row_index * n_column_res + col_index] = col_index < n_columns_first ? first_table[col_index] : second_table[col_index - n_columns_first];
        }
    }
    return res_table;
}
