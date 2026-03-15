#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hippocampus v5.0 - Version Intégrable

This module implements a simplified hippocampus for aNA v5.0 with:
- Pattern learning and memory consolidation
- Transition-based prediction (A -> B)
- Simple dictionary-based memory storage (L1/L2/L3)
- Integration-ready design for Thalamus connection

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline and GPT
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum


class HippocampalRegion(Enum):
    """Hippocampal subregions"""
    DENTATE_GYRUS = "DG"      # Pattern separation
    CA4 = "CA4"               # Hilus, mossy cells
    CA3 = "CA3"               # Autoassociative memory
    CA2 = "CA2"               # Social memory
    CA1 = "CA1"               # Output to cortex
    SUBICULUM = "SUB"         # Final output stage


class Hippocampus:
    """
    Simplified Hippocampus for aNA v5.0 integration.
    
    This version uses a simple dictionary-based structure for memory storage
    and focuses on pattern learning and transition-based prediction.
    """
    
    # Memory thresholds for consolidation
    L1_TO_L2_THRESHOLD = 1    # Nombre d'apparitions pour passer en L2
    L2_TO_L3_THRESHOLD = 3    # Nombre d'apparitions pour passer en L3
    L3_REINFORCEMENT_THRESHOLD = 5  # Nombre d'apparitions pour renforcement L3
    
    def __init__(self, position: np.ndarray = np.array([10.0, -30.0, 0.0])):
        self.position = position
        
        # Structure de données simple pour la mémoire
        self.memory_store = {
            'L1': {},  # Court terme (volatile)
            'L2': {},  # Court terme (renforcé)
            'L3': {}   # Long terme (consolidé)
        }
        
        # Compteurs pour le renforcement
        self.pattern_counts = {}
        
        # Structure pour les transitions (A -> B)
        self.transitions = {}
        self.last_item = None
        
        print("🧠 Hippocampus v5.0 initialized")
        print(f"📍 Position: {position}")
        print(f"📊 Memory thresholds: L1→L2 after {self.L1_TO_L2_THRESHOLD} reps, L2→L3 after {self.L2_TO_L3_THRESHOLD} reps")
    
    def encode(self, signal: str, importance: float = 1.0) -> None:
        """
        Encode a signal into memory.
        
        Args:
            signal: The signal to encode (ex: "A", "B", "HELLO")
            importance: Importance factor (0.0 to 1.0)
        """
        # Stockage immédiat en L1
        if signal not in self.memory_store['L1']:
            self.memory_store['L1'][signal] = 0
        
        self.memory_store['L1'][signal] += importance
        
        # Compter les apparitions pour le renforcement
        if signal not in self.pattern_counts:
            self.pattern_counts[signal] = 0
        self.pattern_counts[signal] += 1
        
        # Enregistrer la transition si on a un item précédent
        if self.last_item is not None:
            if self.last_item not in self.transitions:
                self.transitions[self.last_item] = {}
            
            if signal not in self.transitions[self.last_item]:
                self.transitions[self.last_item][signal] = 0
            
            self.transitions[self.last_item][signal] += 1
        
        # Mettre à jour le dernier item
        self.last_item = signal
    
    def consolidate(self) -> None:
        """
        Consolidation routine - moves patterns from L1 to L2/L3.
        
        This method is called periodically to simulate reinforcement.
        """
        signals_to_move = []
        
        # Vérifier les signals en L1 pour passage en L2
        for signal, count in self.pattern_counts.items():
            if signal in self.memory_store['L1']:
                if count >= self.L1_TO_L2_THRESHOLD and count < self.L2_TO_L3_THRESHOLD:
                    # Déplacer en L2
                    signals_to_move.append((signal, 'L2'))
        
        # Vérifier les signals en L2 pour passage en L3
        for signal, count in self.pattern_counts.items():
            if signal in self.memory_store['L2']:
                if count >= self.L2_TO_L3_THRESHOLD and count < self.L3_REINFORCEMENT_THRESHOLD:
                    # Déplacer en L3
                    signals_to_move.append((signal, 'L3'))
                elif count >= self.L3_REINFORCEMENT_THRESHOLD:
                    # Renforcer en L3
                    pass  # Already in L3, just reinforce
        
        # Effectuer les déplacements
        for signal, target_level in signals_to_move:
            if signal in self.memory_store['L1']:
                # Déplacer de L1 vers L2
                value = self.memory_store['L1'].pop(signal)
                self.memory_store['L2'][signal] = value
            elif signal in self.memory_store['L2']:
                # Déplacer de L2 vers L3
                value = self.memory_store['L2'].pop(signal)
                self.memory_store['L3'][signal] = value
    
    def retrieve(self, context: str) -> str:
        """
        Retrieve a prediction based on context.
        
        Args:
            context: The context query (ex: "A" to predict what follows)
            
        Returns:
            The most probable prediction, or "?" if nothing found
        """
        # D'abord chercher dans les transitions
        if context in self.transitions:
            # Trouver la transition la plus fréquente
            best_next = "?"
            best_count = 0
            
            for next_signal, count in self.transitions[context].items():
                if count > best_count:
                    best_count = count
                    best_next = next_signal
            
            if best_next != "?":
                return best_next
        
        # Si aucune transition trouvée, chercher dans la mémoire traditionnelle
        best_prediction = "?"
        best_score = 0
        
        # Chercher dans L3 (mémoire à long terme)
        for signal in self.memory_store['L3']:
            if signal.startswith(context):
                score = self.memory_store['L3'][signal]
                if score > best_score:
                    best_score = score
                    best_prediction = signal
        
        # Si rien en L3, chercher dans L2
        if best_prediction == "?":
            for signal in self.memory_store['L2']:
                if signal.startswith(context):
                    score = self.memory_store['L2'][signal]
                    if score > best_score:
                        best_score = score
                        best_prediction = signal
        
        # Si rien en L2/L3, chercher dans L1
        if best_prediction == "?":
            for signal in self.memory_store['L1']:
                if signal.startswith(context):
                    score = self.memory_store['L1'][signal]
                    if score > best_score:
                        best_score = score
                        best_prediction = signal
        
        return best_prediction
    
    def get_outputs(self) -> Dict[str, Any]:
        """Get outputs from all regions"""
        return {
            'memory_status': {
                'L1_count': len(self.memory_store['L1']),
                'L2_count': len(self.memory_store['L2']),
                'L3_count': len(self.memory_store['L3']),
                'total_patterns': len(self.pattern_counts),
                'transitions_count': len(self.transitions)
            },
            'current_prediction': self.last_item,
            'transitions': self.transitions.copy(),
            'pattern_counts': self.pattern_counts.copy()
        }
    
    def reset(self):
        """Reset the hippocampus"""
        self.memory_store = {'L1': {}, 'L2': {}, 'L3': {}}
        self.pattern_counts = {}
        self.transitions = {}
        self.last_item = None
        print("🔄 Hippocampus reset")


def test_integration():
    """
    Test function to verify integration with Thalamus.
    
    This simulates the flow: Thalamus -> Hippocampus -> Thalamus
    """
    print("\n🧪 INTEGRATION TEST: Thalamus ↔ Hippocampus")
    print("=" * 60)
    
    # Create hippocampus
    hippo = Hippocampus()
    
    # Simulate sequence from Thalamus
    sequence = ["A", "B", "A", "B", "A", "B"]
    
    print(f"📚 Sequence from Thalamus: {sequence}")
    print()
    
    # Phase 1: Learning
    print("📝 PHASE 1: Learning from Thalamus")
    print("-" * 40)
    
    for i, signal in enumerate(sequence):
        print(f"Tour {i+1}: Thalamus → Hippocampus: '{signal}'")
        hippo.encode(signal, importance=1.0)
        hippo.consolidate()
        
        # Get hippocampus outputs
        outputs = hippo.get_outputs()
        print(f"   Hippocampus → Thalamus: Memory L1={outputs['memory_status']['L1_count']}, L2={outputs['memory_status']['L2_count']}, L3={outputs['memory_status']['L3_count']}")
        print()
    
    # Phase 2: Prediction
    print("🔍 PHASE 2: Prediction for Thalamus")
    print("-" * 40)
    
    # Test prediction after "A"
    context = "A"
    prediction = hippo.retrieve(context)
    
    print(f"❓ Thalamus query: 'What follows {context}?'")
    print(f"🧠 Hippocampus response: '{prediction}'")
    
    # Verify success
    expected = "B"
    success = prediction == expected
    
    print(f"✅ Success: {success}")
    
    # Phase 3: Error Calculation (Free Energy)
    print("\n📊 PHASE 3: Error Calculation (Free Energy)")
    print("-" * 45)
    
    # Simulate reality check
    reality = "B"  # What actually happens
    prediction_error = abs(ord(prediction) - ord(reality)) if prediction != "?" else 1.0
    
    print(f"Reality: '{reality}'")
    print(f"Prediction: '{prediction}'")
    print(f"Prediction Error: {prediction_error}")
    
    # This error can be used by Amygdala for stress response
    if prediction_error > 0:
        print("⚠️  High prediction error → Amygdala stress response")
    else:
        print("✅ Perfect prediction → Amygdala calm")
    
    # Final status
    print(f"\n🏁 INTEGRATION STATUS:")
    print("=" * 25)
    if success:
        print("✅ INTEGRATION SUCCESSFUL")
        print("   - Hippocampus learns patterns correctly")
        print("   - Prediction works as expected")
        print("   - Error calculation ready for Amygdala")
        print("   - Ready for Thalamus integration")
    else:
        print("❌ INTEGRATION FAILED")
        print("   - Check encoding logic")
        print("   - Check prediction algorithm")
        print("   - Check transition storage")
    
    return success


if __name__ == "__main__":
    # Run integration test
    success = test_integration()
    
    print(f"\n🏁 FINAL STATUS: {'HIPPOCAMPE READY FOR THALAMUS INTEGRATION' if success else 'HIPPOCAMPE NEEDS ADJUSTMENTS'}")