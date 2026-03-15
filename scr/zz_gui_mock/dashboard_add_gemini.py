#!/usr/bin/env python3
# -*- coding: utf-8 -*-


    def create_sensoryinputs_section(self) -> Panel:
        """
        Antidote v1.0 : Nettoyage du buffer et alignement des entrées sensorielles.
        Gère l'affichage sans dédoublement.
        """
        # On utilise une grille invisible pour un contrôle total du placement
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        
        # Récupération des données (sera branché sur InputGateway demain)
        input_char = getattr(self, 'current_input', 'IDLE')
        accuracy = getattr(self, 'current_accuracy', 0.0)
        proc_time = getattr(self, 'current_proc_time', 0.0)

        # Ligne 1 : Keyboard Input & Metrics
        grid.add_row(
            Text.assemble(
                (" ⌨️  KEYBOARD: ", "bold cyan"), (f"'{input_char}'", "yellow"),
                ("  |  🎯 ACCURACY: ", "bold cyan"), (f"{accuracy:.1%}", "green" if accuracy > 0.8 else "red"),
                ("  |  ⏱️  TIME: ", "bold cyan"), (f"{proc_time:.2f}ms", "magenta")
            )
        )
    
        # Ligne 2 : Placeholders pour le futur (Micro/Caméra)
        grid.add_row(
            Text.assemble(
                ("\n 🎤  AUDIO: ", "dim white"), ("OFFLINE", "dim red"),
                ("  |  📷  VISION: ", "dim white"), ("OFFLINE", "dim red")
            )
        )

        return Panel(
            grid,
            title="[bold #666666]⌨️ Sensory Inputs[/bold #666666]",
            border_style="#666666",
            box=box.ROUNDED,
            padding=(0, 1)
        )