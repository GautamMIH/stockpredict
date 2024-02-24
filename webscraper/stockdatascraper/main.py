import subprocess

# List of Python files to run in sequential order
python_files = ['alicl.py', 'cli.py', 'hli.py', 'ili.py', 'licn.py', 'nlic.py', 'nlicl.py', 'pmli.py', 'rnli.py', 'sjlic.py', 'snli.py', 'srli.py']

# Loop through the list and execute each file
for file in python_files:
    print('now pulling file:'+file)
    subprocess.run(['python', file])