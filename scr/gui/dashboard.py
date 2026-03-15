#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neural Dashboard for aNA v5.0

This module implements a rich-based terminal dashboard
for real-time monitoring of the neural architecture.

Features:
- Fixed layout with non-scrolling interface
- Real-time neural activity monitoring
- Bio-inspired color coding
- Precision loss sparkline
- Non-blocking input system

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline and GPT
"""

import time
import threading
import sys
import select
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich import box
import numpy as npPadding
import os

# Minimum window size
import os
os.system("resize -s 32 132")  # Set rows and columns   

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import all components
from core.neuromodulator import NeuromodulatorMatrix, NeuromodulatorType
from core.input_gateway import InputGateway, create_ascii_input_gateway
from core.output_gateway import OutputGateway, create_high_precision_output_gateway
from core.neural_transmission import NeuralTransmission
from anatomy.thalamus import Thalamus, ThalamicNucleusType
from anatomy.cortex.occipital import OccipitalLobe, create_primary_occipital
from anatomy.cortex.frontal import FrontalLobe, create_motor_focused_frontal
from anatomy.cortex.parietal import ParietalLobe, create_spatial_focused_parietal
from anatomy.cortex.temporal import TemporalLobe, create_semantic_focused_temporal
from anatomy.amygdala import Amygdala
from anatomy.hippocampus import Hippocampus
from anatomy.cerebellum import Cerebellum

@dataclass
class DashboardConfig:
  
    """Configuration for the neural dashboard"""
    refresh_rate: float = 0.1  # 10 FPS (0.1 seconds)
    max_history: int = 100     # Maximum history points for sparkline


class ColorScheme:
    """Bio-inspired color scheme for neural monitoring"""
    
    # System states
    NORMAL = "green"
    FATIGUE = "yellow"
    STRESS = "red"
    CRITICAL = "bright_red"
    
    # Brain regions
    THALAMUS = "cyan"
    OCCIPITAL = "blue"
    PARIETAL = "magenta"
    TEMPORAL = "purple"
    FRONTAL = "bright_blue"
    
    # Neuromodulators
    DOPAMINE = "bright_green"
    ACETYLCHOLINE = "bright_yellow"
    SEROTONIN = "bright_cyan"
    NOREPINEPHRINE = "bright_red"
    NO = "bright_magenta"
    
    # Status indicators
    ACTIVE = "bold green"
    IDLE = "dim"
    PROCESSING = "bold yellow"
    ERROR = "bold red"


class NeuralHistory:
    """Manages historical data for sparklines and trend analysis"""

    def __init__(self, max_length: int = 100):
        self.max_length = max_length
        self.precision_history: List[float] = []
        self.energy_history: List[float] = []
        self.stress_history: List[float] = []
        self.thalamic_history: List[float] = []
        self.timestamp_history: List[float] = []
    
    def add_point(self, precision: float, energy: float, stress: float, thalamic: float):
        """Add a new data point to all histories"""
        current_time = time.time()
        
        # Add to histories
        self.precision_history.append(precision)
        self.energy_history.append(energy)
        self.stress_history.append(stress)
        self.thalamic_history.append(thalamic)
        self.timestamp_history.append(current_time)
        
        # Trim histories if too long
        if len(self.precision_history) > self.max_length:
            self.precision_history.pop(0)
            self.energy_history.pop(0)
            self.stress_history.pop(0)
            self.thalamic_history.pop(0)
            self.timestamp_history.pop(0)


class NeuralDashboard:
    """
    Main dashboard class for aNA v5.0 neural monitoring
    
    Provides a rich-based terminal interface with:
    - Real-time brain activity monitoring
    - Processing pipeline status
    - Interactive input/output system
    """
    
    def __init__(self, config: Optional[DashboardConfig] = None):
        self.config = config or DashboardConfig()
        self.console = Console()
        self.layout = Layout()
        self.history = NeuralHistory(self.config.max_history)

        # Test thalamus
        self.thalamus = Thalamus()
        self.processing_history = []
        
        # Dashboard state
        self.is_running = False
        self.current_data: Dict[str, Any] = {}
        self.input_buffer = []
        self.output_buffer = []
        
        # Threading for non-blocking input
        self.input_thread = None
        self.input_event = threading.Event()
        
        self._setup_layout()
    
    def _setup_layout(self):
        """Setup the dashboard layout structure 132 (80 to 132) x 32 (24 to 42)"""
        # Main layout structure
        self.layout.split_column(
            Layout(name="header", size=12),      # ASCII header
            Layout(name="dashboard", ratio=14, minimum_size=4),  # Main monitoring area
            Layout(name="interactive", size=4)   # Input/output area
        )
        
        # Dashboard split into two columns
        self.layout["dashboard"].split_row(
            Layout(name="left_column", ratio=1),
            Layout(name="right_column", ratio=1)
        )
        
        # Left column: Processing pipeline
        self.layout["left_column"].split_column(
            Layout(name="vitalflux_section", size=4),
            Layout(name="corticalprecision_section", size=5),
            Layout(name="neuromodulatorsavg_section", size=5)
        )
        
        # Right column: System monitoring
        self.layout["right_column"].split_column(
            Layout(name="cascadeprocessing_section", size=4),
            Layout(name="memoryandplasticity_section", size=5),
            Layout(name="cortexactivity_section", size=5)
        )
    
    
    # Le Flash de la Création
    def create_ascii_header(self) -> Panel:
        """Create the 3D wireframe ASCII header"""
        output_text = " ".join(self.output_buffer[-10:]) if self.output_buffer else "[italic dim]—[/italic dim]"
        header_text = f"""
░                            ░░░░░░░░░░▒▒▒▒▒▒░░                                                                ░░░░░░░░░░░░▒▒▒▒
                  ░░░░░░░░░▒▒▒▒▒▓▒▒▒▒░░░░░░░░░░▒▒▒▒░                          ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒
░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▒░░░░░▒▒▒░░░░▒▓▒░░      ░░░░░░░░░░░░░░░░░░░░░░▒▒░░▒▒▒▓▓▓▓▓▓▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒
░░░░░░░░░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓▓▓▓▓▓▒░░▒▒▒░░░░▒▓▓▓▓▓▓▒▒▒▒▒░   ░▒▒▒▒▒▒▒▒▓▒▒░▒▓▒░░░░░░▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░▒▒▒▒▒
▒▒▒▒▒░░░░░░░░▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▒░         ░░▒▒▒░▒▒▒▒▓▓▓▓▓▓▓▒▒░░           ░▒▒░░▒▒▓▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓▓▓▓▓▓
▒░░░░▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓░                     ░▒▒▓▒░▒▓▓▓░▒▒░░        ░░░▒▒▓▓▒▒▓▓▓▓▓▓▓▓▓▒░      ░▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
░░░░▒▒▒▒▒▓▓▓▓▓▓▓▒▒░░                           ░▓▓▒░░▒▓▓░ _   _   _  ░▒▓▓▒▓▒▒▒▓▓▓▒▒░░                              ░░░░▒▒▒▒░░░░
▒▒▓▓▓▓▓▓▓▓▒░  AI inspired by natural plasticity ░░   ░░░  a   N   A  ░▓▓▒▓░░▒▓░ Autonomous Neural Architecture v5.0 
▓▓▒▒░░                                                    ‾   ‾   ‾   ░▒▓░ ░░░
Motor Outputs: [italic dim]{output_text}[/italic dim]
        """.strip()
        
        return Panel(
            header_text,
            border_style="#444444"
        )
    

    def create_vitalflow_monitor(self, title) -> Panel:
        """Create Vital Flow monitor with pulse"""
        # À faire
        content = f"""
Thalamic Rhythm: 1.0s   Membrane Potential: [italic dim]-55mV[/italic dim]
Overall Energy: ▒▒▒▒▒▒▒▒░░ [italic dim]50.0%[/italic dim]   THL Gate: [italic dim]0.15[/italic dim]
Neurons: [italic dim]1000000[/italic dim]
        """.strip()
        
        return Panel(
            content,
            title="[bold #666666]⚡ Vital Flow[/bold #666666]",
            border_style="#444444"
        )
    

    def create_corticalprecision_monitor(self, title) -> Panel:
        """Create Cortical Precision monitor"""
        # À faire
        content = f"""
Precision Loss: [italic dim]BATTLE[/italic dim]   Gain (ACh): [italic dim]IDLE[/italic dim]
Exp Cascade: ▒▒▒▒▒▒▒▒░░ [italic dim]65.0% (0.90×0.85×0.85)[/italic dim]
EFF: ▒▒▒▒▒▒▒▒░░ [italic dim]85.0%[/italic dim]   Cortical columns: [italic dim]10000[/italic dim]
        """.strip()
        
        # Détail non utilisé : 65% (0.90×0.85×0.85)

        return Panel(
            content,
            title="[bold #666666]📊 Cortical Precision[/bold #666666]",
            border_style="#444444"
        )
    

    def create_neuromodulatorsavg_monitor(self, title) -> Panel:
        """Create Neuromodulators Avg monitor"""
        # À faire
        content = f"""
DA: ▒▒▒▒▒▒▒▒░░ [italic dim]50.0%[/italic dim]   ACh: ▒▒▒▒▒▒▒▒░░ [italic dim]50.0%[/italic dim]
5-HT: ▒▒▒▒▒▒▒▒░░ [italic dim]50.0%[/italic dim]   NE: ▒▒▒▒▒▒▒▒░░ [italic dim]50.0%[/italic dim]
NO (Gas): ▒▒▒▒▒▒▒▒░░ [italic dim]50.0%[/italic dim]
        """.strip()
        
        return Panel(
            content,
            title="[bold #666666]⚗️ Neuromodulators Avg[/bold #666666]",
            border_style="#444444"
        )
    

    def create_cascadeprocessing_monitor(self, title) -> Panel:
        """Create Cascade Processing monitor"""
        # À vérifier


        # Create complete result
        result = {
            'brain_activity': {
                'thalamus': self.thalamus.get_activity()
            }
        }
        self.processing_history.append(result)

        # latest = self.processing_history[-1] if self.processing_history else None
        # brain_activity = latest.get('brain_activity', {}) if latest else {}
        # thalamus_val = brain_activity.get('thalamus', 0.0)
        # occipital_val = 0.0
        # frontal_val = 0.0

        if self.processing_history:
            latest = self.processing_history[-1]
            brain_activity = latest.get('brain_activity', {}) if latest else {}
            thalamus_val = brain_activity.get('thalamus', 0.0)
            occipital_val = 0.0
            frontal_val = 0.0
            lgn_thalamus_frontal_val = 0.0
            thalamus_frontal_val = 0.0
            lgn_to_thl = 0.0
            thl_to_frn = 0.0

        if 'occipital' in brain_activity:
                occipital_outputs = brain_activity['occipital']
                if 'v1_features' in occipital_outputs:
                    occipital_val = occipital_outputs['v1_features'].get('output_activity', 0.0)
        
        if 'frontal' in brain_activity:
                frontal_outputs = brain_activity['frontal']
                frontal_val = frontal_outputs.get('final_output', 0.0)

        # Logique d'affichage propre
        # if thalamus_val is None:
        #     display_val = "IDLE"
        # else:
        #     display_val = f"{thalamus_val:.6f}"

        # Exemple de logique de flux dans ton objet "Cortex" ou orchestrateur
        # Dans ton orchestrateur ou main.py
        def get_neural_data(self):
            lgn_nucleus = self.thalamus.get_nucleus(ThalamicNucleusType.LGN)
            
            # Extraction des flux
            lgn_to_thl = lgn_nucleus.get_input_signal() # Ton signal sensoriel brut
            thl_to_frn = self.thalamus.get_output_to_frontal() # Ton signal traité
            
            return {
                'lgn_to_thl': lgn_to_thl,
                'thl_to_frn': thl_to_frn
            }

        def get_neural_flow(self):
            # 1. Le LGN (entrée sensorielle) envoie au Thalamus
            lgn_thalamus_frontal_val = self.lgn.get_output() 
            
            # 2. Le Thalamus traite et envoie au Frontal
            thalamus_frontal_val = self.thalamus.process(lgn_thalamus_frontal_val)
            
            # 3. Le Frontal reçoit et génère une activité
            frontal_activity = self.frontal.get_activity()
            
            return {
                'lgn_nucleus': lgn_nucleus,
                'thalamus_frontal_val': thalamus_frontal_val,
                'frontal_activity': frontal_activity
            }

        content = f"""
LGN → THL: [italic dim]{thalamus_val:.2f}[/italic dim]   THL → OCC: [italic dim]{occipital_val:.2f} (×0.90)[/italic dim]
LGN → THL → FRN: [italic dim]{lgn_thalamus_frontal_val:.2f}[/italic dim]   THL → FRN: [italic dim]{thalamus_frontal_val:.2f}[/italic dim]
OCC → FRN: [italic dim]{frontal_val:.2f} (×0.85)[/italic dim]   FRN → Out: [italic dim]{latest.get('output_character', '?')}[/italic dim]
        """.strip()

        return Panel(
            content,
            title="[bold #666666]🔬 Cascade Processing[/bold #666666]",
            border_style="#444444"
        )
    

    def create_memoryandplasticity_monitor(self, title) -> Panel:
        """Create Memory and Plasticity monitor"""
        # À faire
        content = f"""
Memory Traces: [italic dim]0.0000[/italic dim]   LTP/LTD Rate: ▒▒▒▒▒▒▒▒░░ [italic dim]50.0%[/italic dim]
Pattern Separation: ▒▒▒▒▒▒▒▒░░ [italic dim]50.0%[/italic dim]  
Hippocampal Out: [italic dim]0.0000[/italic dim]
        """.strip()
        
        return Panel(
            content,
            title="[bold #666666]💡 Memory & Plasticity[/bold #666666]",
            border_style="#444444"
        )
    

    def create_cortexactivity_monitor(self, title) -> Panel:
        """Create Cortex Activity monitor"""
        # À faire
        content = f"""
Occipital: ▒▒▒▒▒▒▒▒░░ [italic dim]50.0%[/italic dim]   Parietal: ▒▒▒▒▒▒▒▒░░ [italic dim]50.0%[/italic dim]
Temporal: ▒▒▒▒▒▒▒▒░░ [italic dim]50.0%[/italic dim]   Frontal: ▒▒▒▒▒▒▒▒░░ [italic dim]50.0%[/italic dim]
Amygdala: ▒▒▒▒▒▒▒▒░░ [italic dim]50.0%[/italic dim]
        """.strip()
        
        return Panel(
            content,
            title="[bold #666666]🧠 Cortex Activity[/bold #666666]",
            border_style="#444444"
        )
    

    def create_sensoryinputs_section(self) -> Panel:
        """Create the interactive input/output section"""
        # Input buffer display - À faire
        input_text = " ".join(self.input_buffer[-10:]) if self.input_buffer else "[italic dim]—[/italic dim]"
        content = f"""
Keyboard Input: {input_text}   Processed: [italic dim]'A' → 'A'[/italic dim]   Accuracy: ▒▒▒▒▒▒▒▒▒░ [italic dim]98.0%[/italic dim]   Time: [italic dim]15.2ms[/italic dim]
        """.strip()
    
        return Panel(
            content,
            title="[bold #666666]⌨️ Sensory Inputs[/bold #666666] [italic](Ctrl+C: Close)[/italic]",
            border_style="#444444"
        )
    
    
    def add_input_char(self, char: str):
        """Add character to input buffer"""
        self.input_buffer.append(char)
        if len(self.input_buffer) > 50:
            self.input_buffer.pop(0)
    
    def add_output_char(self, char: str):
        """Add character to output buffer"""
        self.output_buffer.append(char)
        if len(self.output_buffer) > 50:
            self.output_buffer.pop(0)
    
    def _input_thread_worker(self):
        """Worker function for non-blocking input capture"""
        while self.is_running:
            if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                try:
                    char = sys.stdin.read(1)
                    if char:
                        self.add_input_char(char)
                except:
                    pass
    
    def start_input_thread(self):
        """Start the input capture thread"""
        if self.input_thread is None or not self.input_thread.is_alive():
            self.input_thread = threading.Thread(target=self._input_thread_worker, daemon=True)
            self.input_thread.start()
    
    def stop_input_thread(self):
        """Stop the input capture thread"""
        self.is_running = False
        if self.input_thread and self.input_thread.is_alive():
            self.input_thread.join(timeout=1.0)
    
    def render_dashboard(self) -> Layout:
        """Render the complete dashboard layout"""
        
        # Create header
        self.layout["header"].update(self.create_ascii_header())
        
        # Create left column
        vitalflux_panel = self.create_vitalflow_monitor(self.current_data)
        corticalprecision_panel = self.create_corticalprecision_monitor(self.current_data)
        neuromodulatorsavg_panel = self.create_neuromodulatorsavg_monitor(self.current_data)
        
        # Update left column with split_column
        self.layout["left_column"].split_column(
            Layout(vitalflux_panel, name="vitalflux_section"),
            Layout(corticalprecision_panel, name="corticalprecision_section"),
            Layout(neuromodulatorsavg_panel, name="neuromodulatorsavg_section")
        )
        
        # Create right column
        cascadeprocessing_panel = self.create_cascadeprocessing_monitor(self.current_data)
        memoryandplasticity_panel = self.create_memoryandplasticity_monitor(self.current_data)
        cortexactivity_panel = self.create_cortexactivity_monitor(self.current_data)
        
        # Update right column with split_column
        self.layout["right_column"].split_column(
            Layout(cascadeprocessing_panel, name="cascadeprocessing_section"),
            Layout(memoryandplasticity_panel, name="memoryandplasticity_section"),
            Layout(cortexactivity_panel, name="cortexactivity_section")
        )
        
        # Create sensory inputs section
        sensoryinputs_panel = self.create_sensoryinputs_section()
        self.layout["interactive"].update(sensoryinputs_panel)
        
        return self.layout
    
    def run(self):
        """Run the dashboard with live updates"""
        self.is_running = True
        self.start_input_thread()
        
        try:
            with Live(self.render_dashboard(), refresh_per_second=10, screen=True) as live:
                while self.is_running:
                    # Update and refresh
                    live.update(self.render_dashboard())
                    time.sleep(self.config.refresh_rate)
                    
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the dashboard"""
        self.is_running = False
        self.stop_input_thread()
        self.console.print("\n[bold green]aNA - Dashboard: stopped.[/bold green]")


def create_dashboard() -> NeuralDashboard:
    """Create a configured neural dashboard instance"""
    config = DashboardConfig(
        refresh_rate=0.1,  # 10 FPS
        max_history=100
    )
    
    return NeuralDashboard(config)


if __name__ == "__main__":
    # Demo the dashboard
    dashboard = create_dashboard()

    dashboard.run()