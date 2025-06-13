# JULES CLI Framework

JULES (Just Understandable Little Execution System) is a lightweight Python CLI framework designed for modularity and ease of use. It allows users to define and run various workloads, with built-in support for profiling and other common utilities.

## Table of Contents
- [Setup Instructions](#setup-instructions)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Configuration (`config.toml`)](#configuration-configtoml)
- [Application Logging](#application-logging)
- [Available Decorators](#available-decorators)
- [CI/CD Pipeline](#cicd-pipeline)
- [Pre-commit Hooks for Local Development](#pre-commit-hooks-for-local-development)
- [Feature and Issue Management (`todo.toml`)](#feature-and-issue-management-todotoml)
- [Design Notes (`DESIGN_NOTES.md`)](#design-notes-design_notesmd)
- [Suggested Open Source Projects](#suggested-open-source-projects)

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
    This will install all necessary packages, including `pytest` for testing, `memory_profiler` for the memory profiling decorator, `flake8` for linting, `toml` for configuration file parsing, and `pre-commit` for git hook management.

4.  **(Optional but Recommended) Set up Pre-commit Hooks:**
    After cloning the repository and installing dependencies, install the git hooks:
    ```bash
    pre-commit install
    ```
    See the [Pre-commit Hooks](#pre-commit-hooks-for-local-development) section for more details.


## Usage Examples

1.  **View CLI help:**
    ```bash
    python main.py --help
    ```

2.  **Run a workload:**
    *   To run the sample workload:
        ```bash
        python main.py run_workload sample_workload
        ```
    *   To run the CPU-intensive Fibonacci workload:
        ```bash
        python main.py run_workload cpu_intensive_workload
        ```
    *   To run the I/O-bound file operations workload:
        ```bash
        python main.py run_workload io_bound_workload
        ```
    *   To run the prime number calculation workload (Segmented Sieve):
        ```bash
        python main.py run_workload prime_minimal_branching_workload
        ```
    Replace the workload name with the name of the workload you wish to run.

## Project Structure

-   `main.py`: The main entry point for the CLI application. Handles argument parsing and orchestrates tasks.
-   `config.toml`: Application-wide configuration file (see [Configuration](#configuration-configtoml) section).
-   `todo.toml`: For manual tracking of features or problematic tests (see [Feature and Issue Management](#feature-and-issue-management-todotoml) section).
-   `DESIGN_NOTES.md`: Contains notes on potential future development and architectural considerations.
-   `.pre-commit-config.yaml`: Configuration for pre-commit hooks (see [Pre-commit Hooks](#pre-commit-hooks-for-local-development) section).
-   `modules/`: Contains reusable Python modules with core application logic.
    -   `example_module.py`: An example module demonstrating basic functionality.
    -   `app_logging.py`: Configures the application's logging system (see [Application Logging](#application-logging) section).
-   `decorators/`: Houses custom decorators, such as for profiling.
    -   `profiling.py`: Contains performance profiling decorators (`time_it`, `memory_profile_it`).
-   `workloads/`: Stores scripts that define specific tasks or operations to be executed by the CLI.
    -   `sample_workload.py`: An example workload script.
    -   `cpu_intensive_workload.py`: A workload that performs a CPU-bound task (Fibonacci calculation).
    -   `io_bound_workload.py`: A workload that simulates I/O-bound tasks (file operations).
    -   `prime_minimal_branching_workload.py`: Calculates prime numbers up to a given limit using a segmented sieve algorithm.
-   `tests/`: Contains unit tests for the project.
    -   `test_example_module.py`: Tests for `modules/example_module.py`.
    -   `test_profiling.py`: Tests for the decorators in `decorators/profiling.py`.
    -   `test_prime_minimal_branching.py`: Tests for the prime number generation functions.
-   `.github/workflows/`: Contains GitHub Actions workflow files.
    -   `python_ci.yml`: Defines the CI/CD pipeline (see [CI/CD Pipeline](#cicd-pipeline) section).
-   `jules/`: Directory for verbose logging output and other runtime-generated files (gitignored).
-   `requirements.txt`: Lists project dependencies.
-   `.gitignore`: Specifies intentionally untracked files that Git should ignore.
-   `.flake8`: Configuration file for the Flake8 linter.

## Configuration (`config.toml`)

The application uses a `config.toml` file located in the root directory for managing application-wide settings. This allows for easy modification of parameters without changing the source code.

**Supported Settings:**

*   `app_name` (string): The name of the application. (Example: "PythonProfilingFramework")
*   `log_level` (string): Sets the logging verbosity for the application.
    *   Possible values: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
    *   This setting is used by `modules/app_logging.py` to configure the logger.
    *   If the file, key, or value is invalid, a default of `INFO` is used.

*   `[workload_defaults]` (table): A section for defining default parameters for workloads.
    *   `default_iterations` (integer, example): An example of a default value that could be used by workloads.
    *   *This section is currently illustrative and not programmatically enforced by all workloads.*

*   `[profiling]` (table): A section for controlling profiling behavior.
    *   `enable_time_profiler` (boolean, example): Conceptual flag to enable/disable the `@time_it` decorator's output globally.
    *   `enable_memory_profiler` (boolean, example): Conceptual flag to enable/disable the `@memory_profile_it` decorator's output globally.
    *   *These flags are currently illustrative and not programmatically enforced by the decorators.*

**Modifying Settings:**
To change a setting, simply edit the `config.toml` file with a text editor and save it. The application will load the configuration when it next starts.

## Application Logging

The application utilizes Python's standard `logging` module for comprehensive event logging. The setup is managed in `modules/app_logging.py`.

**Log Destinations:**
Logs are written to two primary destinations:
1.  **Console:** Real-time log output is displayed on the console where the application is run.
2.  **Log Files:** Logs are also saved to daily rotating files located in the `jules/` directory (which is gitignored).
    *   **Filename Format:** `app_YYYYMMDD.log` (e.g., `jules/app_20231028.log`).
    *   **Rotation:** A new log file is created each day at midnight.
    *   **Retention:** The system uses `logging.handlers.TimedRotatingFileHandler` and is configured to keep the last 7 days of log files.

**Log Level Configuration:**
The verbosity of the logs is primarily controlled by the `log_level` setting in the `config.toml` file.
*   Valid levels include `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
*   If `config.toml` is missing, the `log_level` key is absent, or an invalid value is provided, the application defaults to `INFO` log level.
*   The initial loading of the configuration and any issues encountered are logged using a pre-setup logger, ensuring that messages about configuration loading itself are captured.

**Log Format:**
The standard log format is:
`%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s`

This provides a timestamp, logger name, log level, source module and line number, and the log message itself.

For detailed setup, refer to the `setup_logging` function in `modules/app_logging.py`.

## Available Decorators

The framework provides the following decorators in `decorators/profiling.py`:

*   `@time_it`: Measures and prints the execution time of the decorated function.
*   `@memory_profile_it`: Measures and prints the memory usage (before, after, and difference) of the decorated function. This decorator relies on the `memory_profiler` library. If `memory_profiler` is not installed, it will print a warning and the function will execute without memory profiling.

## CI/CD Pipeline

The project uses GitHub Actions for Continuous Integration and Continuous Delivery (CI/CD). This ensures that code changes are automatically built, tested, and linted.

**Workflow Details:**
The CI pipeline is defined in the workflow file: `.github/workflows/python_ci.yml`.

**Key Pipeline Stages:**
1.  **Triggers:** The pipeline automatically runs on:
    *   Pushes to the `main` branch.
    *   Pull requests targeting the `main` branch.
2.  **Environment:** The jobs run on an `ubuntu-latest` runner provided by GitHub Actions.
3.  **Python Version Matrix:** Tests are executed across multiple Python versions to ensure compatibility (currently configured for Python 3.12).
4.  **Code Linting:**
    *   Flake8 is used to lint the Python codebase for style consistency and potential errors. Configuration for Flake8 can be found in the `.flake8` file.
5.  **Unit Testing & Coverage:**
    *   Pytest is used to run all unit tests found in the `tests/` directory.
    *   Test coverage is measured using `pytest-cov`.
    *   The coverage report includes:
        *   A summary printed to the terminal, highlighting any missing lines.
        *   An XML file (`coverage.xml`) generated for potential integration with other tools (e.g., SonarQube, Codecov).

**Checking CI Status:**
The status of CI runs for your pushes and pull requests can be monitored directly on GitHub:
*   Navigate to the "Actions" tab of the project repository.
*   Here you will find a list of all workflow runs, their status (success, failure, in progress), and detailed logs for each step.

## Pre-commit Hooks for Local Development

To help maintain code quality and catch issues before they are committed to the repository, this project is configured to use `pre-commit`. Pre-commit hooks automatically run checks (like linting and code formatting) on your code each time you make a commit.

**Purpose:**
*   **Automated Checks:** Runs linters (Flake8) and other checks automatically.
*   **Early Issue Detection:** Catches common issues, style violations, and potential errors before they enter the codebase or CI pipeline.
*   **Consistent Code Style:** Helps ensure all contributions adhere to the project's coding standards.

**Setup Instructions:**
1.  **Install pre-commit:**
    The `pre-commit` package is listed in `requirements.txt` and will be installed when you run `pip install -r requirements.txt`. If you need to install or upgrade it separately:
    ```bash
    pip install pre-commit
    ```

2.  **Set up the git hooks:**
    Navigate to the root directory of your local clone of this repository and run:
    ```bash
    pre-commit install
    ```
    This command needs to be run only once per clone of the repository. It installs the hooks into your local `.git/hooks` directory. From now on, the configured hooks will run automatically on `git commit`.

**Running Hooks Manually:**
You can also run the pre-commit hooks manually at any time:
*   **On all files in the project:**
    ```bash
    pre-commit run --all-files
    ```
    This is useful for checking the entire codebase or after making changes to the hook configurations.

*   **On staged files (simulates what happens on commit):**
    ```bash
    pre-commit run
    ```
    This will run the hooks only on files that are currently staged for commit. If a hook modifies a file, you will need to `git add` the changes again before committing.

**Configuration:**
The pre-commit hooks are configured in the `.pre-commit-config.yaml` file located in the root of the project. This file specifies which repositories and hooks to use. Currently, it includes:
*   General file checks from `pre-commit-hooks` (e.g., `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-toml`).
*   Python linting using `flake8` with settings that match the project's `.flake8` configuration.

If a pre-commit hook makes a change to a file (e.g., removes trailing whitespace), the commit will be aborted. Review the changes, `git add` the modified files, and then try committing again.

## Feature and Issue Management (`todo.toml`)

`todo.toml` is a manually maintained file in the root of the project used to keep track of features, tests, or parts of the codebase that are currently problematic, under review, or temporarily disabled.

**Purpose:**
The primary purpose of `todo.toml` is to provide a centralized, human-readable log for such items directly within the codebase. This allows developers to quickly note down issues or disabled components without necessarily creating a formal ticket in an external system for minor or very temporary items.

**Current Use:**
At present, `todo.toml` serves purely as a documentation and tracking aid for developers. The application **does not** read this file to programmatically alter its behavior, skip tests, or disable features automatically. Its contents are for informational purposes only.

**Future Potential:**
It is envisioned that in the future, entries in `todo.toml` *could* be parsed by scripts or the application itself. This could enable functionalities such as:
*   Automatically skipping tests listed as "problematic" or "skipped_in_ci".
*   Conditionally disabling specific features or workloads during execution.
*   Altering application behavior based on flags set in this file.
Implementing such programmatic use would require further development, including parsing logic and integration into the relevant parts of the application and CI/CD pipeline.

**Example Entry Format (Conceptual):**
Entries in `todo.toml` are conceptual and can be structured as needed. A TOML format allows for clear key-value pairs and sections. Here's an example:

```toml
# Example of a feature that is temporarily disabled
[feature_advanced_plotting]
status = "disabled"
reason = "Depends on an external library with a critical bug (Bug #789)."
associated_ticket = "JIRA-123"
owner = "data_viz_team"
re_evaluate_date = "2024-09-01"

# Example of a test that is flaky in CI
[test_workload_alpha_memory_usage]
status = "skipped_in_ci"
reason = "Test shows inconsistent memory readings on CI runners, needs investigation."
notes = "Runs fine locally. Might be related to CI environment constraints."
github_issue = "#567"
```
Key fields might include:
*   `status`: Current state (e.g., "disabled", "problematic", "under_review", "skipped_in_ci").
*   `reason`: A brief explanation.
*   `associated_ticket` or `github_issue`: Links to formal issue trackers.
*   `owner` or `team`: Who is responsible or most familiar with the item.
*   `re_evaluate_date` or `condition_to_reenable`: When or under what conditions this item should be revisited.

**Not a Replacement for Proper Issue Trackers:**
It is important to emphasize that `todo.toml` is intended for quick, in-codebase notes and tracking of temporary states. It is **not** a replacement for a full-fledged issue tracking system like GitHub Issues, Jira, Asana, etc. Formal bug reports, feature requests, and detailed task management should still reside in those dedicated systems. `todo.toml` can serve as a bridge or a quick reference to items also tracked more formally elsewhere.

## Design Notes (`DESIGN_NOTES.md`)

For insights into potential future development directions, advanced architectural considerations, and ideas for extending the framework (such as multi-language workload support), please refer to the `DESIGN_NOTES.md` file in the root of the project.

## Suggested Open Source Projects

Here are some open-source projects that could be beneficial for extending this framework:

### CLI Frameworks
*   **Click:** A popular Python package for creating beautiful command-line interfaces with as little code as necessary. It's highly configurable and comes with sensible defaults.
*   **Typer:** Built on top of Click, Typer is designed to be easy to use and provides type hints-based CLI argument parsing. It's a good choice if you like using Python type hints.
*   **Argparse:** (Already used in a basic way) Part of the Python standard library, it's robust for parsing command-line arguments. For more complex CLIs, Click or Typer might offer a more convenient API.

### Profiling Libraries
*   **cProfile and pstats:** Built-in Python modules for deterministic profiling. `cProfile` collects profiling data, and `pstats` helps analyze it. Good for understanding time spent in different functions.
*   **memory-profiler:** (Already included in `requirements.txt`) A Python module for monitoring memory consumption of a process as well as line-by-line memory consumption of functions.
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
