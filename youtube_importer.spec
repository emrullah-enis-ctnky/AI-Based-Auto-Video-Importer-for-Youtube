# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import customtkinter

# Find customtkinter path to include its theme files
ctk_path = os.path.dirname(customtkinter.__file__)

block_cipher = None

added_files = [
    ('src/assets', 'src/assets'),
    ('src/gui/assets', 'src/gui/assets'),
    (ctk_path, 'customtkinter'),
]

a = Analysis(
    ['main.py'],
    pathex=['.', 'src'],
    binaries=[],
    datas=added_files,
    hiddenimports=['PIL._tkinter_finder', 'rich', 'rich._unicode_data.unicode17-0-0', 'rich._unicode_data', 'rich.logging', 'dotenv', 'tkinter.filedialog', 'customtkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='youtube_importer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/assets/icon.png',
)
