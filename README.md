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

The application requires Python 3.x and the following packages:

```bash
PyQt5>=5.15.0
PyYAML>=5.1
python3.11
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dpt.git
cd dpt
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

To start the application:

```bash
python main.py
```

### Basic Controls

- **Add Clips**: Click "Add Item" button or use Cmd+T
- **Select Clips**: Click on a clip or use Cmd+drag for multiple selection
- **Move Clips**: 
  - Drag clips with mouse
  - Use Cmd+Arrow keys for fine movement
  - Use Cmd+Up/Down to move between tracks
- **Resize Clips**: Cmd+Shift+Left/Right
- **Zoom**: 
  - Use Cmd++/- for zoom in/out
  - Alt+Up/Down for alternative zoom controls
- **Navigate**: Alt+Left/Right for timeline navigation
- **Edit Parameters**: Double-click a clip or use Cmd+Return
- **Rename Clips**: Select clip and press Return
- **Delete Clips**: Select and press Delete/Backspace
- **Duplicate Clips**: Cmd+D

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New File | Cmd+N |
| Open | Cmd+O |
| Save | Cmd+S |
| Save As | Cmd+Shift+S |
| Settings | Cmd+, |
| Add New Item | Cmd+T |
| Move Right | Cmd+Right |
| Move Left | Cmd+Left |
| Move Up Track | Cmd+Up |
| Move Down Track | Cmd+Down |
| Show Parameters | Cmd+Return |
| Rename Clip | Return |
| Increase Width | Cmd+Shift+Right |
| Decrease Width | Cmd+Shift+Left |
| Exit | Cmd+Q |

### Settings

The application stores its settings in `settings.json`, which includes:
- Default directories for file operations
- Make command directory
- Text styling preferences
- Default track count and duration

## File Format

The application uses YAML files to store timeline data. Each clip in the timeline has the following parameters:

```yaml
comportamenti:
  - cAttacco: [float]  # Attack time in beats
    durataArmonica: [float]  # Harmonic duration
    ritmo: [float, float]  # Rhythm parameters
    durata: [float]  # Duration in beats
    ampiezza: [float, float]  # Amplitude range
    frequenza: [float, float]  # Frequency parameters
    posizione: [float]  # Position parameter
```

## Make Integration

The application supports integration with external Make commands. The Make directory can be configured in the settings, and the application will execute make commands using the current YAML filename as a parameter.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT LICENSE
