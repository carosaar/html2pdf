"""
PyInstaller hook for tkinterdnd2.

This hook ensures that tkinterdnd2 is properly bundled with PyInstaller.
It collects all submodules and data files (e.g., DLLs) needed for tkinterdnd2.
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

# Collect all submodules of tkinterdnd2
hiddenimports = collect_submodules('tkinterdnd2')

# Collect data files (e.g., DLLs) for tkinterdnd2
datas = collect_data_files('tkinterdnd2')

# Collect dynamic libraries
binaries = collect_dynamic_libs('tkinterdnd2')