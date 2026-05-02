🚀 Quick links: [ReadMe](/README.md), Installation, [Contributing](/CONTRIBUTING.md), [Innovation-Lab](/docs/innovation-lab.md), [Philosophy](/docs/philosophy.md), [Genesis](/docs/genesis.md), [Architecture](/docs/architecture.md)

Instructions française : [installation (fr)](/docs/installation_fr.md)

# Installation and Usage: ✴️*aNA* AI Project

```
░              ░ ░░░▒▒▓▒▓▒▒▒▒▒░░▒▒░▒▒▒▓▒▓▒                                                                     ░ ░
▒░░   ░░░░░░░░░░▒▒▓▓▓▓▓▓▓██▓▒▒▒░░░▒▒▒▒▒░░░▒▒▓▓▒                                                         ░░░░░░▒▒▒▒
░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓██████▓▓▒▒▒░░▒▒▓▓▓▒▒▒░░▒▒▒▒▓▒                                        ░ ░░░ ░ ░░░░░░░░░▒▒▒▒▒▒
▓▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓▓██████▓▒▒ ▒   ▒▓▒▓▒▒▒▒▓▒▓ ██▓▓▓▒▒▒▒▓      ░░▒▒▒▒▒▒▒░░░░░░▒░░░░▒▒░░▒░░░░░░░░░░░░░░░░░▒░▒▒▒░▒▒▒▓▓▓▓
▒▒▒▒▒▒▒▓▓▓▓▓████▓▓░                 ░░▒▒▒▓█▓░▓▓█▓▓ ░▒▓  ▒▓▓▓▓▓█▓▓▓█▓▒▒▒▓▓▒░░░░▒▓█▓▓▓▓▓▒▓▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒
▒▒▓▒▓▓▓▓█████▓▒                         ░▒▒▓░ ▓██▓                ▒▓▒▒░░▒▓▒░░▒▓███▓█▓▓▓▓▓▓▓▓▓▓▓▒▓▒▒▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓
▓▓▓█████▓░                                    ░░▒▒ _    _    _ ░▒░▒▒▒▓▒▓▒▓▒▓█▓███▒▓▓▓▓▓▓▓▓▓▓▓▓▓█▓██▓▓▓▓▓█▓████████
▓███▓▒      AI inspired by natural plasticity  ✴️  a    N    A  ▒▓█▒▓ ▒▓█▒Autonomous Neural Architecture v5.3  ▒▓▓
▓░                                                 _    _    _  ░▓▒▓  ░▓
```

###### _"The Creation" —Michelangelo_

## Multi-Platform Installation Guide

To ensure optimal configuration of _aNA IA_'s neural architecture, this section helps you to configure its environment according to your system.

### Common First Steps

Before jumping into OS-specific guides, ensure you have the following ready:

- **Git** : Be sure to clone _[aNA-ai.git](https://github.com/theriaubenoit-ops/aNA-ai.git)_.
- **Python 3.10+** : You had the free core engine.
- **Virtual Environment Knowledge** : Strictly use `venv` to protect your system's integrity.

### Basic concepts _(Terminal)_

Here are the universal commands you will use to navigate:

- **`cd <folder_name>`**: Enter a folder _(e.g.,`cd aNA-ai`)_.
- **`cd ..`**: Return to parent's folder.
- **`ls`** _(Mac/Linux)_ or **`dir`** _(Windows)_: List the files present.

![ ](/docs/assets/spacer32x32.png)

## Choose your OS

Please select the guide corresponding to your operating system:

![ ](/docs/assets/spacer32x32.png)

# 🪟 Windows _(PC)_

For the best experience, use **PowerShell** or **Git Bash**.

- **Installing Python:** Download it from the Microsoft Store or python.org. **Important:** Check the "Add Python to PATH" box during installation.
- **Cloning** :
  ```powershell
  git clone https://github.com/theriaubenoit-ops/aNA-ai.git
  cd aNA-ai
  ```
- **Virtual Environment** :
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **Dependencies** :

  ```powershell
  pip install -r requirements.txt
  ```

[Continued ▶️](/docs/installation_2.md)

![ ](/docs/assets/spacer32x32.png)

# 🍏 macOS _(Apple)_

On Mac, using the terminal is smooth, but sometimes requires administrative permissions.

- **Open the Terminal**: Press `Cmd + Space` and type "Terminal".
- **Install Python**: Check with `python3 --version`. If it's not there, download it from _python.org_.
- **Clone & Folder**:
  ```bash
  git clone https://github.com/theriaubenoit-ops/aNA-ai.git
  cd aNA-ai
  ```
- **Virtual Environment** :
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **Dependencies** :

  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

[Continued ▶️](/docs/installation_2.md)

> **Note :** If you have a permission error, use `sudo pip install...` _(your password will be requested, but it will not be displayed while typing)_.

![ ](/docs/assets/spacer32x32.png)

# 🐧 Linux _(Ubuntu/Debian)_

Installing on Linux often requires updating system packages first.

- **Update & Prerequisites** :
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

[Continued ▶️](/docs/installation_2.md)

![ ](/docs/assets/spacer32x32.png)

## Quick Verification

Once installed, you can verify the "heartbeat" of the project by running a basic neuron test from your terminal:
`python3 src/tests/test_neuron.py`

### ⚒️ Troubleshooting (FAQ)

- **"Command not found"**: Make sure Python is installed. On Windows, restart your terminal after installation.
- **"Permission denied"**: On Mac and Linux, add `sudo` before your command if you are not in a virtual environment.
- **How ​​do I know if I'm in the correct directory?**: Type `pwd` (Mac/Linux) or `echo %cd%` (Windows) to see your current path. It should end with `/aNA-ai`.

![ ](/docs/assets/spacer16x16.png)

<a href="#start-of-content" style="text-decoration: none;">Back to top 🔼</a>

![ ](/docs/assets/spacer16x16.png)

_░▒▓ [BT](https://github.com/theriaubenoit-ops/) 2026-05-02_
