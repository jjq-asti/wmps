import subprocess
from pathlib import Path

speedtest = Path('wmps') / 'ookla' / 'speedtest'
def run(server=None):
    """create speedtest and return process"""
    proc = subprocess.Popen([speedtest, '-f', 'jsonl'], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        encoding='utf-8',
        errors='replace')

    return proc
