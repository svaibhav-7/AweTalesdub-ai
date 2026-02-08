
import sys
import pkg_resources

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")

packages = ['transformers', 'TTS', 'scipy', 'numpy', 'torch']
for pkg in packages:
    try:
        dist = pkg_resources.get_distribution(pkg)
        print(f"{pkg}: {dist.version}")
    except pkg_resources.DistributionNotFound:
        print(f"{pkg}: Not Found")
    except Exception as e:
        print(f"{pkg}: Error checking version: {e}")
