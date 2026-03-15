# Dashboard legend - Observer's manual - *aNA* v5.0

This document defines the metrics displayed on the *Metabolic & cognitive dashboard* and explains the biological logic behind them.

### 1. Vital metrics *(Metabolic state)*

| Metric | Full name | Biological meaning | Logic source |
| --- | --- | --- | --- |
| **-mV** | *Membrane potential* | Electrical potential of the active population. Resting: -70mV / Threshold: -55mV. | `thalamus.current_potential` |
| **NRG** | *Metabolic energy* | Level of available resources. Low *NRG* reduces processing speed and prediction accuracy. | `core.metabolism` |
| **GATE** | *THL Gate* | The Thalamus filtering threshold. Determines which stimuli reach *"consciousness"*. | `thalamus.rtn_threshold` |

### 2. Cortical cascade dynamics *(Information flow)*

The dashboard monitors how information "travels" through the architecture:

* **LGN > THL**: **Sensory phase.** Raw detection from the environment *(Input Gateway)*.
* **LGN > THL > FRN**: *Conscious pathway.* Signal analyzed by the *6-layer Cortex* before reaching the *Frontal Lobe* *(Decision)*.
* **THL > FRN**: **Executive bypass.** Fast-track reflex. Minimal *cortical* analysis for maximum speed.

### 3. Cognitive accuracy & focus

* **EFF (Efficiency)**: Ratio between Input effort and Output clarity. Low *EFF* indicates high internal *"noise"*.
* **ACh gain**: Acetylcholine influence. It sharpens the signal-to-noise ratio in Layer IV *(Attention)*.
* **PRED ERROR**: The *"Free Energy"* gap. Difference between the *Hippocampus* prediction and reality.

### 4. Amygdala & emotional modulation *(Stress response)*

These indicators measure the system's response to the unknown or failure.

* **AMY STRESS (Stress level)**: Increases when the prediction error *(PRED ERROR)* persists. A high level triggers the release of Adrenaline, increasing processing speed at the cost of energy.
* **FEAR SPIKE (Alarm)**: A sudden spike due to input radically different from the stored patterns. This forces an immediate capture in the Hippocampus (forced learning).
* **VALENCE (+/-)**: Indicates whether the current interaction is perceived as *"rewarding"* *(Dopamine)* or *"threatening"* *(Cortisol-like response)*.

**Rendering logic:**

* **Red flash (Spike)**: If `amygdala.threat_level > 0.8`.
* **Vibration/Intensity**: The higher the stress, the faster the refresh of vital metrics (simulating digital tachycardia).

### 5. Dashboard rendering rules *(for developers)*

**Visual feedback colors**

* **🟢 GREEN**: Nominal state. Prediction error is low *(< 0.2)*. Energy is stable.
* **🟡 YELLOW**: Active filtering. System is "concentrating." High *ACh* levels detected.
* **🔴 RED**: Critical error or Energy depletion. High prediction error *(> 0.8)* triggers Amygdala stress.

**Technical constraints**

* **Refresh Rate**: Real-time polling via `get_dashboard_metrics()`.
* **Layout**: Optimized for *132 x 32* character terminal or Web-GUI.
* **Abbreviations**: Use short codes *(NRG, EFF, ACh)* to maintain high data density without clutter.

*BT 2026-03-12*
