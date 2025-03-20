Got it! Here's an updated `Makefile` where the map file is placed in the appropriate directories (`x86` or `x86_64`) based on the architecture:

```makefile
# Makefile

# Compiler and tools
CC = gcc
OBJDUMP = objdump

# Compiler flags
CFLAGS_X86 = -O3 -Wall -Wextra -Wpedantic -Wl,-Map,$(BUILD_X86)/sum.map
CFLAGS_X86_64 = -O3 -Wall -Wextra -Wpedantic -Wl,-Map,$(BUILD_X86_64)/sum.map
ASMFLAGS = -S -g -fverbose-asm

# Target directories
BUILD_DIR = build
BUILD_X86 = $(BUILD_DIR)/x86
BUILD_X86_64 = $(BUILD_DIR)/x86_64

# Targets
TARGET_X86 = $(BUILD_X86)/sum
TARGET_X86_64 = $(BUILD_X86_64)/sum

# Source file
SRCS = sum.c

# Object files and assembly files
OBJ_X86 = $(BUILD_X86)/sum.o
OBJ_X86_64 = $(BUILD_X86_64)/sum.o
ASM_X86_ATT = $(BUILD_X86)/sum_att.s
ASM_X86_INTEL = $(BUILD_X86)/sum_intel.s
ASM_X86_64_ATT = $(BUILD_X86_64)/sum_att.s
ASM_X86_64_INTEL = $(BUILD_X86_64)/sum_intel.s

# Dependency files
DEP_X86 = $(OBJ_X86:.o=.d)
DEP_X86_64 = $(OBJ_X86_64:.o=.d)

# Rules
.PHONY: all build_dirs clean
all: build_dirs $(TARGET_X86) $(TARGET_X86_64) disassemble intel_asm

# Create build directories
build_dirs:
	mkdir -p $(BUILD_X86) $(BUILD_X86_64)

# Compile x86 target
$(TARGET_X86): $(OBJ_X86)
	$(CC) $(CFLAGS_X86) -m32 -o $@ $<

# Compile x86-64 target
$(TARGET_X86_64): $(OBJ_X86_64)
	$(CC) $(CFLAGS_X86_64) -m64 -o $@ $<

# Compile x86 object and assembly files (AT&T syntax)
$(OBJ_X86): $(SRCS)
	$(CC) $(CFLAGS_X86) -MMD -m32 -c $< -o $@
	$(CC) $(ASMFLAGS) -m32 $< -o $(ASM_X86_ATT)

# Compile x86 assembly file (Intel syntax)
$(ASM_X86_INTEL): $(SRCS)
	$(CC) $(ASMFLAGS) -masm=intel -m32 $< -o $@

# Compile x86-64 object and assembly files (AT&T syntax)
$(OBJ_X86_64): $(SRCS)
	$(CC) $(CFLAGS_X86_64) -MMD -m64 -c $< -o $@
	$(CC) $(ASMFLAGS) -m64 $< -o $(ASM_X86_64_ATT)

# Compile x86-64 assembly file (Intel syntax)
$(ASM_X86_64_INTEL): $(SRCS)
	$(CC) $(ASMFLAGS) -masm=intel -m64 $< -o $@

# Generate Intel syntax assembly for x86 and x86-64
intel_asm: $(ASM_X86_INTEL) $(ASM_X86_64_INTEL)

# Disassemble object files for both architectures
disassemble: $(OBJ_X86) $(OBJ_X86_64)
	$(OBJDUMP) -d $(OBJ_X86) > $(BUILD_X86)/disassembly.txt
	$(OBJDUMP) -d $(OBJ_X86_64) > $(BUILD_X86_64)/disassembly.txt

# Clean up generated files
clean:
	rm -rf $(BUILD_DIR)

# Include dependencies
-include $(DEP_X86) $(DEP_X86_64)
```

### Key Updates:
1. **Architecture-Specific Map Files**:
   - Added `$(BUILD_X86)/sum.map` for x86 and `$(BUILD_X86_64)/sum.map` for x86-64 in their respective `CFLAGS`.

2. **Clear Separation**:
   - Ensured the map files are generated in the correct directory for each architecture.

Let me know if there’s anything else to refine!
