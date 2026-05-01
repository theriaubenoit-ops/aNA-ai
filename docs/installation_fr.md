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

## Guide d'Installation Multi-Plateforme

Pour garantir une configuration optimale de l'architecture neuronale d'_aNA IA_, cette section vous aide à configurer son environnement en fonction de votre système.

### Premières étapes communes

Avant de commencer, assurez-vous d'avoir les éléments suivants à portée de main :

- **Git** : Be sure to clone _[aNA-ai.git](https://github.com/theriaubenoit-ops/aNA-ai.git)_.
- **Python 3.10+** : You had the free core engine.
- **Virtual Environment Knowledge** : Strictly use `venv` to protect your system's integrity.

![ ](/docs/assets/spacer16x16.png)

### Notions de base _(Terminal)_

Here are the universal commands you will use to navigate:

- **`cd <folder_name>`**: Enter a folder _(e.g.,`cd aNA-ai`)_.
- **`cd ..`**: Return to parent's folder.
- **`ls`** _(Mac/Linux)_ or **`dir`** _(Windows)_: List the files present.

## Consultez votre système d'exploitation

Veuillez consulter le guide correspondant à votre système d'exploitation :

![ ](/docs/assets/spacer32x32.png)

### 🪟 Windows _(PC)_

Pour une expérience optimale, utilisez **PowerShell** ou **Git Bash**.

- **Installation de Python** : Téléchargez-le via le Microsoft Store ou python.org. **Important :** Cochez la case _"Add Python to PATH"_ lors de l'installation.
- **Clonage** :
  ```powershell
  git clone `https://github.com/theriaubenoit-ops/aNA-ai.git`
  cd aNA-ai
  ```
- **Environnement Virtuel** :
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **Dépendances** :

  ```powershell
  pip install -r requirements.txt
  ```

  [Suite ▶️](/docs/installation_2.md)

![ ](/docs/assets/spacer32x32.png)

### 🐧 Linux _(Ubuntu/Debian)_

L'installation sur Linux nécessite souvent de mettre à jour les paquets système d'abord.

- **Mise à jour & Prérequis** :
  ```bash
  sudo apt update
  sudo apt install python3-venv python3-pip git
  ```
- **Installation** :

  ```bash
  git clone `https://github.com/theriaubenoit-ops/aNA-ai.git`
  cd aNA-ai
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

  [Suite ▶️](/docs/installation_2.md)

![ ](/docs/assets/spacer32x32.png)

### 🍏 macOS _(Apple)_

Sur Mac, l'utilisation du terminal est fluide, mais nécessite parfois des permissions administratives.

- **Ouvrir le Terminal** : Appuyez sur `Cmd + Espace` et tapez "Terminal".
- **Installation de Python** : Vérifiez avec `python3 --version`. Si absent, téléchargez-le sur _python.org_.
- **Clonage & Dossier** :
  ```bash
  git clone `https://github.com/theriaubenoit-ops/aNA-ai.git`
  cd aNA-ai
  ```
- **Environnement Virtuel** :
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **Dépendances** :

  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

  [Suite ▶️](/docs/installation_2.md)

  > **Note :** Si vous avez une erreur de permission, utilisez `sudo pip install...` _(votre mot de passe sera demandé, mais il ne s'affichera pas pendant la saisie)_.

![ ](/docs/assets/spacer32x32.png)

## Quick Verification

Une fois installé, vous pouvez vérifier le « pouls » du projet en exécutant un test neuronal de base depuis votre terminal :
`python3 src/tests/test_neuron.py`

![ ](/docs/assets/spacer16x16.png)

### 🛠️ Dépannage (FAQ)

- **"Command not found"** : Assurez-vous que Python est bien installé. Sur Windows, redémarrez votre terminal après l'installation.
- **"Permission denied"** : Sur Mac et Linux, ajoutez `sudo` devant votre commande si vous n'êtes pas dans un environnement virtuel.
- **Comment savoir si je suis dans le bon dossier ?** : Tapez `pwd` _(Mac/Linux)_ ou `echo %cd%` _(Windows)_ pour voir votre chemin actuel. Il doit se terminer par `/aNA-ai`.

![ ](/docs/assets/spacer16x16.png)

<a href="#start-of-content" style="text-decoration: none;">Retour en haut 🔼</a>

![ ](/docs/assets/spacer16x16.png)

_░▒▓ [BT](https://github.com/theriaubenoit-ops/) 2026-05-01_
