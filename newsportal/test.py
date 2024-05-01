import os
from pathlib import Path

dotenv_path = os.path.join(os.path.dirname(__file__)[:-11], '.env')
# test = dotenv_path.rsplit(maxsplit=1)
print()
# test = os.path.normpath(dotenv_path)
print(dotenv_path)
