# DPT - Delta Personal Timeline

DPT (Delta Personal Timeline) is a PyQt5-based desktop application that provides a visual timeline interface for music composition and arrangement. It allows users to create, arrange, and manage musical clips on a multi-track timeline with precise control over timing and parameters.

## Features

- Multi-track timeline interface with customizable number of tracks
- Visual grid system with adaptive scaling and zoom levels
- Drag-and-drop clip placement with snap-to-grid functionality
- Parameter editing for each clip including attack time, duration, rhythm, amplitude, and frequency
- Color coding for clips
- Timeline zoom and navigation controls
- Save/Load functionality using YAML format
- Integration with external Make commands for processing
- Customizable text styling and directory preferences

## Dependencies

The application requires Python 3.11 and the following packages:

```bash
PyQt5>=5.15.0
PyYAML>=5.1
CMake>=3.10
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dpt.git
cd dpt
```

2. Build using CMake:
```bash
mkdir build
cd build
cmake ..
make
```

3. Run the application:
```bash
make run
```

## Project Structure

```
project_root/
├── src/
│   ├── main.py
│   ├── MainWindow.py
│   └── ... (other Python files)
├── CMakeLists.txt
├── clean-all.cmake
└── requirements.txt
```

### Build System

The project uses CMake for build management, which:
- Creates a Python virtual environment
- Installs required dependencies
- Provides build and run targets
- Manages cleanup operations

Key CMake targets:
- `make`: Build the project
- `make run`: Run the application
- `make clean-all`: Clean build artifacts

[Rest of the README remains the same...]