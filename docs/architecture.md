# aNA *(Autonomous Neural Architecture)* v5.0

### Architecture overview
```
├── src/
│   ├── core/                       # Core neural components
│   ├── anatomy/                    # Brain region implementations
│   ├── gui/                        # Web-based interface
│   └── tests/                      # Comprehensive test suite
├── docs/
│   ├── architecture.md             # The technical plan
│   ├── legend.md                   # (To do)
│   ├── genesis.md                  # The story of the project
│   ├── philosophy.md               # The ethical vision
│   ├── api-reference.md            # (To do)
│   ├── assets/                     # Images
│   └── examples/                   # (To do)
├── examples/
│   ├── basic-demo.html             # (To do)
│   ├── memory-demo.html            # (To do)
│   └── learning-demo.html          # (To do)
├── README.md                       # The Manifesto
├── CONTRIBUTING.md                 # The rules of collaboration
└── LICENSE.md                      # Your protection license
```

### Level 1: Core brain simulation
```
aNA v5.0 Autonomous Neural Architecture
├── Main (Controller, the Pacemaker TEMPO):
│   ├── Rhythm Orchestration: Synchronizes the processing cycle (Input -> Prediction -> Output)
│   └── Neural State Management: Ensures overall stability and module integration
│
├── Configuration (Preference)
│
└── NEW - Dashboard (Metabolic & Cognitive):
    ├── Real-time Neural Stats: Monitors neurotransmitter levels
    ├── Predictive Accuracy (Free Energy): Real-time visualization of prediction error
    └── Memory Status: Fill and consolidation state (L1/L2/L3)
```

### Level 2: Primary brain structures
```
├── Cerebral Cortex (The "Thinking" Shell, 4 Lobes + 6 Layers)
│   ├── Frontal Lobe (Logic, Planning, Motor)
│   │   ├── Prefrontal Cortex (Executive Function)
│   │   ├── Motor Cortex (Movement Planning)
│   │   └── Broca's Area (Speech Production)
│   │
│   ├── Parietal Lobe (Integration, Spatial)
│   │   ├── Somatosensory Cortex (Touch Processing)
│   │   ├── Spatial Processing (Navigation)
│   │   └── Multisensory Integration
│   │
│   ├── Temporal Lobe (Memory, Auditory)
│   │   ├── Auditory Cortex (Sound Processing)
│   │   ├── Wernicke's Area (Language Comprehension)
│   │   └── Memory Formation (with Hippocampus)
│   │
│   ├── NEW - Hippocampal Hub & Memory Integration:
│   │   ├── Role: Temporal indexer and consolidation (L1 Buffer -> L2/L3 Store)
│   │   ├── Thalamocampal Connection: Receives the raw signal + importance
│   │   │   (Amygdala) and returns predictions to the Thalamus
│   │   ├── Mechanism: Uses transition matrices (A -> B) to minimize
│   │   │   prediction error (Free Energy)
│   │   └── L1/L2/L3 Hierarchy: Adaptive management of information storage
│   │
│   ├── Occipital Lobe (Vision)
│   │   ├── Primary Visual Cortex (V1)
│   │   ├── Visual Association Areas (V2-V5)
│   │   └── Object Recognition
│   │
│   ├── Internal Wiring: Lobe-specific 6-layer columns
│   └── Long-range Wiring (The "Bridges"):
│       ├── Arcuate Fasciculus (Temporal <-> Frontal): Language/Logic Loop
│       └── Superior Longitudinal Fasciculus (Parietal <-> Frontal): Spatial/Action Loop
│       └── NEW - Corpus Callosum (Future: Left <-> Right Hemisphere)
│
├── Thalamus (The "Router", Sensory Gateway)
│   ├── Sensory Filtering, Relay Nuclei
│   │   ├── LGN (Visual → Occipital)
│   │   ├── MGN (Auditory → Temporal)
│   │   ├── VPL/VPM (Somatosensory → Parietal)
│   │   └── NEW - RTN (Firewall): Gain control and global inhibition
│   │
│   ├── Gating mechanism, Reticular Thalamic Nucleus (RTN) : Inhibits signal if global charge is too high
│   └── Thalamocortical Loops: Maintains the "Awake" state frequency
│
├── NEW - Hippocampus (The "Buffer", Memory System)
│   ├── Dentate Gyrus/CA4 (Pattern Separation: Prevents memory overlap)
│   ├── CA3 (Autoassociative Memory)
│   ├── CA2 (Social and temporal relay. It is a buffer between CA3 and CA1)
│   ├── CA1 (Pattern Integration, final output)
│   └── Entorhinal Cortex (The bidirectional bridge to the Cortex)
│
├── NEW - Cerebellum (The "Clock", Timing & Error Correction)
│   └── Coordination between Motor Cortex and Sensory Feedback
│
└── NEW - Amygdala (The "Priority Filter", Emotional Valence)
    └── Labels incoming charges as "Important" or "Neutral"

    Computational Engine: Free Energy Principle (FEP)
    aNA v5.0 optimizes prediction accuracy by minimizing the error between sensory reality and internal models (stored in the hippocampus/cortex). A high error triggers the release of neuromodulators (adrenaline/dopamine) to force learning or adaptation.
```

### Level 3: The cognitive loop *("Cognitive heart")*
```
Cognitive Loop
├── Thalamus: Sensory relay and prediction comparator
├── Hippocampus: Temporal indexing and sequence recall (L1-L3 memory gateway)
├── Amygdala: Emotional modulator (survival value and stress)
└── Interaction: The thalamus compares sensory input to the hippocampus's prediction
    The discrepancy (prediction error) is sent to the amygdala to adjust the system's alertness
```

### Level 4: Cortical layer organization *(in each Lobe)*
```
Cortical Layer Dynamics (Each Lobe contains 6 Cortical Layers)
├── Layer I (Sensory Buffer): Volatile, immediate, high resolution
├── Layer II (Associative Reinforcement): Repeated patterns, beginning of consolidation
├── Layer III (Long-Term Storage): Consolidated patterns, robust semantic structures
├── Layer IV: Internal Granular (Sensory Gateway - LGN/MGN reception)
├── Layer V: Internal Pyramidal (Motor Output - Cerebellum/Subcortical)
└── Layer VI: Multiform (Thalamic Regulatory Loop - Gain Control)
```

### Level 5: Lobe-specific functional systems
```
├── Frontal Lobe System
│   ├── Executive Function (Prefrontal)
│   ├── Motor Planning and Execution
│   ├── Decision Making
│   └── Working Memory
│
├── Parietal Lobe System
│   ├── Spatial Awareness and Navigation
│   ├── Sensory Integration
│   ├── Attention Control
│   └── Mathematical Processing
│
├── Temporal Lobe & Hippocampal Integration
│   ├── Auditory Processing
│   ├── Language Comprehension
│   ├── Memory Encoding/Retrieval
│   └── Object Recognition
│
└── Occipital Lobe System
    ├── Visual Processing (Primary)
    ├── Visual Association (Secondary)
    ├── Motion Detection
    └── Color and Shape Recognition
```

### Level 6: Cross-lobe integration
```
├── Inter-lobar Communication
│   ├── Frontal-Pariental Network (Attention)
│   ├── Temporal-Occipital Network (Visual Memory)
│   ├── Frontal-Temporal Network (Language)
│   └── Parietal-Occipital Network (Spatial Vision)
│
├── Sensory-Motor Integration
│   ├── Occipital → Parietal → Frontal (Visual Guidance)
│   ├── Temporal → Frontal (Auditory Guidance)
│   └── Parietal → Frontal (Somatosensory Guidance)
│
└── Memory Networks
    ├── Hippocampus ↔ Temporal Lobe (Episodic Memory)
    ├── Hippocampus ↔ Frontal Lobe (Working Memory)
    └── Hippocampus ↔ Parietal Lobe (Spatial Memory)
```

### Level 7: Dynamic processing flow
```
Dynamic Processing Flow:
├── Ascending (Bottom-Up): Thalamus → Occipital → Parietal → Frontal. (I see, I locate, I decide)
├── Descending (Top-Down): Frontal → Thalamus. (I decide to stop listening to this noise; the Thalamus closes the door)

Sensory Input Pathways:
├── Visual: Thalamus (LGN) → Occipital Lobe → Temporal/Frontal
├── Auditory: Thalamus (MGN) → Temporal Lobe → Frontal
└── Somatosensory: Thalamus (VPL/VPM) → Parietal Lobe → Frontal

Processing Hierarchy:
├── Primary Sensory Areas (Layer IV) → Association Areas (Layers II/III)
├── Association Areas → Integration Centers (All Layers)
└── Integration Centers → Motor Planning (Frontal Layer V)
```

### Level 8: Functional specialization by lobe *(Role summary)*
```
├── Occipital Lobe (Posterior “What” and “Where”)
│   - Primary: Visual Processing
│   - Secondary: Visual Association
│   - Tertiary: Visual Integration
│
├── Parietal Lobe (Superior “Where” and “How much” - logical)
│   - Primary: Somatosensory
│   - Secondary: Spatial Processing
│   - Tertiary: Multisensory Integration
│
├── Temporal Lobe (Inferior “Who” and “What” semantics - language/memory)
│   - Primary: Auditory Processing
│   - Secondary: Language and Memory
│   - Tertiary: Object Recognition
│
└── Frontal Lobe (Anterior “How” and “When” - action/decision)
    - Primary: Motor Planning
    - Secondary: Executive Function
    - Tertiary: Decision Making
```

### Level 9: Neuromodulator matrix *(The chemical layer):*
```
├── NO (Nitric Oxide) -> Volumetric Retrograde Signaling
│   └── Role: "Zone Strengthening". Diffuses from active neurons to nearby
│       synapses to signal "We just fired together, strengthen everything here."
│       (Crucial for local clusters and blood flow simulation).
│
├── NEW - Acetylcholine -> Sensory Sensitivity (Layer IV)
│   └── Role: "Focus & Alertness". Lowers the firing threshold of Layer IV
│       to make external inputs (Thalamus) more prominent.
│
├── Dopamine -> Reward & Plasticity (Layers II/III)
│   └── Role: "Learning Signal". Acts as a multiplier for LTP (Long-Term
│       Potentiation) in the association layers. No Dopamine = No Memory growth.
│
├─── NEW - Serotonin -> Homeostatic Balance (Global)
│   └── Role: "The Governor". Prevents runaway excitation (Epilepsy simulation)
│       by stabilizing the global neural threshold.
│
└─── NEW - Adrenaline -> Hyper-Alertness & Flashbulb Memory
    ├── Sensitivity: Acts as an overall win multiplier.
    │   All layers (I to VI) become extremely responsive.
    ├── Concentration: Reduces background “noise” by increasing the
    │   contrast between very active neurons and resting neurons.
    └── Learning: Triggers an instant “Memory Capture”
        (More charge sent to the Hippocampus/CA3).
```

*BT 2026-03-12*
