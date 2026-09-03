import sys

try:
    import numpy as np
    import pandas as pd
    print("Numpy version:", np.__version__)
    print("Pandas version:", pd.__version__)
    print("Environment verification successful.")
    print(f"Python version: {sys.version}")
    
except ImportError as e:
    print(f"Error: Required packages are not installed. -> {e}")
    sys.exit(1)