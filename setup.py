# setup.py
from cx_Freeze import setup, Executable

base = None

executables = [Executable("myapp.py", base=base)]

options = {
    "build_exe": {
        # Add any additional packages your app uses
        "packages": ["django", "numpy", "pandas", "selenium", "openpyxl"],
        "excludes": [],
    },
}

setup(
    name="MyDjangoApp",
    version="1.0",
    description="My Django Application",
    options=options,
    executables=executables,
)
