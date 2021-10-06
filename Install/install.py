# sqljin installer 

import sys, subprocess
from venv import EnvBuilder 
from pathlib import Path


# TODO: setup logging

# Setup virtual environment
p = Path('.')
coaEnv = EnvBuilder(with_pip=True, prompt='sqljin')
coaEnv.create( p / 'install' / 'venv')


