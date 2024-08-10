Overview
========
<img src="https://raw.githubusercontent.com/ushumgigal/noroi/main/noroi.png" style="height: 300px; width:auto;"/>

![GitHub Release](https://img.shields.io/github/v/release/ushumgigal/noroi?display_name=release&style=plastic)
![License](https://img.shields.io/badge/license-MIT-aquamarine?style=plastic)

Wrapper for the curses module.

Aim and Scope of the Project
============================
- The project aims to create a wrapper library for Python's curses module that provides
  - A user-friendly way to create TUI apps, taking care of the low-level hassle
  - A simple syntax built around Python dictionaries
  - Ready-to-use TUI widgets, based on the package's core module class Div
- Package distribution will be implemented once the project's matured enough (which shouldn't be too far off).
- Simple progress chart for Divs/Widgets:

|           |  Div   |  Label | Button | TextArea |  Slider  | List | Bar Graph | Shape | Digital Clock |
|:---------:|:------:|:------:|:------:|:--------:|:--------:|:----:|:---------:|:-----:|:-------------:|
|  version  | ≥1.0.0 | ≥1.0.0 | ≥1.0.0 |  ≥1.0.0  |    WIP   | TBA  |    TBA    | TBA   |     TBA       |


Compatibility
=============
- Recommended Python version: 3.10.12
- Should run without any issue on any terminal emulator with color support.

Getting Started
===============
Simply clone the repo and run the setup script, then  test.py
```bash
git clone https://github.com/ushumgigal/noroi
noroi/setup.sh
noroi/tests/test.py
```
<img src="https://raw.githubusercontent.com/ushumgigal/noroi/main/demo.gif" style="width: 768px; height:auto;"/>

The test script utilizes every single element within the package noroi. If you haven't run into any issues so far, that means your setup is perfectly compatible with the modules and you're all set.

Attention
=========
- The source code is copyrighted (2024) by [ushumgigal](https://github.com/ushumgigal) under MIT License, a copy of which may be found in the root folder of the [repository](https://github.com/ushumgigal/noroi).
- This is not a derivative work and does not include or modify any priorly copyrighted work in source or object form.

Contact
=======
atilla_aricioglu@yahoo.com
