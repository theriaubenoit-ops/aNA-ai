# aNA v5.0 Neural Dashboard

A rich-based terminal dashboard inspired by "btop" for real-time monitoring of the aNA v5.0 neural architecture.

## 🧠 Features

### 🎨 **Bio-Inspired Interface**
- **Fixed Layout**: Non-scrolling dashboard with clear sections
- **3D ASCII Header**: Wireframe cube visualization
- **10 FPS Refresh Rate**: Optimized for lower-end CPUs
- **Rich-based Rendering**: Beautiful terminal interface

### 📊 **Real-Time Monitoring**
- **Thalamic Pulse**: Flashing dot every second for biological rhythm
- **6-Layer Cortical Cascade**: Visual monitoring of neural processing
- **Neuromodulator Levels**: Live bars for all 5 chemicals
- **Precision Loss Sparkline**: Historical accuracy tracking
- **System Status**: Energy, stress, and memory monitoring

### 🎯 **Bio-Inspired Color Coding**
- 🟢 **Green**: Normal activity (0.0-0.6)
- 🟡 **Yellow**: Fatigue/LTD (0.6-0.8)
- 🔴 **Red**: Stress/Critical (>0.8 accuracy loss)

### ⌨️ **Interactive System**
- **Non-blocking Input**: Independent of visual refresh rate
- **Real-time Processing**: Immediate feedback on character processing
- **Input/Output Buffers**: Track processing history
- **Character Processing**: Type to see neural pipeline in action

## 🏗️ Architecture

```
scr/gui/
├── dashboard.py          # Main dashboard implementation
├── integration.py        # Integration with aNA v5.0 system
├── test_dashboard.py     # Comprehensive testing suite
└── __init__.py          # Package exports
```

### Core Components

#### `NeuralDashboard`
- Main dashboard class with rich-based interface
- Fixed layout with two-column design
- Real-time data visualization
- Thalamic pulse animation
- Historical data tracking

#### `DashboardController`
- Integration bridge between aNA v5.0 and dashboard
- Background data collection
- Character processing pipeline
- Performance optimization

#### `NeuralDataCollector`
- Extracts data from all brain structures
- Formats data for dashboard visualization
- Background collection thread
- Thread-safe data management

## 🚀 Usage

### Basic Integration

```python
from scr.gui import integrate_dashboard_with_controller

# Connect dashboard to your main aNA controller
dashboard_controller = integrate_dashboard_with_controller(main_controller)

# Start interactive mode
dashboard_controller.run_interactive_mode()
```

### Manual Setup

```python
from scr.gui import create_dashboard_controller, create_dashboard

# Create dashboard
dashboard = create_dashboard()

# Create controller
controller = create_dashboard_controller()

# Connect to brain system
controller.connect_brain_system(your_main_controller)

# Start dashboard
controller.start_dashboard()
```

### Testing

```bash
# Run comprehensive tests
python scr/gui/test_dashboard.py --test

# Test performance only
python scr/gui/test_dashboard.py --performance

# Run live demo
python scr/gui/test_dashboard.py --demo
```

## 📊 Dashboard Sections

### Top Section: ASCII Header
```
    +--------+
   /        /|
  +--------+ |  aNA v5.0 - Neural Processing Dashboard
  |  aNA   | |
  |  v5.0  |/ 
  +--------+  
```

### Left Column: Processing Pipeline

#### **⚡ Thalamic Activity**
- Real-time thalamic activity monitoring
- Biological baseline visualization (0.15)
- Thalamic pulse indicator (• flashing dot)
- Status color coding

#### **🔬 Cortical Cascade**
- 6-layer processing visualization:
  - Layer IV (Input): Sensory reception
  - Layer II/III (Association): Pattern recognition
  - Layer V (Output): Motor planning
- Precision loss monitoring
- Attention boost visualization

#### **📊 Processing Status**
- Current character processing
- Input → Output mapping
- Processing accuracy and time
- Status indicators (✅⚠️❌)

### Right Column: System Monitoring

#### **🧪 Neuromodulator Levels**
- Live progress bars for all 5 neuromodulators:
  - Dopamine (reward, learning)
  - Acetylcholine (attention, focus)
  - Serotonin (stability, mood)
  - Norepinephrine (stress, alertness)
  - Nitric Oxide (plasticity, blood flow)

#### **⚡ System Status**
- Energy level monitoring
- Stress level tracking
- Adrenaline level display
- Color-coded status indicators

#### **🧠 Hippocampal State**
- Memory strength visualization
- Consolidation rate tracking
- Memory trace counting
- Spatial navigation signals

### Bottom Section: Interactive Zone

#### **⌨️ Input/Output Buffers**
- Real-time character input display
- Processing output tracking
- Buffer history (last 50 characters)
- Non-blocking input capture

## 🔧 Configuration

### Dashboard Configuration
```python
from scr.gui import DashboardConfig

config = DashboardConfig(
    refresh_rate=0.1,      # 10 FPS
    max_history=100,       # History points
    pulse_interval=1.0     # Thalamic pulse
)
```

### Integration Configuration
```python
from scr.gui import IntegrationConfig

config = IntegrationConfig(
    update_interval=0.1,           # Data collection rate
    dashboard_refresh_rate=0.1,    # Dashboard refresh
    data_collection_interval=0.05, # Collection frequency
    max_history_points=100         # History limit
)
```

## 🎯 Performance Optimization

### 10 FPS Guarantee
- **Efficient Rendering**: Rich library optimization
- **Smart Updates**: Only update changed data
- **Background Collection**: Separate data collection thread
- **Memory Management**: Automatic history trimming

### CPU Optimization
- **Non-blocking Input**: Input capture independent of UI
- **Efficient Data Structures**: Minimal memory overhead
- **Smart Refresh**: Only refresh when data changes
- **Thread Safety**: Proper synchronization

## 🧪 Testing

### Performance Tests
- Frame rate verification (10 FPS target)
- Memory usage optimization
- CPU load testing
- Data update performance

### Integration Tests
- Brain structure connectivity
- Data collection accuracy
- Character processing pipeline
- Error handling

### Visualization Tests
- Color scheme validation
- Layout rendering
- Animation smoothness
- Sparkline generation

## 🔗 Integration with aNA v5.0

### Brain Structure Support
- **Thalamus**: Sensory gateway monitoring
- **Occipital Lobe**: Visual processing cascade
- **Frontal Lobe**: Motor planning and execution
- **Parietal Lobe**: Spatial coordination
- **Temporal Lobe**: Semantic processing
- **Amygdala**: Emotional state tracking
- **Hippocampus**: Memory and consolidation
- **Cerebellum**: Motor coordination

### Data Flow
```
Brain Structures → Data Collector → Dashboard Controller → Neural Dashboard
```

### Real-time Updates
- **Continuous Monitoring**: All brain structures tracked
- **Live Processing**: Character processing in real-time
- **Historical Data**: Sparklines and trend analysis
- **Status Updates**: Immediate feedback on system state

## 🎨 Customization

### Color Schemes
```python
from scr.gui import ColorScheme

# Customize status colors
ColorScheme.NORMAL = "green"
ColorScheme.FATIGUE = "yellow" 
ColorScheme.STRESS = "red"
```

### Layout Customization
- Modify dashboard layout structure
- Customize panel sizes and positions
- Adjust refresh rates
- Personalize color schemes

## 🐛 Troubleshooting

### Common Issues

#### **High CPU Usage**
- Reduce refresh rate in configuration
- Limit history points
- Check for infinite loops in data collection

#### **Input Lag**
- Ensure non-blocking input is working
- Check terminal settings
- Verify threading implementation

#### **Display Issues**
- Ensure terminal supports rich formatting
- Check color scheme compatibility
- Verify layout rendering

### Performance Tips
- Use appropriate refresh rates for your system
- Monitor memory usage with large history
- Optimize data collection intervals
- Test with realistic data loads

## 📈 Future Enhancements

### Planned Features
- **Multi-monitor Support**: Extended dashboard views
- **Export Capabilities**: Data export for analysis
- **Alert System**: Notifications for critical states
- **Custom Widgets**: User-defined monitoring panels
- **Theme System**: Multiple visual themes
- **Remote Monitoring**: Network-based dashboard access

### Research Integration
- **Data Logging**: Comprehensive system logging
- **Analysis Tools**: Built-in data analysis
- **Visualization Export**: Charts and graphs
- **Research Interface**: Academic research support

## 🤝 Contributing

### Development Guidelines
- Follow existing code patterns
- Maintain performance standards
- Add comprehensive tests
- Document new features
- Ensure backward compatibility

### Testing Requirements
- All new features must include tests
- Performance benchmarks required
- Integration tests for brain structures
- User interface testing

## 📄 License

This dashboard is part of the aNA v5.0 project by Benoit Theriault.

## 🙏 Acknowledgments

- **Benoit Theriault**: Architecture and supervision
- **Rich Library**: Terminal interface framework
- **Neuroscience Research**: Biological inspiration
- **Open Source Community**: Tools and libraries

---

**Experience the future of neural architecture monitoring with aNA v5.0's bio-inspired dashboard!** 🧠✨