# src/ structure overview
-------------------------
    1. main: Main control loop - setup motors and encoders, setup IMU. Loop over scanning sensors, updating current position, and calling trajectory function.
    2. trajectories: 4 trajectories (STILL, LEFT, RIGHT, CIRCLE). Defines function with chosen trajectory, which then calculates the desired position xd.
    3. drive: Defines 2 motors and 2 encoders, along with LQR and PID updating functions.
    4. config: Defines constant values that we may change over time, like kp, ki, kd.


# test/ structure overview
--------------------------
    1. motor_test: Tests that motors are working properly.
    2. encoder_test: Tests that encoders are working properly.


# venv/ and requirements.txt
----------------------------
**IMPORTANT:** Everyone should use Python 3.13.x for consistency.
    check your python version: python --version

Set up your virtual environment once:
    1. Open terminal (Ctrl + `)
    2. python -m venv .venv
    3. .venv\Scripts\Activate.ps1
    4. python -m pip install --upgrade pip
    5. python -m pip install -r requirements.txt

When opening a new VS Code terminal, if you don't see (.venv),
you may need to activate with:
    .venv\Scripts\Activate.ps1

And you may need to select it as interpreter:
    1. Ctrl + Shift + P
    2. Python: Select Interpreter
    3. Choose .venv\Scripts\python.exe

When adding a new library:
    1. python -m pip install library_name
    2. python -m pip freeze > requirements.txt

**IMPORTANT:** Do not commit your venv to GitHub.
    It is in .gitignore so that shouldn't happen, but watch out.


# coding conventions
--------------------
| Convention     | Recommendation                     |
| -------------- | ---------------------------------- |
| File names     | `snake_case.py`                    |
| Function names | `snake_case()`                     |
| Class names    | `PascalCase`                       |
| Constants      | `UPPER_CASE`                       |
| Indentation    | 4 spaces                           |
| Imports        | At the top of the file             |
| Documentation  | Docstrings for important functions |
