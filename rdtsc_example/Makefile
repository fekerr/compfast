# Makefile for RDTSC example in Rust

# Build the project and generate assembly files
build:
	RUSTFLAGS="--emit asm -g" cargo build --release

# Generate objdump disassembly and map files with source lines
disassemble: build
	# Create the disassembly directory if it doesn't exist
	mkdir -p disassembly
	# Disassemble the binary
	llvm-objdump --source --disassemble target/release/rdtsc_example > disassembly/rdtsc_example_disassembly.txt
	# Create a map file
	nm target/release/rdtsc_example > disassembly/rdtsc_example_map.txt
	# Generate object dump for dependencies
	for file in target/release/deps/*.rlib; do llvm-objdump --source --disassemble $$file > disassembly/$$(basename $$file).disassembly.txt; done

# Run the project and redirect output to a file
run: disassemble
	cargo run --release | tee run_output.txt

# Clean up generated files
clean:
	cargo clean
	rm -rf disassembly

# Display help
help:
	@echo "Makefile for RDTSC example in Rust"
	@echo ""
	@echo "Available targets:"
	@echo "  build       - Build the project and generate assembly files"
	@echo "  disassemble - Generate objdump disassembly and map files with source lines"
	@echo "  run         - Run the project and redirect output to a file"
	@echo "  clean       - Clean up generated files"
	@echo "  help        - Display this help message"

