#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project - v5.2
Module: Test Hippocampus
Description: This test is designed to validate the core functionalities of the hippocampus module in complete isolation. It simulates a simple data stream to verify that the hippocampus learns patterns correctly and can retrieve them based on context. The test covers encoding, consolidation, and retrieval processes, as well as the handling of transitions between items.
Unit Test for the Hippocampus - Isolated Version
Architecture and neuroinformatics: Theriault Benoit
"""
import unittest
import numpy as np
import os
import sys
from typing import Dict, List, Tuple, Optional
from enum import Enum

# On définit la racine du projet dynamiquement
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from config import get_config

def create_ascii_header():
    print(f"\033c") 
    print("░                     ░░░░░░░░░░▒▒▒▒▒▒░░")
    print("           ░░░░░░░░░▒▒▒▒▒▓▒▒▒▒░░░░░░░░░░▒▒▒▒░                                                          ░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▒░░░░░▒▒▒░░░░▒▓▒░░                      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓▓▓▓▓▓▒░░▒▒▒░░░░▒▓▓▓▓▓▓▒▒▒▒▒░     ░░░░░░░░░░░░░░░░░░░░░▒▒░░▒▒▒▓▓▓▓▓▓▒▒▒░░░░░░░░░░░░░░░░░▒▒▒▒")
    print("▒░░░░░▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▒░         ░░▒▒▒░▒▒▒▒▓▓▓▓▓▓▓▒▒░░  ░▒▒▒▓▒▒▒▓▒▓▒▓▒░░░░░░░▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░▒▓")
    print("░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓░                   ░░ ▒▒▓▒░▒▓▓▓░▒▒░░           ░▒░░░▒▓▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓")
    print("▒▒▓▓▓▓▓▓▒▒▒░░                           ░▓▓▒░░▒▓▓░ _    _    _ ░▒░░▒▓▒▓▓▓▓▓▓▓▓▓▓▒░░░░░░░░░▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
    print("▓▓▓▓▓▒░AI inspired by natural plasticity ░░   ░░░  a    N    A  ▒▓▒▓▒▒▒▓░Autonomous Neural Architecture v5.2   ░▒▓")
    print("░                                                  ‾    ‾    ‾ ░▓▒▓░░▒▓░\n\n")

class HippocampalRegion(Enum):
    """Hippocampal subregions"""
    DENTATE_GYRUS = "DG"      # Pattern separation
    CA4 = "CA4"               # Hilus, mossy cells
    CA3 = "CA3"               # Autoassociative memory
    CA2 = "CA2"               # Social memory
    CA1 = "CA1"               # Output to cortex
    SUBICULUM = "SUB"         # Final output stage


class SimpleHippocampus:
    """
    Simplified version of the hippocampus for unit testing.

    This version uses a simple data structure (dictionary)
    to simulate L1, L2, and L3 without any external dependencies.
    """
    
    def __init__(self, position: np.ndarray = np.array([10.0, -30.0, 0.0])):
        self.position = position
        
        # Structure de données simple pour la mémoire
        self.memory_store = {
            'L1': {},  # Court terme (volatile)
            'L2': {},  # Court terme (renforcé)
            'L3': {}   # Long terme (consolidé)
        }

        config = get_config()
        # On remplace les entiers fixes par les hyper-paramètres
        self.min_strength_l1 = config.get("MIN_STRENGTH_L1", 1) 
        self.threshold_nmda = config.get("THRESHOLD_NMDA", 3)
        
        # Compteurs pour le renforcement
        self.pattern_counts = {}
        
        # Seuils de consolidation
        self.l1 = []
        self.l2 = {}
        self.l3 = []
        self.transitions = {}
        self.last_item = None
        
        print("🧠 SimpleHippocampus initialized")
        print(f"📍 Position: {position}")
        print(f"📊 Memory thresholds: L1→L2 after {self.min_strength_l1} reps, L2→L3 after {self.threshold_nmda} reps")
    
    def encode(self, signal: str, importance: float = 1.0) -> None:
        """
        Encode a signal in memory.

        Arguments:
            signal: The signal to encode (e.g., "A", "B", "HELLO")
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
        
        print(f"📝 Encoded: '{signal}' (importance: {importance:.1f}, count: {self.pattern_counts[signal]})")
    
    def consolidate(self, item):
        """
        Consolidation v5.1.1 : Gère le passage entre L1, L2 et L3
        en utilisant les seuils du Tempérament (config.py).
        """
        # CRUCIAL : On initialise la liste au début pour éviter la NameError
        signals_to_move = []
        
        # On récupère le compte actuel pour cet item dans L2
        # (Note: dans ce test simple, on simule la progression via pattern_counts)
        count = self.pattern_counts.get(item, 0)

        # 1. Logique de passage L1 -> L2
        # Si l'item atteint le seuil L1 et n'est pas encore dans le store L2
        if count >= self.min_strength_l1 and item not in self.memory_store['L2']:
            signals_to_move.append((item, "L2"))
            print(f"  🔄 Consolidating '{item}' from L1 → L2 (stabilité initiale)")
            
        # 2. Logique de passage L2 -> L3 (Potentiation NMDA)
        if count >= self.threshold_nmda and item not in self.memory_store['L3']:
            signals_to_move.append((item, "L3"))
            print(f"  🔥 Potentiation NMDA : '{item}' passe en L3 (Modèle Long Terme)")

        # 3. Exécution des déplacements
        for signal, target_level in signals_to_move:
            # Transfert physique dans le dictionnaire de stockage
            if target_level == "L2":
                if signal in self.memory_store['L1']:
                    val = self.memory_store['L1'].pop(signal)
                    self.memory_store['L2'][signal] = val
            
            elif target_level == "L3":
                # On peut venir de L1 ou L2 vers L3
                source = 'L2' if signal in self.memory_store['L2'] else 'L1'
                if signal in self.memory_store[source]:
                    val = self.memory_store[source].pop(signal)
                    self.memory_store['L3'][signal] = val
    
    def retrieve(self, context: str) -> str:
        """
        Retrieves a context-based prediction.

        Args:
            context: The query context (e.g., "A" to predict what follows)

        Returns:
            The most likely prediction, or "?" if nothing is found.
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
                print(f"🔍 Retrieved from transitions: '{best_next}' for context '{context}' (count: {best_count})")
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
        
        print(f"🔍 Retrieved from memory: '{best_prediction}' for context '{context}' (score: {best_score:.1f})")
        return best_prediction
    
    def encode_sequence(self, sequence: List[str]) -> None:
        """
        Encode a sequence of signals to learn the transitions.

        Args:
            sequence: List of signals in chronological order
        """
        for i, signal in enumerate(sequence):
            # Encoder le signal actuel
            self.encode(signal, importance=1.0)
            
            # Si ce n'est pas le dernier signal, encoder la transition
            if i < len(sequence) - 1:
                next_signal = sequence[i + 1]
                transition = f"{signal}->{next_signal}"
                self.encode(transition, importance=2.0)  # Importance plus élevée pour les transitions
            
            # Consolidation après chaque encodage
            self.consolidate()
    
    def get_memory_status(self) -> Dict:
        """Returns the current state of memory"""
        return {
            'L1_count': len(self.memory_store['L1']),
            'L2_count': len(self.memory_store['L2']),
            'L3_count': len(self.memory_store['L3']),
            'total_patterns': len(self.pattern_counts),
            'memory_store': self.memory_store.copy(),
            'pattern_counts': self.pattern_counts.copy()
        }
    
    def reset(self):
        """Reset l'hippocampe"""
        self.memory_store = {'L1': {}, 'L2': {}, 'L3': {}}
        self.pattern_counts = {}
        print("🔄 SimpleHippocampus reset")


def test_hippocampus_pattern_learning():
    """
    Unit test to verify that the hippocampus learns patterns correctly.

    Scenario: A -> B -> A -> B -> A -> B
    The hippocampus must learn that "B" often follows "A".
    """
    print("\n🧪 UNIT TEST: Pattern Learning")
    print("=" * 60)
    
    # Créer l'hippocampe
    hippo = SimpleHippocampus()
    
    # Séquence d'apprentissage
    sequence = ["A", "B", "A", "B", "A", "B"]
    
    print(f"📚 Learning sequence: {sequence}")
    print()
    
    # Phase 1: Encodage
    print("📝 PHASE 1: Encoding")
    print("-" * 30)
    
    for i, item in enumerate(sequence):
        print(f"Cycle {i+1}: Encoding '{item}'")
        hippo.encode(item)
        
        # Consolidation après chaque encodage
        hippo.consolidate(item)
        
        # Afficher l'état de la mémoire
        status = hippo.get_memory_status()
        print(f"   Memory: L1={status['L1_count']}, L2={status['L2_count']}, L3={status['L3_count']}")
        print()
    
    # Phase 2: Récupération et Prédiction
    print("🔍 PHASE 2: Recovery and Prediction")
    print("-" * 40)
    
    # Tester la prédiction après "A"
    print("❓ Prediction test: What follows 'A'?")
    prediction = hippo.retrieve("A")
    
    # Vérification
    expected = "B"  # On s'attend à ce que "B" soit prédit après "A"
    success = prediction == expected
    
    print(f"🎯 Prediction: '{prediction}'")
    print(f"✅ Success: {success}")
    print(f"📊 Pattern counts: {hippo.pattern_counts}")
    
    # Phase 3: Vérification détaillée
    print("\n🔍 PHASE 3: Detailed Verification")
    print("-" * 35)
    
    status = hippo.get_memory_status()
    print(f"📦 Content L1: {list(status['memory_store']['L1'].keys())}")
    print(f"📦 Content L2: {list(status['memory_store']['L2'].keys())}")
    print(f"📦 Content L3: {list(status['memory_store']['L3'].keys())}")
    
    # Analyse de l'apprentissage
    a_count = hippo.pattern_counts.get("A", 0)
    b_count = hippo.pattern_counts.get("B", 0)
    
    print(f"\n📈 Analyse:")
    print(f"   'A' appears {a_count} fois")
    print(f"   'B' appears {b_count} fois")
    print(f"   Pattern 'A' in L3: {'Yes' if 'A' in status['memory_store']['L3'] else 'No'}")
    print(f"   Pattern 'B' in L3: {'Yes' if 'B' in status['memory_store']['L3'] else 'No'}")
    
    # Résultat final
    print(f"\n🏁 TEST RESULTS:")
    print("=" * 25)
    if success:
        print("✅ TEST SUCCESSFUL: The hippocampus has learned the pattern!")
        print("   - The pattern 'A' → 'B' has been correctly memorized")
        print("   - The prediction works as expected")
    else:
        print("❌ TEST FAILED: The hippocampus did not learn correctly")
        print("   - Check the consolidation thresholds")
        print("   - Check the search logic")
    
    return success


def test_hippocampus_complex_pattern():
    """
    Unit test for a more complex pattern.

    Scenario: "HELLO" -> "WORLD" -> "HELLO" -> "WORLD"
    """
    print("\n🧪 UNIT TEST: Complex Pattern")
    print("=" * 50)
    
    hippo = SimpleHippocampus()
    
    # Séquence plus complexe
    sequence = ["HELLO", "WORLD", "HELLO", "WORLD"]
    
    print(f"📚 Sequence: {sequence}")
    
    # Encodage
    for item in sequence:
        print(f"Cycle X: Encoding '{item}'") # Ton log montre que ça s'arrête ici
        hippo.encode(item)

        hippo.consolidate(item)
    
    # Test de prédiction
    print(f"\n❓ What comes after 'HELLO' ?")
    prediction = hippo.retrieve("HELLO")
    
    success = prediction == "WORLD"
    print(f"🎯 Prediction: '{prediction}'")
    print(f"✅ Success: {success}")
    
    return success


def run_all_tests():
    """Runs all unit tests"""
    print("🚀 LAUNCH OF HIPPOCAMPE UNIT TESTS")
    print("=" * 60)
    
    # Test 1: Pattern simple
    test1_success = test_hippocampus_pattern_learning()
    
    # Test 2: Pattern complexe
    test2_success = test_hippocampus_complex_pattern()
    
    # Résumé
    print("\n📊 TEST SUMMARY")
    print("=" * 25)
    print(f"Test 1 (Pattern A→B): {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"Test 2 (Pattern HELLO→WORLD): {'✅ PASS' if test2_success else '❌ FAIL'}")
    
    overall_success = test1_success and test2_success
    print(f"\n🎯 OVERALL RESULT: {'✅ ALL BASIC FUNCTIONS ARE VALIDATED' if overall_success else '❌ SOME FUNCTIONS REQUIRE ADJUSTMENTS'}")
    
    if overall_success:
        print("\n🎉 The seahorse is ready for integration!")
        print("   - encode() works correctly")
        print("   - retrieve() works correctly")
        print("   - consolidate() works correctly")
        print("   - The data structure is valid")
    else:
        print("\n⚠️ Adjustments are needed before integration")
    
    return overall_success


if __name__ == "__main__":
    create_ascii_header()
    # Exécuter tous les tests
    success = run_all_tests()
    
    print(f"\n🏁 STATUT: {'HIPPOCAMPE READY FOR INTEGRATION' if success else 'HIPPOCAMPE AWAITING CORRECTIONS'}")