import os
from dotenv import set_key

env_path = '../.env'

env_vars = {}
if os.path.exists(env_path):
    with open(env_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, _ = line.strip().split('=', 1)
                env_vars[key] = True

secret_key = os.urandom(32).hex()

if 'SECRET_KEY' not in env_vars:
    set_key('../.env', 'SECRET_KEY', secret_key)


