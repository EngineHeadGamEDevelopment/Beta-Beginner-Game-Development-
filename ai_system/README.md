# Draegtile AI System

A unified, self-learning AI system built from the ideas described in the project's `guides/` folder.

## Architecture

```
ai_system/
├── bios/
│   └── draegtile_bios.py     # BIOS: boot sequence, POST, security, sensor stubs
├── core/
│   ├── ai_module.py          # Self-learning AI (online mean/regression, anomaly detection)
│   ├── code_interpreter.py   # Multi-language script runner (Python, JS, C++)
│   ├── data_handler.py       # Real-time data fetching & pre-processing
│   ├── stack_machine.py      # Draegtile stack VM + multi-dimensional data stacks
│   ├── user_interaction.py   # User event logging with hooks
│   └── visualizer.py         # 3-D visualiser (PyVista → Matplotlib → ASCII fallback)
├── game/
│   └── rpg_game.py           # Open-world text RPG (exploration, combat, quests, NPCs)
├── main.py                   # Unified entry point / interactive menu
└── README.md                 # This file
```

## Quick Start

```bash
# From the repository root
python ai_system/main.py
```

No third-party packages are required.  Optional packages add richer output:
- `pyvista` — 3-D mesh visualisation
- `matplotlib` — 2-D / 3-D plots

## Modules

### DraegtileBIOS (`bios/draegtile_bios.py`)
Simulates the Draegtile BIOS layer described in `guides/Draegtile Bios.txt`.
- Power-On Self-Test (POST)
- Hardware/OS discovery
- SHA-256 integrity check for watched source files
- Temperature and frequency sensor stubs
- Module registration registry

### StackMachine & DimensionalStack (`core/stack_machine.py`)
Implements the stack-based virtual machine from `guides/Draegtile overview.txt`.
- `StackMachine` — executes PUSH, POP, ADD, SUB, MUL, DIV, DUPLICATE, SWAP, PRINT, CLEAR
- `DimensionalStack` — 1-D, 2-D and 3-D data containers

### AILearningModule (`core/ai_module.py`)
Lightweight, dependency-free self-learning AI based on the AI module designs in
`guides/Python Detailer.txt` and `guides/A basic python idea script module for complete implementation.txt`.
- `learn(label, value)` — online incremental mean / variance update
- `predict(label)` — linear-regression-based next-value prediction
- `is_anomaly(label, value)` — z-score anomaly detection
- `optimize()` — returns a summary of learned metrics
- `self_repair(label)` — resets learned state when drift is too large
- `save(path)` / load from JSON — persistent model state

### DataHandler (`core/data_handler.py`)
Fetches and pre-processes data from external JSON APIs.
Uses only the Python standard library (`urllib`).

### UserInteraction (`core/user_interaction.py`)
Records user events with timestamps and supports callback hooks.
Feeds interaction history back to the AI for continuous adaptation.

### CodeInterpreter (`core/code_interpreter.py`)
Runs scripts or inline code snippets in Python, JavaScript (Node.js), or C++.

### Visualizer (`core/visualizer.py`)
Renders stack/array data using the best available backend:
1. PyVista (3-D mesh)
2. Matplotlib (2-D / 3-D plot)
3. ASCII table (always available)

### RPGGame (`game/rpg_game.py`)
Fully playable text RPG described in `guides/Guide contents.txt`.
- 6 explorable locations (village, forest, cave, ruins, plains, market)
- Turn-based combat
- Inventory system
- 2 built-in quests
- NPC dialogue
- Levelling system with XP and gold

## Running Tests

```bash
python -m pytest ai_system/tests/ -v
```

## Guides This System Is Based On

| Guide file | Module(s) |
|---|---|
| `Guide contents.txt` | `game/rpg_game.py` |
| `A basic python idea script module for complete implementation.txt` | `core/ai_module.py`, `core/data_handler.py` |
| `Python Detailer.txt` | All core modules |
| `A unified project build.txt` | `main.py` (UnifiedSystem) |
| `Draegtile overview.txt` | `core/stack_machine.py`, `core/ai_module.py` |
| `Draegtile Bios.txt` | `bios/draegtile_bios.py` |
| `Implementation phase 1.txt` | `main.py` |
| `Basic weather and news AI models using python script.txt` | `core/data_handler.py` |
