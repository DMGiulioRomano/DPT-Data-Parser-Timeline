from setuptools import setup
import os

APP = ['main.py']

# Il file icon.icns sta nella root (un livello sopra)
ICON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icon.icns')

DATA_FILES = [
    ('', ['settings.json'])
]

OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5', 'yaml'],
    'includes': [
        'MainWindow',
        'MusicItem',
        'ParamDialog',
        'RenameDialog',
        'Settings',
        'SettingsDialog',
        'Timeline',
        'TimelineRuler',
        'TimelineView'
    ],
    'iconfile': ICON_PATH,
    'plist': {
        'CFBundleName': 'DPT',
        'CFBundleDisplayName': 'Delta Parser Timeline',
        'CFBundleGetInfoString': 'Delta Parser Timeline',
        'CFBundleIdentifier': 'com.deltaresearch.dpt',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright 2024 MIT LICENSE',
        'LSMinimumSystemVersion': '10.15',
        'LSArchitecturePriority': ['arm64', 'x86_64'],  # Priorità architetture
    },
    'arch': 'universal2'  # Supporto universale per Intel e Apple Silicon
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app>=0.28.0']  # Versione minima che supporta ARM64
)