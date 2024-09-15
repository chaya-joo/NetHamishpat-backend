import os
from dotenv import set_key


secret_key = os.urandom(32).hex()
set_key('../.env', 'SECRET_KEY', secret_key)

