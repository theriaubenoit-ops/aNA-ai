🚀 Quick links: [ReadMe](/README.md), Installation, [Contributing](/CONTRIBUTING.md), [Innovation-Lab](/docs/innovation-lab.md), [Philosophy](/docs/philosophy.md), [Genesis](/docs/genesis.md), [Architecture](/docs/architecture.md)

English instructions: [installation (en)](/docs/installation.md)

# Installation et utilisation projet ✴️*aNA* IA

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

- **Git** : Assurez-vous de cloner _[aNA-ai.git](https://github.com/theriaubenoit-ops/aNA-ai.git)_.
- **Python 3.10+** : Vous disposez du moteur de base (gratuit).
- **Virtual Environment Knowledge** : Utilisez strictement `venv` pour protéger l'intégrité de votre système.

### Notions de base _(Terminal)_

Voici les commandes universelles que vous utiliserez pour naviguer :

- **`cd <folder_name>`**: Saisissez un dossier _(ex.:`cd aNA-ai`)_.
- **`cd ..`**: Retour au dossier parent.
- **`ls`** _(Mac/Linux)_ ou **`dir`** _(Windows)_: Liste des fichiers présents.

![ ](/docs/assets/spacer16x16.png)

## Consultez votre système d'exploitation

Veuillez consulter le guide correspondant à votre système d'exploitation :

![ ](/docs/assets/spacer32x32.png)

# 🪟 Windows _(PC)_

Pour une expérience optimale, utilisez **PowerShell** ou **Git Bash**.

- **Installation de Python** : Téléchargez-le via le Microsoft Store ou python.org. **Important :** Cochez la case _"Add Python to PATH"_ lors de l'installation.
- **Clonage** :
  ```powershell
  git clone https://github.com/theriaubenoit-ops/aNA-ai.git
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

# 🍏 macOS _(Apple)_

Sur Mac, l'utilisation du terminal est fluide, mais nécessite parfois des permissions administratives.

- **Ouvrir le Terminal** : Appuyez sur `Cmd + Espace` et tapez "Terminal".
- **Installation de Python** : Vérifiez avec `python3 --version`. Si absent, téléchargez-le sur _python.org_.
- **Clonage & Dossier** :
  ```bash
  git clone https://github.com/theriaubenoit-ops/aNA-ai.git
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

# 🐧 Linux _(Ubuntu/Debian)_

L'installation sur Linux nécessite souvent de mettre à jour les paquets système d'abord.

- **Mise à jour & Prérequis** :
  ```bash
  sudo apt update
  sudo apt install python3-venv python3-pip git
  ```
- **Installation** :

  ```bash
  git clone https://github.com/theriaubenoit-ops/aNA-ai.git
  cd aNA-ai
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

[Suite ▶️](/docs/installation_2.md)

![ ](/docs/assets/spacer32x32.png)

## Vérification rapide

Une fois installé, vous pouvez vérifier le « pouls » du projet en exécutant un test neuronal de base depuis votre terminal :
`python3 src/tests/test_neuron.py`

### ⚒️ Dépannage (FAQ)

- **"Command not found"** : Assurez-vous que Python est bien installé. Sur Windows, redémarrez votre terminal après l'installation.
- **"Permission denied"** : Sur Mac et Linux, ajoutez `sudo` devant votre commande si vous n'êtes pas dans un environnement virtuel.
- **Comment savoir si je suis dans le bon dossier ?** : Tapez `pwd` _(Mac/Linux)_ ou `echo %cd%` _(Windows)_ pour voir votre chemin actuel. Il doit se terminer par `/aNA-ai`.

![ ](/docs/assets/spacer16x16.png)

<a href="#start-of-content" style="text-decoration: none;">Retour en haut 🔼</a>

![ ](/docs/assets/spacer16x16.png)

_░▒▓ [BT](https://github.com/theriaubenoit-ops/) 2026-05-02_
