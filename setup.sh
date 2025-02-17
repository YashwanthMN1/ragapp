# find . -type d -name "__pycache__" -exec rm -rf {} +
python3 -m venv ragenv

source ragenv/bin/activate

pip install --no-cache-dir -r req.txt


