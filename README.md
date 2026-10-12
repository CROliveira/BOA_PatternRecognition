# BOA — Pattern Recognition for Software Testing Automation

> **Finalist, 2019 North American Software Testing & QE Awards** — *Best Use of Technology in a Project* (Cloudpipe Inc.)

BOA is a pattern-recognition solution for software testing automation. It applies machine learning to test data and execution results to identify patterns in pass/fail behaviour — helping QA teams focus effort where failures are most likely and automate scenario selection.

## How it works

The pipeline is organized by stage, each in its own module:

| Directory | Stage |
|---|---|
| `dataHarvesting/` | Collects test execution data and results |
| `featureEngineering/` | Builds predictive features from test artefacts |
| `machineLearning/` | Trains pattern-recognition models on pass/fail outcomes |
| `passFailScenario/` | Defines and evaluates pass/fail test scenarios |
| `latestPass/` | Tracks the most recent passing state |
| `testData/` | Sample and fixture data |
| `nest/` | Supporting/nested components |

## Repository contents

- `Desktop/Boa-master/` — the full project snapshot (modules above)
- `README.md` — this file

## Background

Built 2019–2020, during a period of applied machine-learning work in software quality engineering. The project was nominated as a finalist for the 2019 North American Software Testing & QE Awards in the *Best Use of Technology in a Project* category. This repository is an archived snapshot — shared as a record of the approach, not as maintained software.
