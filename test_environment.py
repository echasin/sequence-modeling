import sys
import networkx
import matplotlib
import pandas
import numpy

def test_environment():
    print(f"Python version: {sys.version}")
    print(f"\nPackage versions:")
    print(f"NetworkX: {networkx.__version__}")
    print(f"Matplotlib: {matplotlib.__version__}")
    print(f"Pandas: {pandas.__version__}")
    print(f"NumPy: {numpy.__version__}")

if __name__ == "__main__":
    test_environment()
