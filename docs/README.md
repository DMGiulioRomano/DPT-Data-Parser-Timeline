# DPT - Delta Personal Timeline

## Overview
DPT (Delta Personal Timeline) is a PyQt5-based desktop application for creating and managing musical timelines. It provides a visual interface for arranging and manipulating musical clips with various parameters.

## Features
- Visual timeline interface with multiple tracks
- Drag-and-drop clip manipulation
- Parameter editing for each clip
- Zoom in/out functionality
- Grid-based snapping
- Custom color assignments for clips
- Search functionality for clip parameters
- File save/load support (YAML format)
- Integration with external make commands

## System Requirements
- Python 3.11
- PyQt5
- PyYAML

## Project Structure

### Core Components

#### `main.py`
Entry point of the application. Initializes the QApplication and main window.

#### `MainWindow.py`
Main application window containing:
- Menu bar with File, Edit, View, and Settings menus
- Timeline view
- Control buttons
- Search functionality
- File handling operations

#### `Timeline.py`
Manages the timeline scene:
- Grid drawing
- Track management
- Zoom functionality
- Time markers
- Visual scaling

#### `TimelineView.py`
Handles user interaction with the timeline:
- Mouse and keyboard events
- Rubber band selection
- Zooming
- Item duplication
- Navigation

#### `MusicItem.py`
Represents individual clips on the timeline with:
- Draggable behavior
- Parameter storage
- Visual representation
- Color customization

### Dialogs

#### `ParamDialog.py`
Dialog for editing clip parameters:
- Numeric value editing
- List parameter support
- Color selection

#### `RenameDialog.py`
Simple dialog for renaming clips.

#### `SettingsDialog.py`
Application settings management:
- Directory configurations
- Text styling options
- Color preferences

## Key Features

### Timeline Navigation
- Zoom: `Ctrl +/-` or mouse wheel
- Pan: Alt + Arrow keys
- Track movement: Ctrl + Up/Down arrows

### Clip Management
- Create: Ctrl + T
- Delete: Delete/Backspace
- Duplicate: Ctrl + D
- Rename: Return key
- Move: Drag or Ctrl + Left/Right arrows
- Resize: Ctrl + Shift + Left/Right arrows

### Parameters
Each clip contains:
- cAttacco: Attack time
- durataArmonica: Harmonic duration
- ritmo: Rhythm values
- durata: Duration
- ampiezza: Amplitude
- frequenza: Frequency
- posizione: Position

### File Operations
- New: Ctrl + N
- Open: Ctrl + O
- Save: Ctrl + S
- Save As: Ctrl + Shift + S

## Configuration
The application uses `settings.json` for storing:
- Default directories
- Text appearance
- Make command directory
- Other preferences

## Make Integration
The application integrates with external make commands through:
- Configurable make directory
- Section-based compilation
- YAML to make command parameter passing

## Usage

1. **Starting the Application**
   ```bash
   python3.11 main.py
   ```

2. **Creating a New Timeline**
   - Use File > New or Ctrl + N
   - Add clips using Ctrl + T or the "Add Item" button

3. **Editing Clips**
   - Double-click or Cmd/Meta + click to edit parameters
   - Drag to reposition
   - Use keyboard shortcuts for precise movements

4. **Saving Work**
   - Save as YAML files
   - Integrates with make system for further processing

## Development

### Adding New Features
- Follow PyQt5 widget structure
- Maintain grid-based positioning system
- Use existing parameter dialog system for new parameters

### Style Guidelines
- Use Qt's signal/slot mechanism
- Maintain consistent grid measurements
- Follow existing naming conventions

## Troubleshooting

Common issues:
1. **Make Command Fails**
   - Check make directory configuration
   - Verify YAML file format
   - Ensure correct section names

2. **Clip Movement Issues**
   - Check grid snapping settings
   - Verify track boundaries
   - Confirm zoom level settings

3. **File Operations**
   - Verify directory permissions
   - Check YAML format consistency
   - Confirm file extensions
