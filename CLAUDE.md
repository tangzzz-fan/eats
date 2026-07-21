# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a structured 12-day Python hands-on learning repository themed around building an **Embodied AI Trajectory Tracker Simulator (EATS)**. Each day's module contains TODO placeholders with `NotImplementedError` that learners fill in to practice specific Python skills — from OOP fundamentals through deep learning to robotics simulation.

## Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests (unimplemented modules are auto-skipped via pytest.skip on NotImplementedError)
pytest

# Run a single day's tests
pytest tests/test_day01_bank_account.py

# Type checking
mypy src
```

No build step — this is a uv-managed project (Python 3.12). Dependencies are in `pyproject.toml` and installed via `uv sync`.

## Architecture

```
src/python_projects/          # Main package
├── core/                     # Day 1: BankAccount OOP class
├── common/                   # Shared utilities
│   ├── utils.py              # setup_logger() — standard logging config used project-wide
│   ├── day02_log_analyzer.py # Log file scanning/archiving (os, shutil, datetime)
│   ├── day03_tools.py        # @retry decorator + fibonacci_generator
│   └── day05_cli.py          # argparse CLI with 'analyze' subcommand → calls day02
├── data_engineering/         # Numerical computing & data pipelines
│   ├── day04_data_processor.py # CSV→pandas→matplotlib pipeline with NaN handling
│   ├── day06_kmeans.py       # Pure NumPy K-means: broadcasting distance matrix, argmin, centroid update
│   └── day07_pipeline.py     # Pandas time-series: resample→ffill→rolling/lag features→chronological split
├── modeling/                 # PyTorch deep learning
│   ├── day08_trainer.py      # YAML config loading, argparse merge, Trainer class (train_epoch/val_epoch/fit)
│   ├── day09_network.py      # TelemetryDataset, SteeringMLP (BatchNorm+Dropout), early-stopping training loop
│   ├── day10_attention.py    # From-scratch MultiHeadAttention + FeedForwardNetwork (pure PyTorch, no nn.MultiheadAttention)
│   └── day11_generator.py    # Transformer-based LanguageModel, top-k sampling, autoregressive generation loop
└── simulation/               # Embodied AI / robotics
    ├── day12_kinematics.py   # Robot2D: Euler-integration differential-drive kinematics
    ├── day12_controller.py   # PIDController with integral anti-windup
    └── day12_sim_loop.py     # Circular path generation + closed-loop trajectory tracking simulation
```

**Cross-module dependencies**: `day05_cli` → `day02_log_analyzer`; `day12_sim_loop` → `day12_kinematics` + `day12_controller`; `day09_network` consumes features built by `day07_pipeline`. Configuration flows from `config/config.yaml` → `day08_trainer.load_yaml_config`.

## Testing Pattern

Every test file follows the same skip-on-unimplemented convention:

```python
try:
    result = some_function()
    assert result == expected
except NotImplementedError:
    pytest.skip("some_function is not implemented yet.")
```

This means `pytest` always passes — use `pytest -v` to see which tests skipped vs. ran. A fully-implemented module will show all tests as `PASSED` with no `SKIPPED`.

## Data Files

- `data/sample.csv` — small CSV with `Date,Value` columns (contains intentional NaN gaps for Day 4 fill exercises)
- `data/raw_odometry.csv` — 20 rows of `timestamp,value` sensor readings for Day 7 Pandas pipeline
- `config/config.yaml` — hyperparameters for training (lr, batch_size, epochs, patience) and robot control (PID gains, sim dt)
