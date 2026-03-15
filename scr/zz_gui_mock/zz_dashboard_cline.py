#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neural Dashboard for aNA v5.0

This module implements a rich-based terminal dashboard inspired by "btop"
for real-time monitoring of the neural architecture.

Features:
- Fixed layout with non-scrolling interface
- Real-time neural activity monitoring
- Bio-inspired color coding
- Thalamic pulse visualization
- Precision loss sparkline
- Non-blocking input system

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Cline
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
import numpy as np


@dataclass
class DashboardConfig:
    """Configuration for the neural dashboard"""
    refresh_rate: float = 0.1  # 10 FPS (0.1 seconds)
    max_history: int = 100     # Maximum history points for sparkline
    pulse_interval: float = 1.0  # Thalamic pulse every 1 second


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
    
    def get_sparkline_data(self, data_type: str) -> List[float]:
        """Get data for sparkline visualization"""
        if data_type == "precision":
            return self.precision_history
        elif data_type == "energy":
            return self.energy_history
        elif data_type == "stress":
            return self.stress_history
        elif data_type == "thalamic":
            return self.thalamic_history
        return []


class ThalamicPulse:
    """Manages the biological thalamic pulse visualization"""
    
    def __init__(self, interval: float = 1.0):
        self.interval = interval
        self.last_pulse = time.time()
        self.is_pulsing = False
        self.pulse_phase = 0.0
    
    def update(self):
        """Update pulse state"""
        current_time = time.time()
        time_since_pulse = current_time - self.last_pulse
        
        if time_since_pulse >= self.interval:
            self.is_pulsing = True
            self.pulse_phase = 0.0
            self.last_pulse = current_time
        else:
            self.is_pulsing = False
            self.pulse_phase = time_since_pulse / self.interval
    
    def get_pulse_indicator(self) -> str:
        """Get visual pulse indicator"""
        if self.is_pulsing:
            return "•"  # Flashing dot
        else:
            return "◦"  # Dim dot


class NeuralDashboard:
    """
    Main dashboard class for aNA v5.0 neural monitoring
    
    Provides a rich-based terminal interface with:
    - Real-time brain activity monitoring
    - Neuromodulator level visualization
    - Processing pipeline status
    - Interactive input/output system
    """
    
    def __init__(self, config: Optional[DashboardConfig] = None):
        self.config = config or DashboardConfig()
        self.console = Console()
        self.layout = Layout()
        self.history = NeuralHistory(self.config.max_history)
        self.thalamic_pulse = ThalamicPulse(self.config.pulse_interval)
        
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
        """Setup the dashboard layout structure"""
        # Main layout structure
        self.layout.split_column(
            Layout(name="header", size=16),      # ASCII header
            Layout(name="dashboard", ratio=6),  # Main monitoring area
            Layout(name="interactive", size=8) # Input/output area
        )
        
        # Dashboard split into two columns
        self.layout["dashboard"].split_row(
            Layout(name="left_column", ratio=1),
            Layout(name="right_column", ratio=1)
        )
        
        # Left column: Processing pipeline
        self.layout["left_column"].split_column(
            Layout(name="thalamic_section", size=12),
            Layout(name="cortical_section", size=6),
            Layout(name="processing_section", size=6)
        )
        
        # Right column: System monitoring
        self.layout["right_column"].split_column(
            Layout(name="neuromodulator_section", size=12),
            Layout(name="system_section", size=6),
            Layout(name="memory_section", size=6)
        )
    
    def get_status_color(self, value: float, threshold_normal: float = 0.6, threshold_stress: float = 0.8) -> str:
        """Get color based on bio-inspired thresholds"""
        if value <= threshold_normal:
            return ColorScheme.NORMAL
        elif value <= threshold_stress:
            return ColorScheme.FATIGUE
        else:
            return ColorScheme.STRESS
    
    def create_ascii_header(self) -> Panel:
        """Create the 3D wireframe ASCII header"""
        header_text = """
##%%%###%#%%%%%%##%%#(%%%%(#%&%%%%#((((((((########(/((###((((/,/(((/*%%%%&%%&%%#&%%%%&&&&&&&&&&&&&&&&&&&&&&%%&&&&&&&%&%%&&&&&%%&%%%%%&%%%%&&&%&&%&%%%&&%%%&%%%%%%%%%%%%%%%%%%%
####%%##%%%%%##%%#%%#(%%%%%%%%##(/***,,,*,,,.,(###%%##(##%%#####%%#/((/,%%%%%%%%%%%%%%%%%%&&&&&&&&&%&%&%%%&&&%%%%&&%%%%%%%%%&%%%%%%%%%%%%%%%%%&&&%&&&%%%%%%%%%%%%%#%###/##%#(((
####%%%%#%#%%%#####%%%%%%%###((//***,,**,,,..../#(%%%%%##(##(//(#%%%%###(*,..#%%%%%%%%%%%%%%%%%&&&&%%%%%%%&&%%%%%%%%%%%%%%%%%%%%%%#%%%%%&%%%%%%%&%&&&%%%%%%%((####%#%########((
#########%%%%%%%%%%###%#####((****,,.,.,........//(#%%%%%##((.,*//(.######/#(***,/#%(%%%%%%&%%&%%&%%&%%%%%%%%%%&%%%%%%%%%%%%%%%%%%%%%%%%%%#(##%%%%%#%#######%%#%%##########(((/
(#((((((#(###########%###((/**,,,,,,,...../%%%&%%//(/((%%%%%#(*..*...,,,...*(((%#,.#%%%%%%%%%%%&%&%&%%%%%&%&&%%%%&%%%%%%%/((#(#(####%%####%%%#%%##########%%%%%######(((//**/**
(((///((((##(####((/(//******,,,,,,..../#%%%#%%%%%%%,/,((####///,%%.,...,...,..,/##*,%%%%%&%%&&&&%(((((&%%%&&%&%/%%#%###%%%##%#(#%%%#(/,***/***//((#######%%######(((#(((#####(
/////((((((((((//**,,*,,,,,,,,*,.....%%%%%%%%%#%%%%%%%%%%%%**(###/*  ,.#,.. .,, (&/(*.%%%%(###(##(*,(#((//%%%%#/((((*(##%#####(/*.,,*(/**,,****//(/###########%#%%%#%%%%%####(#
(#((##(((((((/****,,,.,,,,,,,,,.,,%#%%%%%%%&#%%%%%%%%%%%&%%%%&%%/(((/*.%&%., ,,. %%,//,%%%%..,..%##&%%..../((/%(,,*%%%##(%%%#(*.,....,,/(/(/(//////((((((((###((#########(#((/*
#(#(##((((///*,*,,,,,,,...,,..&%%%%%%%%%%%%%&%%%%%%%%%%%%%%%%%%&&%.*,(#/,%%&. .. %%%%%%%%%%%%%%%%&%%%&%%%%%(..*.%%%#(/*,(#((/*,.....,**,,,,,,*/**,.,*,,,,**/*****///*//////*/*,
(((((//(/**,,,,,,,,,,,,.*%&&%&&%&%%%%%%%&%%%%%%%%&&%%%%%%&%&&%%%%#**%,/,%%&&,.*,.#&%&&%%%%&%%%%%&%&&%%%%&%(#%(%##/*,,,,,**,,,.,,...,. .....,,,,..,,,*,,,,,..,...,,,,,,,,,,,.,,,
/*******,,,,,......,%%%%&%%%&%%%%&%%&%%%%%%%%%%%%&&%%%&&&&&%%%%%&%%&%%&&%&%%%&%%&%%%%%%%%%%%&%%%%%%%%%(#%#((***,./##(/.,......... .,#%%%%%%%## ., .,,.,,,,,,,,....,.,..,.......
,,**,,,,,,,,,,...%%%%%%%%%%%&%%%&%%&%%&%&%%%%%%%&&%&&&%&%%&&%%&%%&&&&&&%&&%%%%%%&%%%%%%%%%%%%%%%%%%%#%%.(**,./((*,.*(((*,//* ..,%%%%%%%%%%#%#,(%##%#/#/#%%%#%##%%##, .. . .  . 
,,.........,%%%#%%%%%%&%%%%%%%%%&&%&%%%%%&%%%%%%&%&%%&&&%&&&&%%&%%%%&%%%&%&%%%&&%#%%#%%%%%%%%%%%#%%%%%%#(/,.(/...%(#(, ,(%(%%%%%%&%%%%%%#%#%#%#(%###%%###%%%%%#%%#####(#((/*(*#
..*(###%##%#%%%%%#%%%%%%%&&%&%%%&&%%%%%%%%&&&%%%&&%%%%%%%%&%&%%&&&&&&&&&&&&%&%%%&&&%%%%%%%%%%%%%%%%%%%%/*.,/(*,%%(/*. #%%%%%%%&&%%%%%%%%%%#%###%%%%%%#%%%%%%%%%%%%#%#####(#(/(/
#####(###%%%%%%%%%%%%%%%%&%&%&&&&%%%%%&%&%&&&&%&%%%%%%%%&%%%%(%%%%%%%%&&%&%%%%&%&%%%%%%%%%%%%%%%(%%%%%%%(*,(*,%%%#((*/%&&&&%%%&&&%%%%%%%%%%%#/%%%%%%%%%%%%%%%%%%%%##%#%#(((/((/
######%%##%%%%&%%%%%%%&%%&&&&%&%&&&&&&%%&%&%%%%%%&%%%&%%&%%%&%%%%%%%%%%%%%%%&%&%%%%%#%%%%%%%%%&%&%%%%%%&(,.*,(%%%%((%%%%%%%%%%%%%%%%&%%&&%###(%%%%%%%%%%%%%#%###%%%##%#(###((((
        """.strip()
        
        return Panel(
            header_text,
            title="[bold #cccccc]🧠 aNA v5.0 NEURAL DASHBOARD[/bold #cccccc]",
            border_style="#cccccc"
        )
    
    def create_thalamic_monitor(self, data: Dict[str, Any]) -> Panel:
        """Create thalamic activity monitor with pulse"""
        self.thalamic_pulse.update()
        pulse_indicator = self.thalamic_pulse.get_pulse_indicator()
        
        # Get thalamic data
        thalamic_activity = data.get('thalamic_activity', 0.0)
        baseline = data.get('thalamic_baseline', 0.15)
        
        # Create progress bar
        progress = Progress(
            TextColumn("[bold cyan]Thalamus[/bold cyan]"),
            BarColumn(bar_width=None, complete_style=ColorScheme.THALAMUS),
            TextColumn(f"{thalamic_activity:.1%}"),
            expand=True
        )
        
        progress.add_task("", total=1.0, completed=thalamic_activity)
        
        # Status text with pulse
        status_color = self.get_status_color(thalamic_activity)
        status_text = Text(f"Status: {pulse_indicator} ", style=status_color)
        status_text.append(f"Baseline: {baseline:.2f}", style="dim")
        
        content = f"{progress}\n{status_text}"
        
        return Panel(
            content,
            title="[bold cyan]⚡ THALAMIC ACTIVITY[/bold cyan]",
            border_style="cyan"
        )
    
    def create_cortical_monitor(self, data: Dict[str, Any]) -> Panel:
        """Create 6-layer cortical cascade monitor"""
        # Get cortical layer data
        l4_output = data.get('l4_output', 0.0)
        l23_output = data.get('l23_output', 0.0)
        l5_output = data.get('l5_output', 0.0)
        precision_loss = data.get('precision_loss', 0.0)
        attention_boost = data.get('attention_boost', 1.0)
        
        # Create cascade visualization
        cascade_table = Table.grid(padding=1)
        cascade_table.add_column(justify="left", width=15)
        cascade_table.add_column(justify="right", width=10)
        
        # Layer IV (Input)
        l4_color = self.get_status_color(l4_output)
        cascade_table.add_row(
            f"Layer IV (Input):",
            f"[{l4_color}]{l4_output:.3f}[/{l4_color}]"
        )
        
        # Layer II/III (Association)
        l23_color = self.get_status_color(l23_output)
        cascade_table.add_row(
            f"Layer II/III (Assoc):",
            f"[{l23_color}]{l23_output:.3f}[/{l23_color}]"
        )
        
        # Layer V (Output)
        l5_color = self.get_status_color(l5_output)
        cascade_table.add_row(
            f"Layer V (Output):",
            f"[{l5_color}]{l5_output:.3f}[/{l5_color}]"
        )
        
        # Precision monitoring
        precision_color = self.get_status_color(precision_loss, 0.1, 0.3)
        cascade_table.add_row(
            f"Precision Loss:",
            f"[{precision_color}]{precision_loss:.3f}[/{precision_color}]"
        )
        
        # Attention boost
        attention_text = f"Attention: {attention_boost:.2f}x"
        
        content = f"{cascade_table}\n{attention_text}"
        
        return Panel(
            content,
            title="[bold blue]🔬 CORTICAL CASCADE[/bold blue]",
            border_style="blue"
        )
    
    def create_processing_monitor(self, data: Dict[str, Any]) -> Panel:
        """Create current processing status monitor"""
        input_char = data.get('input_character', '?')
        output_char = data.get('output_character', '?')
        accuracy = data.get('accuracy', 0.0)
        processing_time = data.get('processing_time_ms', 0.0)
        
        # Status indicators
        accuracy_color = self.get_status_color(accuracy, 0.8, 0.95)
        status_emoji = "✅" if accuracy > 0.8 else "⚠️" if accuracy > 0.5 else "❌"
        
        content = f"""
[bold]Current Processing:[/bold]
Input:  '{input_char}' → Output: '{output_char}'
Accuracy: [{accuracy_color}]{accuracy:.1%}[/{accuracy_color}] {status_emoji}
Time: {processing_time:.1f}ms
        """.strip()
        
        return Panel(
            content,
            title="[bold yellow]📊 PROCESSING STATUS[/bold yellow]",
            border_style="yellow"
        )
    
    def create_neuromodulator_monitor(self, data: Dict[str, Any]) -> Panel:
        """Create neuromodulator level visualization"""
        neuromodulators = data.get('neuromodulators', {})
        
        # Create progress bars for each neuromodulator
        progress = Progress(
            TextColumn("[bold]Neuromodulators:[/bold]"),
            BarColumn(bar_width=20),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            expand=True
        )
        
        # Add tasks for each neuromodulator
        modulator_tasks = {}
        for modulator, level in neuromodulators.items():
            color = getattr(ColorScheme, modulator.upper(), "white")
            task_id = progress.add_task(
                f"[{color}]{modulator.title()}[/{color}]:",
                total=1.0,
                completed=level,
                color=color
            )
            modulator_tasks[modulator] = task_id
        
        return Panel(
            progress,
            title="[bold magenta]🧪 NEUROMODULATOR LEVELS[/bold magenta]",
            border_style="magenta"
        )
    
    def create_system_monitor(self, data: Dict[str, Any]) -> Panel:
        """Create system-wide monitoring"""
        energy = data.get('energy_level', 1.0)
        stress = data.get('stress_level', 0.0)
        adrenaline = data.get('adrenaline_level', 0.0)
        
        # Create system status table
        system_table = Table.grid(padding=1)
        system_table.add_column(justify="left", width=12)
        system_table.add_column(justify="right", width=15)
        
        # Energy level
        energy_color = self.get_status_color(1.0 - energy, 0.3, 0.6)  # Invert for energy
        system_table.add_row(
            "Energy:",
            f"[{energy_color}]{energy:.1%}[/{energy_color}]"
        )
        
        # Stress level
        stress_color = self.get_status_color(stress)
        system_table.add_row(
            "Stress:",
            f"[{stress_color}]{stress:.1%}[/{stress_color}]"
        )
        
        # Adrenaline level
        adrenaline_color = self.get_status_color(adrenaline)
        system_table.add_row(
            "Adrenaline:",
            f"[{adrenaline_color}]{adrenaline:.1%}[/{adrenaline_color}]"
        )
        
        return Panel(
            system_table,
            title="[bold red]⚡ SYSTEM STATUS[/bold red]",
            border_style="red"
        )
    
    def create_memory_monitor(self, data: Dict[str, Any]) -> Panel:
        """Create hippocampal memory and consolidation monitor"""
        memory_strength = data.get('memory_strength', 0.0)
        consolidation_rate = data.get('consolidation_rate', 0.0)
        memory_traces = data.get('memory_traces', 0)
        
        # Create memory visualization
        memory_table = Table.grid(padding=1)
        memory_table.add_column(justify="left", width=15)
        memory_table.add_column(justify="right", width=10)
        
        # Memory strength
        memory_color = self.get_status_color(memory_strength)
        memory_table.add_row(
            "Memory Strength:",
            f"[{memory_color}]{memory_strength:.1%}[/{memory_color}]"
        )
        
        # Consolidation rate
        consolidation_color = self.get_status_color(consolidation_rate)
        memory_table.add_row(
            "Consolidation:",
            f"[{consolidation_color}]{consolidation_rate:.1%}[/{consolidation_color}]"
        )
        
        # Memory traces
        traces_text = f"Traces: {memory_traces}"
        
        content = f"{memory_table}\n{traces_text}"
        
        return Panel(
            content,
            title="[bold purple]🧠 HIPPOCAMPAL STATE[/bold purple]",
            border_style="purple"
        )
    
    def create_sparkline(self, data: List[float], title: str, color: str) -> str:
        """Create a simple sparkline visualization"""
        if not data:
            return f"[{color}]{title}: No data[/{color}]"
        
        # Normalize data to 0-1 range for sparkline
        min_val = min(data)
        max_val = max(data)
        
        if max_val == min_val:
            normalized = [0.5] * len(data)
        else:
            normalized = [(x - min_val) / (max_val - min_val) for x in data]
        
        # Create sparkline characters
        sparkline_chars = "▁▂▃▄▅▆▇█"
        sparkline_data = ""
        
        for val in normalized[-20:]:  # Show last 20 points
            index = int(val * (len(sparkline_chars) - 1))
            sparkline_data += sparkline_chars[index]
        
        current_val = data[-1] if data else 0.0
        return f"[{color}]{title}: {sparkline_data} {current_val:.2f}[/{color}]"
    
    def create_interactive_section(self) -> Panel:
        """Create the interactive input/output section"""
        # Input buffer display
        input_text = " ".join(self.input_buffer[-10:]) if self.input_buffer else "No input"
        
        # Output buffer display
        output_text = " ".join(self.output_buffer[-10:]) if self.output_buffer else "No output"
        
        content = f"""
[bold]Input Buffer:[/bold] {input_text}
[bold]Output Buffer:[/bold] {output_text}

[italic dim]Type characters to process (Ctrl+C to exit)[/italic dim]
        """.strip()
        
        return Panel(
            content,
            title="[bold #808080]⌨️ INTERACTIVE ZONE[/bold #808080]",
            border_style="#808080",
            box=box.DOUBLE
        )
    
    def update_data(self, new_data: Dict[str, Any]):
        """Update dashboard with new neural data"""
        self.current_data = new_data
        
        # Add to history for sparklines
        precision = new_data.get('accuracy', 0.0)
        energy = new_data.get('energy_level', 1.0)
        stress = new_data.get('stress_level', 0.0)
        thalamic = new_data.get('thalamic_activity', 0.0)
        
        self.history.add_point(precision, energy, stress, thalamic)
    
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
        # Update thalamic pulse
        self.thalamic_pulse.update()
        
        # Create header
        self.layout["header"].update(self.create_ascii_header())
        
        # Create left column (Processing pipeline)
        thalamic_panel = self.create_thalamic_monitor(self.current_data)
        cortical_panel = self.create_cortical_monitor(self.current_data)
        processing_panel = self.create_processing_monitor(self.current_data)
        
        # Update left column with split_column
        self.layout["left_column"].split_column(
            Layout(thalamic_panel, name="thalamic_section"),
            Layout(cortical_panel, name="cortical_section"),
            Layout(processing_panel, name="processing_section")
        )
        
        # Create right column (System monitoring)
        neuromodulator_panel = self.create_neuromodulator_monitor(self.current_data)
        system_panel = self.create_system_monitor(self.current_data)
        memory_panel = self.create_memory_monitor(self.current_data)
        
        # Update right column with split_column
        self.layout["right_column"].split_column(
            Layout(neuromodulator_panel, name="neuromodulator_section"),
            Layout(system_panel, name="system_section"),
            Layout(memory_panel, name="memory_section")
        )
        
        # Create interactive section
        interactive_panel = self.create_interactive_section()
        self.layout["interactive"].update(interactive_panel)
        
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
        self.console.print("\n[bold green]Dashboard stopped.[/bold green]")


def create_dashboard() -> NeuralDashboard:
    """Create a configured neural dashboard instance"""
    config = DashboardConfig(
        refresh_rate=0.1,  # 10 FPS
        max_history=100,
        pulse_interval=1.0
    )
    
    return NeuralDashboard(config)


if __name__ == "__main__":
    # Demo the dashboard
    dashboard = create_dashboard()
    
    # Simulate some data
    test_data = {
        'thalamic_activity': 0.75,
        'thalamic_baseline': 0.15,
        'l4_output': 0.68,
        'l23_output': 0.61,
        'l5_output': 0.55,
        'precision_loss': 0.12,
        'attention_boost': 1.25,
        'input_character': 'A',
        'output_character': 'A',
        'accuracy': 0.92,
        'processing_time_ms': 15.2,
        'neuromodulators': {
            'dopamine': 0.85,
            'acetylcholine': 0.72,
            'serotonin': 0.68,
            'norepinephrine': 0.45,
            'no_gas': 0.35
        },
        'energy_level': 0.85,
        'stress_level': 0.25,
        'adrenaline_level': 0.30,
        'memory_strength': 0.65,
        'consolidation_rate': 0.45,
        'memory_traces': 12
    }
    
    dashboard.update_data(test_data)
    dashboard.run()