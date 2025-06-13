# Makefile

# Compiler and tools
CC = gcc
OBJDUMP = objdump

# Compiler flags
CFLAGS = -O3 -Wall -Wextra -Wpedantic -Wl,-Map,build/sum.map
ASMFLAGS = -S -g -fverbose-asm

# Target
TARGET = build/sum

# Source files
SRCS = sum.c

# Object files for different architectures
OBJS_x86 = build/x86/sum.o
OBJS_x86_64 = build/x86_64/sum.o

# Assembly files for different architectures and syntax styles
ASMS_x86_att = build/x86/sum_att.s
ASMS_x86_intel = build/x86/sum_intel.s
ASMS_x86_64_att = build/x86_64/sum_att.s
ASMS_x86_64_intel = build/x86_64/sum_intel.s

# Rules
all: build_dir $(TARGET) disassemble intel_asm

# Create build directory if it doesn't exist
build_dir:
	mkdir -p build/x86 build/x86_64

# Compile the target for x86 and x86-64
$(TARGET): $(OBJS_x86) $(OBJS_x86_64)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS_x86_64)

# Compile to object files and retain intermediate assembly files for x86 (AT&T syntax)
build/x86/sum.o: sum.c
	$(CC) $(CFLAGS) -m32 -c $< -o $@
	$(CC) $(ASMFLAGS) -m32 $< -o $(ASMS_x86_att)

# Compile to assembly in Intel syntax for x86
build/x86/sum_intel.s: sum.c
	$(CC) $(ASMFLAGS) -masm=intel -m32 $< -o $@

# Compile to object files and retain intermediate assembly files for x86-64 (AT&T syntax)
build/x86_64/sum.o: sum.c
	$(CC) $(CFLAGS) -m64 -c $< -o $@
	$(CC) $(ASMFLAGS) -m64 $< -o $(ASMS_x86_64_att)

# Compile to assembly in Intel syntax for x86-64
build/x86_64/sum_intel.s: sum.c
	$(CC) $(ASMFLAGS) -masm=intel -m64 $< -o $@

# Generate Intel syntax assembly for both x86 and x86-64
intel_asm: build/x86/sum_intel.s build/x86_64/sum_intel.s

# Disassemble object files for both architectures
disassemble: $(OBJS_x86) $(OBJS_x86_64)
	$(OBJDUMP) -d $(OBJS_x86) > build/x86/disassembly.txt
	$(OBJDUMP) -d $(OBJS_x86_64) > build/x86_64/disassembly.txt

# Clean up generated files
clean:
	rm -rf build
