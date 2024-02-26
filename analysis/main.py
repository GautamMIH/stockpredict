import subprocess

# List of Python files to run in sequential order
python_files = ['debentures.py', 'foreignexchange.py', 'impactingscripts.py', 'ipo.py', 'marketindices.py', 'marketsummary.py', 'mutualfund.py', 'rightshare.py', 'subindices.py', 'totalbroker.py', 'v1.py']

# Loop through the list and execute each file
for file in python_files:
    print('now pulling file:'+file)
    subprocess.run(['python', file])