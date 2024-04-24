#include <stdio.h>
#include <stdlib.h>

int main() {
    // int working_set_size_kb = 16; // L1 Fitting (No larger than 16kB)
    int working_set_size_kb = 64; // L2 Fitting (No larger than 64kB)
    // int working_set_size_kb = 256; // DRAM Fitting (Larger than 128kB)
    int working_set_size_elements;
    int *data;
    int sum = 0;
    printf("Working set size: %dkB\n", working_set_size_kb);

    // Calculate the number of integers that can be stored in the given number of kilobytes
    // Assuming an integer is 4 bytes, calculate the number of integers that fit in the specified KB
    working_set_size_elements = (working_set_size_kb * 1024) / sizeof(int);

    // Allocate memory based on the calculated number of elements
    data = (int *)malloc(working_set_size_elements * sizeof(int));
    if (data == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    // Initialize the array with some values
    for (int i = 0; i < working_set_size_elements; i++) {
        data[i] = i;
    }

    // Sequentially access the array to simulate workload
    for (int i = 0; i < working_set_size_elements; i++) {
        sum += data[i];
    }

    printf("Sum of array elements: %d\n", sum);

    // Clean up and exit
    free(data);
    return 0;
}
