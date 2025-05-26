# Design Notes and Future Considerations

This document holds notes regarding potential future development directions and more complex architectural considerations.

## Multi-language Workloads and Low-Level Optimizations

There is an interest in extending the workload concept beyond Python to include implementations in languages like C, C++, Rust, and even x86 assembly (potentially leveraging techniques similar to those in `ffmpeg`).

**Key Goals for such an extension would be:**
*   **Performance Comparison:** Directly compare Python performance against these lower-level languages for specific tasks.
*   **Exploiting Hardware:** Enable workloads that can better utilize multi-core CPUs and potentially GPU architectures through minimal branching code design and direct hardware control.
*   **Interoperability:** Investigate mechanisms for Python to call these compiled workloads (e.g., using `ctypes`, CFFI, or Python C extensions) and collect profiling data.

**Challenges and Considerations:**
*   **Build Systems:** Integrating compilers (GCC, Clang, Rustc, NASM/YASM) and managing build processes for multiple languages.
*   **Cross-Platform Compatibility:** Ensuring workloads compile and run across different operating systems.
*   **Profiling Complexity:** Standardizing how profiling data (time, memory, custom counters) is collected and reported from non-Python code.
*   **GPU Programming:** Would require specific libraries (CUDA, OpenCL) and a deeper integration strategy.

This represents a significant expansion of the project's scope and would require careful planning for each language and hardware target. The current "minimal branching" Python workloads are a conceptual first step towards designing algorithms that are more amenable to such parallelization.
