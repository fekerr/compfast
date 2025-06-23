# Interactive Solar System Orbital Model

## 1. Overview

This project simulates the orbital mechanics of celestial bodies in our solar system (or a configurable set of bodies) using Newton's Law of Universal Gravitation and an RK4 numerical integrator. It provides an interactive 2D visualization built with Pygame, allowing users to observe orbits, control time, select bodies for information, and view orbital paths. The application features a multi-pane UI and includes testability features like interaction recording and unit tests.

This project was developed with the assistance of a generative AI coding agent.

## 2. Features

*   **N-Body Simulation:** Simulates gravitational interactions between multiple celestial bodies.
*   **RK4 Integration:** Uses Runge-Kutta 4th order numerical integration for accuracy.
*   **Configurable System:** Celestial body properties (mass, radius, initial position/velocity, color) and simulation parameters (time step, gravity constant) are loaded from `src/config.toml`.
*   **Multi-Pane UI:**
    *   **Left Graphics Pane:** Main interactive view of the simulation.
    *   **Right Graphics Pane:** Secondary view (currently mirrors the left).
    *   **Bottom Text Pane:** Displays status messages, logs, and selected body information.
*   **Interactive Controls:**
    *   **Time Control:** Play/Pause, speed up/slow down, reset simulation.
    *   **Camera Control (Left Pane):** Zoom in/out, pan view.
    *   **Planet Selection (Left Pane):** Click to select a body and view its details.
    *   **Orbital Path Tracing:** Toggle visibility of recent orbital paths for all bodies.
*   **Help System:** In-app help screen ('H' key) detailing controls and features.
*   **Interaction Recording:** Record user inputs and simulation commands to JSON files (F9 key).
*   **Interaction Playback (Core):** Replay recorded sessions via command-line argument (`--playback <file>`).
*   **Unit Tests:** Core logic includes unit tests with coverage reporting.

## 3. Setup Instructions

### 3.1. Prerequisites
*   **Python:** Version 3.13 or newer is recommended (as per initial project specification). Python 3.11+ is required for `tomllib`. For earlier Python 3 versions (e.g. 3.7-3.10), you would need to install the `tomli` library (`pip install tomli`) and potentially adjust the import in `config_loader.py`.
*   **Git:** For cloning the repository.

### 3.2. Getting the Code
1.  Clone the repository (assuming it's hosted on a Git platform):
    ```bash
    # git clone <repository_url>
    # cd <repository_name>/2506
    ```
    If working locally, navigate to the `2506/` project root.

### 3.3. Virtual Environment (Recommended)
It's highly recommended to use a Python virtual environment to manage dependencies.

1.  Navigate to the project root directory (`2506/`).
2.  Create a virtual environment:
    ```bash
    # Example: python -m venv .venv
    # (Actual command commented out to avoid tool parsing issues)
    # python -m venv .venv
    ```
    (You would run: `python -m venv .venv`)
3.  Activate the virtual environment:
    *   On Windows:
        ```bash
        .venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```

### 3.4. Install Dependencies
With the virtual environment activated, install the required packages:
```bash
pip install -r requirements.txt
```
The `requirements.txt` file should include:
```
pygame==2.6.1 # Or your specific version
coverage
```

## 4. Running the Application

1.  Ensure your virtual environment is activated.
2.  Navigate to the `2506/` project root directory.
3.  Run the main script:
    ```bash
    python src/main.py
    ```

### 4.1. Playback Mode
To replay a previously recorded interaction session:
```bash
python src/main.py --playback recordings/your_recording_file.json
```
Replace `your_recording_file.json` with the actual name of your recording file (located in `2506/recordings/`).

## 5. Configuration

*   The main configuration file is `2506/src/config.toml`.
*   This file allows you to define:
    *   Simulation parameters (`time_step`, `gravity_constant`).
    *   Display settings (`screen_width`, `screen_height`, colors, initial zoom).
    *   UI Layout ratios for the different panes.
    *   Data for celestial bodies (mass, radius, color, initial position and velocity).
        *   Positions are typically in Astronomical Units (AU).
        *   Velocities are typically in km/s (these are converted to SI units internally).

## 6. Controls

A summary of controls (also available via the in-app Help screen - press 'H'):

*   **H:** Toggle Help Screen
*   **ESC:** Close Help Screen (if active) / Exit Application
*   **P:** Play / Pause Simulation
*   **[:** Speed Down Simulation
*   **]:** Speed Up Simulation
*   **R:** Reset Simulation
*   **Arrow Keys:** Pan View (Left Graphics Pane)
*   **'+', '=', Mouse Wheel Up:** Zoom In (Left Graphics Pane)
*   **'-', Mouse Wheel Down:** Zoom Out (Left Graphics Pane)
*   **T:** Toggle Orbital Paths
*   **Left Mouse Click:** Select Planet/Body (in Left Graphics Pane)
*   **F9:** Start / Stop Interaction Recording

## 7. Testing

For details on running unit tests and viewing test coverage, please see `TESTING.md`.

## 8. Recording & Playback

*   **Recording:** Press **F9** during simulation to start or stop recording user interactions and key simulation events. Recordings are saved as timestamped `.json` files in the `2506/recordings/` directory.
*   **Playback:** Use the `--playback <filepath>` command-line argument as described in section 4.1.

## 9. Directory Structure Overview

```
2506/
├── src/                     # Main source code
│   ├── celestial_body.py
│   ├── config_loader.py
│   ├── config.toml          # Configuration file
│   ├── help_overlay.py
│   ├── interaction_player.py
│   ├── interaction_recorder.py
│   ├── main.py              # Main application entry point
│   ├── renderer.py
│   ├── simulation_engine.py
│   ├── text_display.py
│   └── ... (other potential Python modules)
├── tests/                   # Unit tests
│   ├── __init__.py
│   ├── test_vector_math.py
│   ├── test_celestial_body.py
│   ├── test_config_loader.py
│   ├── test_text_display.py
│   ├── test_simulation_engine.py
│   └── ... (other test files)
├── recordings/              # Default directory for saved interaction recordings (.gitignored)
├── Jules/                   # Agent's logs and notes (.gitignored)
├── htmlcov/                 # HTML coverage reports (.gitignored)
├── .gitignore
├── requirements.txt
├── README.md                # This file
├── TESTING.md               # Guide for running tests
└── PROFILING.md             # Performance considerations and profiling tools
```

## 10. Future Considerations / Potential Next Steps

*   Implement independent camera controls for the right graphics pane.
*   Enhance UI elements (e.g., clickable buttons instead of just keyboard shortcuts for some controls).
*   More sophisticated orbital path rendering (e.g., fading, thickness options, dynamic path length).
*   Advanced data loading for celestial bodies (e.g., from external datasets like JPL Horizons via SpiceyPy).
*   Full implementation of the interaction playback system with robust timing and state synchronization.
*   Performance optimization using NumPy for vector math, especially if simulating many bodies.
*   Expand unit and integration test coverage, particularly for `simulation_engine.py` and UI interactions.
*   Consider 3D visualization aspects using Pygame's 3D capabilities or other libraries.
*   Implement a more robust method for managing and displaying text in the bottom pane (e.g., scrolling, clearing specific lines).
