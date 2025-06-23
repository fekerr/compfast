# Performance Considerations & Profiling

This document outlines potential performance bottlenecks in the Solar System Orbital Model and suggests tools for profiling if optimization becomes necessary.

## Potential Performance Bottlenecks

1.  **Physics Calculations (N-Body Simulation):**
    *   **Area:** `simulation_engine.py` (`_calculate_all_forces_at_state`, RK4 loop).
    *   **Nature:** O(N^2) complexity for N bodies due to all-pairs gravitational force calculation. RK4 involves multiple such calculations per step.
    *   **Impact:** Becomes the primary bottleneck as the number of simulated bodies (N) increases significantly (e.g., >20-50).
    *   **Future Optimizations (if needed):**
        *   **NumPy:** Introduce NumPy for vector math and array operations. This is often a first good step for numerical Python code.
        *   **Algorithmic:** Barnes-Hut or Fast Multipole methods (for large N, significant change).
        *   **Parallelization/Offloading:** Multiprocessing, GPU (PyCUDA/PyOpenCL), or porting core logic to C++/Rust/Numba.

2.  **Rendering:**
    *   **Area:** `renderer.py` (`render_all_bodies_to_surface`).
    *   **Nature:** Drawing many bodies and especially their historical paths (`pygame.draw.lines` for many points).
    *   **Impact:** Can be significant if many bodies have long, visible orbital paths.
    *   **Future Optimizations:**
        *   Path simplification/downsampling for distant views or long paths.
        *   Level of Detail (LOD) for rendering distant/small objects and their paths.
        *   Optimizing Pygame drawing (e.g., dirty rects if applicable, though less so for full-screen motion).

3.  **Text & UI Updates:**
    *   **Area:** `text_display.py`, `help_overlay.py`, status updates in `main.py`.
    *   **Nature:** Frequent rendering of text.
    *   **Impact:** Generally minor, but can add up if very complex information is updated every frame in the text pane.
    *   **Future Optimizations:** Cache static text surfaces; update dynamic text less frequently if possible.

4.  **Python Overhead for Numerics:**
    *   **Area:** Vector math in `celestial_body.py` (currently Python lists/loops).
    *   **Impact:** Affects physics calculation speed.
    *   **Future Optimizations:** NumPy (see above), Numba.

## Profiling Tools

If performance issues arise, the following tools can help identify bottlenecks:

1.  **`cProfile` (Python built-in):**
    *   Provides detailed statistics on function calls and execution times.
    *   **Usage:** `python -m cProfile -o output.prof src/main.py [args]`
    *   The output file `output.prof` can then be analyzed.

2.  **`snakeviz`:**
    *   A browser-based visualizer for `cProfile` output, making it easier to interpret.
    *   **Installation:** `pip install snakeviz`
    *   **Usage:** `snakeviz output.prof`

3.  **`line_profiler`:**
    *   For line-by-line analysis of specific functions (requires decorating functions with `@profile`).
    *   **Installation:** `pip install line_profiler`
    *   **Usage:**
        1. Decorate functions of interest in your code with `@profile`.
        2. Run: `kernprof -l -v your_script.py` (e.g., `kernprof -l -v src/main.py`)

## Current Optimization Strategy

*   **No Premature Optimization:** The current focus is on functionality and correctness.
*   **Future Steps:** If performance becomes an issue for the desired number of bodies or features, profiling should be performed first to identify true bottlenecks. Introducing **NumPy** for vector/matrix operations in the physics engine would be a recommended initial step for optimization.
