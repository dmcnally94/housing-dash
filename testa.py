from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()
CENSUS_KEY = os.getenv('CENSUS_KEY')
print(CENSUS_KEY)