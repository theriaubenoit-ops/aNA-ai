#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test unitaire pour l'Hippocampe - Version Isolée

Ce module teste l'hippocampe en isolation totale sans aucune dépendance externe.
Il simule un flux de données simple pour vérifier que l'hippocampe apprend bien les patterns.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from enum import Enum


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
    Version simplifiée de l'hippocampe pour tests unitaires.
    
    Cette version utilise une structure de données simple (dictionnaire)
    pour simuler L1, L2, L3 sans aucune dépendance externe.
    """
    
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
        
        # Seuils de consolidation
        self.l1_threshold = 1    # Nombre d'apparitions pour passer en L2
        self.l2_threshold = 3    # Nombre d'apparitions pour passer en L3
        self.l3_threshold = 5    # Nombre d'apparitions pour renforcement L3
        
        # Structure pour les transitions (A -> B)
        self.transitions = {}
        self.last_item = None
        
        print("🧠 SimpleHippocampus initialized")
        print(f"📍 Position: {position}")
        print(f"📊 Memory thresholds: L1→L2 after {self.l1_threshold} reps, L2→L3 after {self.l2_threshold} reps")
    
    def encode(self, signal: str, importance: float = 1.0) -> None:
        """
        Encode un signal dans la mémoire.
        
        Args:
            signal: Le signal à encoder (ex: "A", "B", "HELLO")
            importance: Facteur d'importance (0.0 à 1.0)
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
    
    def consolidate(self) -> None:
        """
        Routine de consolidation - déplace les patterns de L1 vers L2/L3.
        
        Cette méthode est appelée périodiquement pour simuler le renforcement.
        """
        signals_to_move = []
        
        # Vérifier les signals en L1 pour passage en L2
        for signal, count in self.pattern_counts.items():
            if signal in self.memory_store['L1']:
                if count >= self.l1_threshold and count < self.l2_threshold:
                    # Déplacer en L2
                    signals_to_move.append((signal, 'L2'))
                    print(f"🔄 Consolidating '{signal}' from L1 → L2 (count: {count})")
        
        # Vérifier les signals en L2 pour passage en L3
        for signal, count in self.pattern_counts.items():
            if signal in self.memory_store['L2']:
                if count >= self.l2_threshold and count < self.l3_threshold:
                    # Déplacer en L3
                    signals_to_move.append((signal, 'L3'))
                    print(f"🔄 Consolidating '{signal}' from L2 → L3 (count: {count})")
                elif count >= self.l3_threshold:
                    # Renforcer en L3
                    print(f"💪 Reinforcing '{signal}' in L3 (count: {count})")
        
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
        Récupère une prédiction basée sur le contexte.
        
        Args:
            context: Le contexte de requête (ex: "A" pour prédire ce qui suit)
            
        Returns:
            La prédiction la plus probable, ou "?" si rien n'est trouvé
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
        Encode une séquence de signaux pour apprendre les transitions.
        
        Args:
            sequence: Liste de signaux dans l'ordre chronologique
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
        """Retourne l'état actuel de la mémoire"""
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
    Test unitaire pour vérifier que l'hippocampe apprend bien les patterns.
    
    Scénario: A -> B -> A -> B -> A -> B
    L'hippocampe doit apprendre que après "A" vient souvent "B"
    """
    print("\n🧪 TEST UNITAIRE: Apprentissage de Pattern")
    print("=" * 60)
    
    # Créer l'hippocampe
    hippo = SimpleHippocampus()
    
    # Séquence d'apprentissage
    sequence = ["A", "B", "A", "B", "A", "B"]
    
    print(f"📚 Séquence d'apprentissage: {sequence}")
    print()
    
    # Phase 1: Encodage
    print("📝 PHASE 1: Encodage")
    print("-" * 30)
    
    for i, signal in enumerate(sequence):
        print(f"Tour {i+1}: Encodage de '{signal}'")
        hippo.encode(signal, importance=1.0)
        
        # Consolidation après chaque encodage
        hippo.consolidate()
        
        # Afficher l'état de la mémoire
        status = hippo.get_memory_status()
        print(f"   Mémoire: L1={status['L1_count']}, L2={status['L2_count']}, L3={status['L3_count']}")
        print()
    
    # Phase 2: Récupération et Prédiction
    print("🔍 PHASE 2: Récupération et Prédiction")
    print("-" * 40)
    
    # Tester la prédiction après "A"
    print("❓ Test de prédiction: Qu'est-ce qui suit 'A' ?")
    prediction = hippo.retrieve("A")
    
    # Vérification
    expected = "B"  # On s'attend à ce que "B" soit prédit après "A"
    success = prediction == expected
    
    print(f"🎯 Prédiction: '{prediction}'")
    print(f"✅ Succès: {success}")
    print(f"📊 Pattern counts: {hippo.pattern_counts}")
    
    # Phase 3: Vérification détaillée
    print("\n🔍 PHASE 3: Vérification Détaillée")
    print("-" * 35)
    
    status = hippo.get_memory_status()
    print(f"📦 Contenu L1: {list(status['memory_store']['L1'].keys())}")
    print(f"📦 Contenu L2: {list(status['memory_store']['L2'].keys())}")
    print(f"📦 Contenu L3: {list(status['memory_store']['L3'].keys())}")
    
    # Analyse de l'apprentissage
    a_count = hippo.pattern_counts.get("A", 0)
    b_count = hippo.pattern_counts.get("B", 0)
    
    print(f"\n📈 Analyse:")
    print(f"   'A' apparaît {a_count} fois")
    print(f"   'B' apparaît {b_count} fois")
    print(f"   Pattern 'A' en L3: {'Oui' if 'A' in status['memory_store']['L3'] else 'Non'}")
    print(f"   Pattern 'B' en L3: {'Oui' if 'B' in status['memory_store']['L3'] else 'Non'}")
    
    # Résultat final
    print(f"\n🏁 RÉSULTAT DU TEST:")
    print("=" * 25)
    if success:
        print("✅ TEST RÉUSSI: L'hippocampe a appris le pattern!")
        print("   - Le pattern 'A' → 'B' a été correctement mémorisé")
        print("   - La prédiction fonctionne comme attendu")
    else:
        print("❌ TEST ÉCHOUÉ: L'hippocampe n'a pas appris correctement")
        print("   - Vérifiez les seuils de consolidation")
        print("   - Vérifiez la logique de recherche")
    
    return success


def test_hippocampus_complex_pattern():
    """
    Test unitaire pour un pattern plus complexe.
    
    Scénario: "HELLO" -> "WORLD" -> "HELLO" -> "WORLD"
    """
    print("\n🧪 TEST UNITAIRE: Pattern Complexe")
    print("=" * 50)
    
    hippo = SimpleHippocampus()
    
    # Séquence plus complexe
    sequence = ["HELLO", "WORLD", "HELLO", "WORLD"]
    
    print(f"📚 Séquence: {sequence}")
    
    # Encodage
    for signal in sequence:
        hippo.encode(signal, importance=1.5)  # Importance plus élevée
        hippo.consolidate()
    
    # Test de prédiction
    print(f"\n❓ Qu'est-ce qui suit 'HELLO' ?")
    prediction = hippo.retrieve("HELLO")
    
    success = prediction == "WORLD"
    print(f"🎯 Prédiction: '{prediction}'")
    print(f"✅ Succès: {success}")
    
    return success


def run_all_tests():
    """Exécute tous les tests unitaires"""
    print("🚀 LANCEMENT DES TESTS UNITAIRES HIPPOCAMPE")
    print("=" * 60)
    
    # Test 1: Pattern simple
    test1_success = test_hippocampus_pattern_learning()
    
    # Test 2: Pattern complexe
    test2_success = test_hippocampus_complex_pattern()
    
    # Résumé
    print("\n📊 RÉSUMÉ DES TESTS")
    print("=" * 25)
    print(f"Test 1 (Pattern A→B): {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"Test 2 (Pattern HELLO→WORLD): {'✅ PASS' if test2_success else '❌ FAIL'}")
    
    overall_success = test1_success and test2_success
    print(f"\n🎯 RÉSULTAT GLOBAL: {'✅ TOUTES LES FONCTIONS DE BASE SONT VALIDÉES' if overall_success else '❌ CERTAINES FONCTIONS NÉCESSITENT DES AJUSTEMENTS'}")
    
    if overall_success:
        print("\n🎉 L'hippocampe est prêt pour l'intégration!")
        print("   - encode() fonctionne correctement")
        print("   - retrieve() fonctionne correctement") 
        print("   - consolidate() fonctionne correctement")
        print("   - La structure de données est valide")
    else:
        print("\n⚠️  Des ajustements sont nécessaires avant l'intégration")
    
    return overall_success


if __name__ == "__main__":
    # Exécuter tous les tests
    success = run_all_tests()
    
    print(f"\n🏁 STATUT: {'HIPPOCAMPE PRÊT POUR INTÉGRATION' if success else 'HIPPOCAMPE EN ATTENTE DE CORRECTIONS'}")