### finding path
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
### needed for every file we run
