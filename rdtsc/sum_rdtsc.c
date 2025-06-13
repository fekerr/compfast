#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include <unistd.h>
#include <sched.h>
#include <string.h>

// Inline assembly function to read the Time-Stamp Counter
static inline uint64_t rdtsc() {
    unsigned int lo, hi;
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t)hi << 32) | lo;
}

// Function to simulate some work
void exampleFunction(int iterations) {
    volatile int sum = 0;
    for (int i = 0; i < iterations; ++i) {
        sum += i;
    }
}

// Function to get the CPU clock speed
double get_cpu_frequency() {
    FILE* fp;
    char buffer[128];
    double freq = 0.0;

    fp = fopen("/proc/cpuinfo", "r");
    if (fp == NULL) {
        perror("fopen");
        return -1;
    }

    while (fgets(buffer, sizeof(buffer), fp)) {
        if (sscanf(buffer, "cpu MHz : %lf", &freq) == 1) {
            break;
        }
    }

    fclose(fp);
    return freq * 1e6; // Convert MHz to Hz
}

// Function to get the current CPU core
int get_cpu_core() {
#ifdef _GNU_SOURCE
    return sched_getcpu();
#else
    return -1; // Return -1 if sched_getcpu is not available
#endif
}

// Function to print CPU core information
void print_cpu_info() {
    FILE* fp;
    char buffer[256];

    fp = fopen("/proc/cpuinfo", "r");
    if (fp == NULL) {
        perror("fopen");
        return;
    }

    printf("CPU Information:\n");
    while (fgets(buffer, sizeof(buffer), fp)) {
        if (strstr(buffer, "processor") || strstr(buffer, "model name") ||
            strstr(buffer, "cpu cores") || strstr(buffer, "core id")) {
            printf("%s", buffer);
        }
    }

    fclose(fp);
}

int main() {
    uint64_t start, end;
    double cpu_frequency = get_cpu_frequency();

    if (cpu_frequency < 0) {
        fprintf(stderr, "Failed to get CPU frequency\n");
        return 1;
    }

    printf("CPU Frequency: %.2f GHz\n", cpu_frequency / 1e9);

    int core = get_cpu_core();
    if (core == -1) {
        printf("CPU core information not available.\n");
    } else {
        printf("Running on CPU core: %d\n", core);
    }

    print_cpu_info();

    int iterations = 1000000; // Initial number of iterations
    start = rdtsc();
    exampleFunction(iterations);
    end = rdtsc();

    double elapsed_seconds = (double)(end - start) / cpu_frequency;
    printf("Elapsed cycles: %" PRIu64 "\n", (end - start));
    printf("Elapsed time: %.6f seconds\n", elapsed_seconds);

    int iterations_for_1s = (int)(iterations / elapsed_seconds);
    printf("Estimated iterations for 1 second runtime: %d\n", iterations_for_1s);

    return 0;
}
