@echo off
python -m venv venv

call venv\Scripts\activate

pip install -r req.txt

echo Virtual environment setup complete.
pause
