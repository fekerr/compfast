Here is the `README.md` file wrapped to 80 columns for better readability:

### **README.md**

```markdown
# RDTSC Example for Measuring Elapsed Cycles

This project demonstrates how to use the `RDTSC` instruction to measure the
execution time of a function in terms of CPU cycles. It includes a C program
(`sum_rdtsc.c`) and a `Makefile` to compile and run the program.

## **Prerequisites**

Before building and running the program, you need to install the necessary
packages. Use the following command to install the required tools:

```bash
sudo apt-get install gcc make cpufrequtils
```

## **Files**

### **sum_rdtsc.c**

This C program reads the Time-Stamp Counter (TSC) using the `RDTSC`
instruction to measure the execution time of a function.

#### **Key Sections:**

- **`rdtsc` function**: Inline assembly to read the TSC.
- **`exampleFunction`**: A simple function to simulate work.
- **`get_cpu_frequency`**: Retrieves the CPU clock speed from `/proc/cpuinfo`.
- **`main` function**: Measures and prints the elapsed CPU cycles and time.

#### **Code:**
```c
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

// Inline assembly function to read the Time-Stamp Counter
static inline uint64_t rdtsc() {
    unsigned int lo, hi;
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t)hi << 32) | lo;
}

// Function to simulate some work
void exampleFunction() {
    volatile int sum = 0;
    for (int i = 0; i < 1000000; ++i) {
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

int main() {
    uint64_t start, end;
    double cpu_frequency = get_cpu_frequency();

    if (cpu_frequency < 0) {
        fprintf(stderr, "Failed to get CPU frequency\n");
        return 1;
    }

    printf("CPU Frequency: %.2f Hz\n", cpu_frequency);

    start = rdtsc();
    exampleFunction();
    end = rdtsc();

    double elapsed_seconds = (double)(end - start) / cpu_frequency;
    printf("Elapsed cycles: %" PRIu64 "\n", (end - start));
    printf("Elapsed time: %.6f seconds\n", elapsed_seconds);

    return 0;
}
```

### **Makefile**

The `Makefile` is used to compile the program, generate assembly listings in
both AT&T and Intel syntax styles, and run the program with the CPU governor
set to `performance`.

#### **Key Targets:**

- **`all`**: Compiles the program and generates assembly files.
- **`build_dir`**: Creates the `build` directory.
- **`$(TARGET)`**: Compiles the target executable.
- **`intel_asm`**: Generates Intel syntax assembly files.
- **`disassemble`**: Disassembles the object files.
- **`run`**: Saves the current CPU governor, sets it to `performance`, runs
  the program, and restores the original governor.
- **`clean`**: Removes the `build` directory and all generated files.

#### **Makefile:**
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

# Run the program with the performance governor
run: $(TARGET)
	set -x; \
	CURRENT_GOVERNOR=$$(cpufreq-info -p | awk '{print $$3}'); \
	sudo cpufreq-set -g performance; \
	./build/sum_rdtsc; \
	sudo cpufreq-set -g $${CURRENT_GOVERNOR}; \
	set +x;

# Clean up generated files
clean:
	rm -rf build
```

## **Usage**

1. **Ensure the `build` directory is clean**:
   ```bash
   make clean
   ```

2. **Build the project**:
   ```bash
   make
   ```

3. **Run the program with the `run` target**:
   ```bash
   make run
   ```

This `README.md` provides detailed instructions on setting up, building, and
running the project. If you encounter any issues or need further assistance,
feel free to reach out!

---
Is there anything else you'd like to configure or any other aspects of your
project you're working on? 😊🚀
```

This version ensures that all lines are wrapped at 80 columns for better readability. If you have any other requests or need further assistance, feel free to let me know! 😊🚀

---
Is there anything else you'd like to configure or any other aspects of your project you're working on? 😊🚀
