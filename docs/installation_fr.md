🚀 Quick links: [ReadMe](/README.md), Installation, [Contributing](/CONTRIBUTING.md), [Innovation-Lab](/docs/innovation-lab.md), [Philosophy](/docs/philosophy.md), [Genesis](/docs/genesis.md), [Architecture](/docs/architecture.md)

English instructions: [installation (en)](/docs/installation.md)

# Installation et utilisation projet ✴️*aNA* AI v5

```
░              ░ ░░░▒▒▓▒▓▒▒▒▒▒░░▒▒░▒▒▒▓▒▓▒                                                                     ░ ░
▒░░   ░░░░░░░░░░▒▒▓▓▓▓▓▓▓██▓▒▒▒░░░▒▒▒▒▒░░░▒▒▓▓▒                                                         ░░░░░░▒▒▒▒
░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓██████▓▓▒▒▒░░▒▒▓▓▓▒▒▒░░▒▒▒▒▓▒                                        ░ ░░░ ░ ░░░░░░░░░▒▒▒▒▒▒
▓▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓▓██████▓▒▒ ▒   ▒▓▒▓▒▒▒▒▓▒▓ ██▓▓▓▒▒▒▒▓      ░░▒▒▒▒▒▒▒░░░░░░▒░░░░▒▒░░▒░░░░░░░░░░░░░░░░░▒░▒▒▒░▒▒▒▓▓▓▓
▒▒▒▒▒▒▒▓▓▓▓▓████▓▓░                 ░░▒▒▒▓█▓░▓▓█▓▓ ░▒▓  ▒▓▓▓▓▓█▓▓▓█▓▒▒▒▓▓▒░░░░▒▓█▓▓▓▓▓▒▓▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒
▒▒▓▒▓▓▓▓█████▓▒                         ░▒▒▓░ ▓██▓                ▒▓▒▒░░▒▓▒░░▒▓███▓█▓▓▓▓▓▓▓▓▓▓▓▒▓▒▒▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓
▓▓▓█████▓░                                    ░░▒▒ _    _    _ ░▒░▒▒▒▓▒▓▒▓▒▓█▓███▒▓▓▓▓▓▓▓▓▓▓▓▓▓█▓██▓▓▓▓▓█▓████████
▓███▓▒  IA inspirée de la plasticité naturelle ✴️  a    N    A  ▒▓█▒▓ ▒▓█▒Architecture Neuronale Autonome v5.3 ▒▓▓
▓░                                                 _    _    _  ░▓▒▓  ░▓
```

###### _"La creation" —Michelangelo_

1. **Prérequis _(The Environment)_**
   - [ ] Version _Python_ minimale _(ex: 3.10+)_
   - [ ] Dépendances de base _(ex: `pip install -r requirements.txt`)_
   - [ ] Outils recommandés _(ex: `venv` ou `conda` pour l'isolation)_

2. **Installation _(ex: Terminal, Zsh, Konsole ou Git Bash)_**
   - [ ] Clonage du repo : `git clone https://github.com/theriaubenoit-ops/aNA-ai.git`
   - [ ] Création de l'environnement : `python -m venv venv && source venv/bin/activate`
   - [ ] Installation : `pip install -r requirements.txt`

![ ](/docs/assets/spacer16x16.png)

### Exploration pratique

> **Note :** Bien que le `dashboard_fr.py` et le `main_fr.py` soient actuellement en cours de développement, la _logique neuronale centrale_ est déjà opérationnelle via notre _suite de tests_. Ces _scripts_ vous permettent d'observer en temps réel les interactions fonctionnelles entre les différents _organes numériques_.

![ ](/docs/assets/spacer16x16.png)

![img](/docs/assets/test_256x256.gif)

###### _Retrouvez de nombreux fichiers test dans `src/tests/`_

![ ](/docs/assets/spacer16x16.png)

3. - [x] **Exécution des scripts _(Phase « Action »)_** Launch associated _Python scripts_ to validate neural logic:
     - PROCHAINEMENT - `python3 src/gui/dashboard_fr.py`
     - ☄️ `python3 src/main_fr.py` _(Noyau cortical et espace de travail global)_
     - `python3 src/tests_fr/test_amygdala.py` _(Réponse homéostatique au stress et à l'alerte)_
     - ☄️ `python3 src/tests_fr/test_autonomy.py` _(Pour valider les comportements autonomes)_
     - `python3 src/tests_fr/test_cerebellum.py` _(Précision motrice et correction d'erreurs)_
     - ☄️ `python3 src/tests_fr/test_cortical_column.py` _(Flux de signal cortical à six couches)_
     - `python3 src/tests_fr/test_limbic_system.py` _(Intégration émotionnelle et cognitive)_
     - ☄️ `python3 src/tests_fr/test_hippocampus.py` _(Consolidation synaptique et encodage de motifs)_
     - ☄️ `python3 src/tests/test_hippocampus_ampa_nmda.py` _(Mémoire à court terme et à long terme)_
     - `python3 src/tests_fr/test_neuron.py` _(Dynamique métabolique et électrophysiologique)_
     - `python3 src/tests_fr/test_pulse.py` _(Oscillations neuronales et synchronisation temporelle)_
     - ☄️ `python3 src/tests_fr/test_thalamus.py` _(Filtrage sensoriel et signal routage)_
     - ☄️ `python3 src/tests_fr/test_trauma_logic.py` _(Saillance émotionnelle et traces acides)_
   - [ ] PROCHAINEMENT - Démonstrations : Pour lancer _l'interface web_ (e.g., "http://localhost:8000/examples/basic-demo.html").
     - Remarque concernant le serveur local : Pour exécuter les démonstrations web, utilisez `python3 -m http.server 8000` depuis le répertoire racine.

4. **Contribuer et Communiquer _(GitHub Workflow)_**
   - [ ] Issues : "Ouvrez une issue pour toute question ou bug."
   - [ ] Pull Requests : "Pour soumettre vos améliorations de neurones ou de modules."
   - [ ] Discussions : "Utilisez les discussions **GitHub** pour échanger sur la psychologie comportementale du modèle ou simplement pour nous dire que notre code vous a inspiré."

☄️ _Spotlight_

![ ](/docs/assets/spacer16x16.png)

###### _\*Chaque mesure présentée ici est un pont numérique vers la réalité biologique, conçu pour synthétiser les principes fondamentaux des systèmes vivants._

![ ](/docs/assets/spacer16x16.png)

<a href="#start-of-content" style="text-decoration: none;">Retour en haut 🔼</a>

![ ](/docs/assets/spacer16x16.png)

_░▒▓ [BT](https://github.com/theriaubenoit-ops/) 2026-04-26_
