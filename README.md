# JULES CLI Framework

JULES (Just Understandable Little Execution System) is a lightweight Python CLI framework designed for modularity and ease of use. It allows users to define and run various workloads, with built-in support for profiling and other common utilities.

## Setup Instructions

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

2.  **Activate the virtual environment:**
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        venv\\Scripts\\activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage Examples

1.  **View CLI help:**
    ```bash
    python main.py --help
    ```

2.  **Run a workload:**
    To run the sample workload:
    ```bash
    python main.py run_workload sample_workload
    ```
    Replace `sample_workload` with the name of the workload you wish to run.

## Project Structure

-   `main.py`: The main entry point for the CLI application.
-   `modules/`: Contains reusable Python modules with core application logic.
    -   `example_module.py`: An example module demonstrating basic functionality.
-   `decorators/`: Houses custom decorators, such as for profiling.
    -   `profiling.py`: Contains performance profiling decorators (e.g., `time_it`).
-   `workloads/`: Stores scripts that define specific tasks or operations to be executed by the CLI.
    -   `sample_workload.py`: An example workload script.
-   `tests/`: Contains unit tests for the project (not yet implemented).
-   `jules/`: Intended for verbose logging output and other runtime-generated files (currently gitignored).
-   `requirements.txt`: Lists project dependencies.
-   `.gitignore`: Specifies intentionally untracked files that Git should ignore.

## Suggested Open Source Projects

Here are some open-source projects that could be beneficial for extending this framework:

### CLI Frameworks
*   **Click:** A popular Python package for creating beautiful command-line interfaces with as little code as necessary. It's highly configurable and comes with sensible defaults.
*   **Typer:** Built on top of Click, Typer is designed to be easy to use and provides type hints-based CLI argument parsing. It's a good choice if you like using Python type hints.
*   **Argparse:** (Already used in a basic way) Part of the Python standard library, it's robust for parsing command-line arguments. For more complex CLIs, Click or Typer might offer a more convenient API.

### Profiling Libraries
*   **cProfile and pstats:** Built-in Python modules for deterministic profiling. `cProfile` collects profiling data, and `pstats` helps analyze it. Good for understanding time spent in different functions.
*   **memory-profiler:** A Python module for monitoring memory consumption of a process as well as line-by-line memory consumption of functions.
*   **Pyinstrument:** A statistical profiler that records the call stack every millisecond. It has lower overhead than deterministic profilers like cProfile and can be easier to interpret for some use cases.
*   **Scalene:** A high-performance CPU and memory profiler for Python that does line-level profiling and can also identify issues related to multi-threading and GPU usage.

### Testing Frameworks
*   **pytest:** (Already included in `requirements.txt`) A mature, feature-rich testing framework that's easy to get started with and scales well for large projects.
*   **unittest:** Python's built-in unit testing framework (xUnit style). It's a solid choice, though pytest is often preferred for its conciseness and plugin ecosystem.

### Logging
*   **Loguru:** A library which aims to bring enjoyable logging in Python. It offers a simpler API for configuration and usage compared to the standard `logging` module for many common cases.

### Task Runners / Workflow Management
*   **Invoke:** A Python library for managing shell-oriented subprocesses and organizing executable Python code into CLI-invokable tasks.
*   **Poe the Poet:** A task runner that works well with Poetry projects, allowing you to define and run project tasks listed in your `pyproject.toml`.

This list is not exhaustive but provides a good starting point for exploring tools that can enhance the capabilities of this project.
