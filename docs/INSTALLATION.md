🚀 Quick links: [ReadMe](/README.md), Installation, [Usage](/docs/usage.md), [Contributing](/CONTRIBUTING.md), [Innovation-Lab](/docs/innovation-lab.md), [Philosophy](/docs/philosophy.md), [Genesis](/docs/genesis.md), [Architecture](/docs/architecture.md)

Instructions française : [installation (fr)](/docs/INSTALLATION_fr.md)

# Installation: ✴️*aNA AI* Project

```
░              ░ ░░░▒▒▓▒▓▒▒▒▒▒░░▒▒░▒▒▒▓▒▓▒                                                                     ░ ░
▒░░   ░░░░░░░░░░▒▒▓▓▓▓▓▓▓██▓▒▒▒░░░▒▒▒▒▒░░░▒▒▓▓▒                                                         ░░░░░░▒▒▒▒
░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓██████▓▓▒▒▒░░▒▒▓▓▓▒▒▒░░▒▒▒▒▓▒                                        ░ ░░░ ░ ░░░░░░░░░▒▒▒▒▒▒
▓▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓▓██████▓▒▒ ▒   ▒▓▒▓▒▒▒▒▓▒▓ ██▓▓▓▒▒▒▒▓      ░░▒▒▒▒▒▒▒░░░░░░▒░░░░▒▒░░▒░░░░░░░░░░░░░░░░░▒░▒▒▒░▒▒▒▓▓▓▓
▒▒▒▒▒▒▒▓▓▓▓▓████▓▓░                 ░░▒▒▒▓█▓░▓▓█▓▓ ░▒▓  ▒▓▓▓▓▓█▓▓▓█▓▒▒▒▓▓▒░░░░▒▓█▓▓▓▓▓▒▓▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒
▒▒▓▒▓▓▓▓█████▓▒                         ░▒▒▓░ ▓██▓                ▒▓▒▒░░▒▓▒░░▒▓███▓█▓▓▓▓▓▓▓▓▓▓▓▒▓▒▒▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓
▓▓▓█████▓░                                    ░░▒▒ _    _    _ ░▒░▒▒▒▓▒▓▒▓▒▓█▓███▒▓▓▓▓▓▓▓▓▓▓▓▓▓█▓██▓▓▓▓▓█▓████████
▓███▓▒      AI inspired by natural plasticity  ✴️  a    N    A  ▒▓█▒▓ ▒▓█▒Autonomous Neural Architecture v5.4.1▒▓▓
▓░                                                 _    _    _  ░▓▒▓  ░▓
```

###### _"The Creation" —Michelangelo_

![ ](/docs/assets/spacer16x16.png)

_This is your multi-platform installation Guide. To ensure optimal configuration of **aNA** AI's neural architecture, this section helps you to configure its environment according to your system. Please read the common and basic then select the guide corresponding to your operating system._

![ ](/docs/assets/spacer16x16.png)

### Common First Steps

Before jumping into OS-specific guides, ensure you have the following ready _(See the instructions)_:

- **Git** : Be sure to clone/download the latest version of the Code _aNA-ai.git_.
- **Python 3.10+** : You had the core engine.
- **Virtual Environment Knowledge** : Strictly use `venv` to protect your system's integrity.

### Basic concepts _(Terminal)_

Here are the universal commands you will use to navigate:

- **`cd <folder_name>`**: Enter a folder _(e.g.,`cd aNA-ai`)_.
- **`cd ..`**: Return to parent's folder.
- **`ls`** _(Mac/Linux)_ or **`dir`** _(Windows)_: List the files present.

![ ](/docs/assets/spacer32x32.png)

## Choose your OS

![ ](/docs/assets/spacer16x16.png)

# 🪟 Windows _(PC)_

For the best experience, use **PowerShell** or **Git Bash**.

- [ ] **Installing Python:** Download it from the _Microsoft Store_ or _python.org_. **Important:** Check the _"Add Python to PATH"_ box during installation.
- [ ] **Cloning** :
  ```powershell
  git clone https://github.com/theriaubenoit-ops/aNA-ai.git
  cd aNA-ai
  ```
- [ ] **Virtual Environment** :
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
- [ ] **Dependencies** :

  ```powershell
  pip install -r requirements.txt
  ```

[Usage and tests ▶️](/docs/usage.md)

![ ](/docs/assets/spacer32x32.png)

# 🍎 macOS _(Apple)_

On _Mac_, using the terminal is smooth, but sometimes requires administrative permissions.

- [ ] **Open the Terminal**: Press `Cmd + Space` and type "Terminal".
- [ ] **Install Python**: Check with `python3 --version`. If it's not there, download it from _python.org_.
- [ ] **Clone & Folder**:
  ```bash
  git clone https://github.com/theriaubenoit-ops/aNA-ai.git
  cd aNA-ai
  ```
- [ ] **Virtual Environment** :
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- [ ] **Dependencies** :

  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

> **Note :** If you have a permission error, use `sudo pip install...` _(your password will be requested, but it will not be displayed while typing)_.

[Usage and tests ▶️](/docs/usage.md)

![ ](/docs/assets/spacer32x32.png)

# 🐧 _Linux (Ubuntu/Debian)_

Installing on _Linux_ often requires updating system packages first.

- [ ] **Update & Prerequisites** :
  ```bash
  sudo apt update
  sudo apt install python3-venv python3-pip git
  ```
- [ ] **Installation** :

  ```bash
  git clone https://github.com/theriaubenoit-ops/aNA-ai.git
  cd aNA-ai
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

[Usage and tests ▶️](/docs/usage.md)

![ ](/docs/assets/spacer32x32.png)

## Quick Verification

Once installed, you can verify the _"heartbeat"_ of the project by running a basic neuron test from your terminal:
`python3 tests/test_neuron.py`

### ⚒️ Troubleshooting _(FAQ)_

- **"Command not found"**: Make sure Python is installed. On Windows, restart your terminal after installation.
- **"Permission denied"**: On _Mac_ and _Linux_, add `sudo` before your command if you are not in a virtual environment.
- **How ​​do I know if I'm in the correct directory?**: Type `pwd` _(Mac/Linux)_ or `echo %cd%` _(Windows)_ to see your current path. It should end with `/aNA-ai`.

![ ](/docs/assets/spacer16x16.png)

<a href="#start-of-content" style="text-decoration: none;">Back to top 🔼</a>

![ ](/docs/assets/spacer16x16.png)

_░▒▓ [BT](https://github.com/theriaubenoit-ops/) 2026-05-21_
