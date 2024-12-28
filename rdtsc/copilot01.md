Here is the previous markdown file wrapped at 80 columns for better readability:

### **Summary of Our Work**

```markdown
# Summary of RDTSC Measurement and Makefile Configuration

This document provides a summary of the steps taken to measure the execution
time of a function in terms of CPU cycles using the `RDTSC` instruction, as
well as the configuration of a `Makefile` to compile and run the program.

## **Prerequisites**

Before building and running the program, ensure you have the necessary tools
installed by running:

```bash
sudo apt-get install gcc make cpufrequtils
```

## **Steps Taken**

1. **Created the C Program (`sum_rdtsc.c`)**:
    - Implemented the `rdtsc` function to read the Time-Stamp Counter (TSC).
    - Implemented the `exampleFunction` to simulate work.
    - Implemented the `get_cpu_frequency` function to retrieve CPU clock speed.
    - Implemented the `get_cpu_core` function to retrieve the current CPU core.
    - Implemented the `print_cpu_info` function to display CPU core information.
    - Implemented the `main` function to measure and display elapsed cycles, time,
      and estimate iterations for a 1-second runtime.

### **Code:**
```c
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
```

2. **Configured the `Makefile`**:
    - Included rules to compile the program, generate assembly listings, and run
      the program.
    - Configured the `Makefile` to work without changing the CPU governor, making
      it suitable for WSL2 or similar environments.

### **Makefile:**
```makefile
# Makefile for RDTSC example for x86_64 only

# Compiler and tools
CC = gcc
OBJDUMP = objdump

# Compiler flags
CFLAGS = -O3 -Wall -Wextra -Wpedantic -Wl,-Map,build/sum.map
ASMFLAGS = -S -g -fverbose-asm

# Target
TARGET = build/sum_rdtsc

# Source files
SRCS = sum_rdtsc.c

# Object files for x86_64
OBJS_x86_64 = build/x86_64/sum_rdtsc.o

# Assembly files for x86_64
ASMS_x86_64_att = build/x86_64/sum_rdtsc_att.s
ASMS_x86_64_intel = build/x86_64/sum_rdtsc_intel.s

# Rules
all: build_dir $(TARGET) disassemble intel_asm

# Create build directory if it doesn't exist
build_dir:
	mkdir -p build/x86_64

# Compile the target for x86_64
$(TARGET): $(OBJS_x86_64)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS_x86_64)

# Compile to object files and retain intermediate assembly files for x86_64
# (AT&T syntax)
build/x86_64/sum_rdtsc.o: sum_rdtsc.c
	$(CC) $(CFLAGS) -m64 -c $< -o $@
	$(CC) $(ASMFLAGS) -m64 $< -o $(ASMS_x86_64_att)

# Compile to assembly in Intel syntax for x86_64
build/x86_64/sum_rdtsc_intel.s: sum_rdtsc.c
	$(CC) $(ASMFLAGS) -masm=intel -m64 $< -o $@

# Generate Intel syntax assembly for x86_64
intel_asm: build/x86_64/sum_rdtsc_intel.s

# Disassemble object files for x86_64
disassemble: $(OBJS_x86_64)
	$(OBJDUMP) -d $(OBJS_x86_64) > build/x86_64/disassembly.txt

# Run the program (without changing CPU governor)
run: $(TARGET)
	set -x; \
	./build/sum_rdtsc; \
	set +x;

# Clean up generated files
clean:
	rm -rf build
```

3. **Built and Ran the Program**:
    - Cleaned the build directory using `make clean`.
    - Compiled the program using `make`.
    - Ran the program using `make run`.

## **Output**

The program printed the CPU frequency in GHz, the core it was running on, detailed
information about that core, the elapsed CPU cycles, the elapsed time in seconds,
and the estimated number of iterations required for a 1-second runtime.

If you encounter any issues or need further assistance, feel free to reach out!

```

This markdown file now has all lines wrapped at 80 columns for better readability. If you have any other requests or need further assistance, feel free to let me know! 😊🚀

Is there anything else you'd like to configure or any other aspects of your project you're working on? 😊🚀
