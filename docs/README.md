# DPT Technical Documentation

## Architecture Overview

### Core Components

#### MainWindow (MainWindow.py)
- Primary application controller
- Manages UI layout and menu structure
- Handles file operations and timeline state
- Implements search functionality and parameter management

#### Timeline System
The timeline is built on three key components:

1. **Timeline (Timeline.py)**
   - Scene management and grid system
   - Track handling and zoom coordination
   - Parameter-based item positioning
   - Color management and visual styling

2. **TimelineView (TimelineView.py)**
   - User interaction handling
   - Selection and drag operations
   - Keyboard shortcut implementation
   - Scroll and zoom gesture processing

3. **TimelineRuler (TimelineRuler.py)**
   - Time marker visualization
   - Zoom level adaptation
   - Grid subdivision management
   - Visual synchronization with main timeline

#### Music Items
MusicItem (MusicItem.py) implements clip behavior:
- Parameter storage and validation
- Visual representation
- Drag-and-drop functionality
- Real-time position updates

### Parameter System

#### Parameter Structure
```python
default_params = {
    "cAttacco": 0,
    "durataArmonica": 26,
    "ritmo": [7,15],
    "durata": 5,
    "ampiezza": [-30,-0.25],
    "frequenza": [6,1],
    "posizione": -8
}
```

#### Parameter Types
- Numeric: Single float values (cAttacco, durataArmonica)
- Lists: Multiple values (ritmo, frequenza)
- Ranges: Min/max pairs (ampiezza)
- Mixed: Numeric or string values (posizione)

### Settings Management

#### Settings Structure (Settings.py)
- JSON-based configuration storage
- Default value management
- Directory path handling
- Visual preference storage

#### Configurable Elements
- Directory paths
- Text styling
- Color schemes
- Timeline defaults

### Dialog System

#### Parameter Dialog (ParamDialog.py)
- Dynamic parameter field generation
- Type-aware input validation
- Color selection integration
- Real-time preview

#### Other Dialogs
- RenameDialog: Clip renaming
- SettingsDialog: Application configuration

### Build System

#### macOS Build (setup.py)
- py2app configuration
- Universal binary support (Intel/ARM)
- Resource bundling
- Icon integration

## Development Guidelines

### Adding New Features

#### Parameter Addition
1. Add parameter to MusicItem default structure
2. Update ParamDialog for new parameter type
3. Implement validation in parameter processing
4. Update YAML serialization if needed

#### UI Modifications
1. Maintain 70px left margin for track labels
2. Use settings system for colors and dimensions
3. Follow existing zoom handling patterns
4. Implement both mouse and keyboard controls

### Code Style

#### PyQt Patterns
- Use Qt signal/slot mechanism for events
- Maintain widget hierarchy
- Handle keyboard modifiers consistently
- Implement proper cleanup in closeEvent

#### Parameter Handling
- Validate all parameter inputs
- Maintain type consistency
- Support undo/redo where applicable
- Update timeline state appropriately

### File Formats

#### YAML Structure
```yaml
comportamenti:
  - cAttacco: <float>
    durataArmonica: <float>
    ritmo: <list[float]>
    durata: <float|list>
    ampiezza: <float|list>
    frequenza: <list[float]>
    posizione: <float|string|list>
```

#### Settings Format
```json
{
    "last_open_directory": "<path>",
    "last_save_directory": "<path>",
    "make_directory": "<path>",
    "text_color": "<hex>",
    "item_text_size": <int>,
    "timeline_text_size": <int>,
    "track_background_color": "<hex>",
    "timeline_background_color": "<hex>"
}
```

## Implementation Details

### Grid System
- Base unit: pixels_per_beat (default: 100)
- Zoom range: 0.05x to 4x
- Subdivision handling based on zoom level
- Snap threshold: 1/16 beat

### Parameter Processing
- String to float conversion with error handling
- List parsing with proper nesting
- Type validation and coercion
- Default value handling

### Event Handling
- Mouse events with modifier support
- Keyboard shortcuts with platform adaptation
- Selection management
- Drag operation coordination

### Performance Considerations
- Efficient item rendering
- Proper scene management
- Memory-conscious parameter storage
- Smooth zoom implementation