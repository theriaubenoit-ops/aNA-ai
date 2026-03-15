# API Reference - *aNA* v5.0

### Core framework
- **`aNA.core.BaseNucleus`**: Parent class for all brain structures.
  - `fire()`: Triggers neuronal activity.
  - `update_metabolism()`: Adjusts energy based on activity.

### Neuromodulation
- **`aNA.anatomy.Neuromodulator`**:
  - `release(type, intensity)`: Injects a global influence *(ACh, Adrenaline)*.

### Dashboard & observation
- **`aNA.gui.DashboardInterface`**:
  - `poll_metrics()`: Retrieves the overall system state *(mV, NRG, GATE)*.

### Configuration
- **`aNA.config.get_tempest()`**: Returns the current sensitivity settings.

*BT 2026-03-12*
