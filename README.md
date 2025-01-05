# DPT - Delta Parser Timeline

## Overview
DPT (Delta Parser Timeline) is a PyQt5-based desktop application for creating and managing musical timelines with parameterized behaviors. It provides an intuitive interface for arranging and manipulating clips with various musical parameters, designed specifically for composition and analysis.

## Key Features
- Multi-track timeline interface with intuitive drag-and-drop
- Parameter-based clip manipulation with real-time updates
- Intelligent grid system with adjustable zoom levels
- Advanced parameter editing with support for numeric and list values
- YAML export/import for timeline data
- Integration with external make commands for processing
- Customizable appearance with track and timeline colors
- Comprehensive search functionality across clip parameters

## System Requirements
- Python 3.11
- PyQt5
- PyYAML
- macOS 10.15 or later (for compiled application)

## Installation

### Running from Source
1. Clone the repository
2. Install dependencies:
```bash
pip install PyQt5 PyYAML
```
3. Run the application:
```bash
python main.py
```

### Running the Compiled Application (macOS)
1. Download the latest release
2. Move DPT.app to your Applications folder
3. Launch DPT from Applications

## Quick Start Guide

### Basic Controls
- **Add Clip**: Click "Add Item" or press Ctrl/Cmd + T
- **Select Clips**: Click or drag selection rectangle (with Ctrl/Cmd)
- **Move Clips**: Drag or use arrow keys with Ctrl/Cmd
- **Edit Parameters**: Double-click clip or press Ctrl/Cmd + Return
- **Zoom**: Use Ctrl/Cmd +/- or pinch gesture
- **Save/Load**: Use File menu or Ctrl/Cmd + S/O

### Timeline Navigation
- Pan: Alt + Arrow keys
- Track Navigation: Ctrl/Cmd + Up/Down arrows
- Quick Zoom: Alt + Up/Down arrows

### Clip Parameters
Each clip contains musical parameters:
- cAttacco: Starting time
- durataArmonica: Harmonic duration
- ritmo: Rhythm values (list)
- durata: Duration
- ampiezza: Amplitude (single value or range)
- frequenza: Frequency parameters (list)
- posizione: Position parameter

## File Management

### YAML Structure
Timeline data is stored in YAML format with standardized parameter structure:
```yaml
comportamenti:
  - cAttacco: 0.0
    durataArmonica: 35.0
    ritmo: [3.0]
    durata: 10.0
    ampiezza: -14.0
    frequenza: [2.0, 5.0]
    posizione: [-2.0, GEN06]
```

### Settings
Application settings are stored in settings.json and include:
- Directory preferences
- Visual customization options
- Default timeline configuration

## Keyboard Shortcuts

### File Operations
- New Timeline: Ctrl/Cmd + N
- Open: Ctrl/Cmd + O
- Save: Ctrl/Cmd + S
- Save As: Ctrl/Cmd + Shift + S

### Edit Operations
- Add Clip: Ctrl/Cmd + T
- Delete Selection: Delete/Backspace
- Duplicate Clips: Ctrl/Cmd + D
- Rename Clip: Return
- Show Parameters: Ctrl/Cmd + Return

### View Controls
- Zoom In: Ctrl/Cmd + Plus
- Zoom Out: Ctrl/Cmd + Minus
- Increase Width: Ctrl/Cmd + Shift + Right
- Decrease Width: Ctrl/Cmd + Shift + Left

## Make Integration
The application integrates with external make commands through a configurable make directory setting. Timeline data can be processed using:
```bash
make SEZIONE=<yaml_filename>
```

## Support and Documentation
For detailed documentation, see the [/docs](/docs) directory.

## License
MIT License

---

For technical documentation and development details, please refer to [/docs/README.md](/docs/README.md)