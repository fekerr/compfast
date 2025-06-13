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

# Compile to object files and retain intermediate assembly files for x86_64 (AT&T syntax)
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
