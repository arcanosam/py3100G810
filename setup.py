import sys
from cx_Freeze import setup, Executable

setup(
    name = 'py3100g810Csv',
    options={
        'build_exe': {
            'packages': ['dao','gui'],
            'include_files': ['lang.ini','devices.ini','grains.data','LICENSE']
            }
        },
    version = '0.0.1',
    description = 'Grains weight and humidity collector',
    executables = [
        Executable(
            'main.py',
            base = 'Win32GUI'
        )
    ]
)