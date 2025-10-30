# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for IENDLoader - Windows ARM64
# Build command: pyinstaller build_modern_windows_arm64.spec

block_cipher = None

a = Analysis(
    ['iendloader.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['customtkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'PIL',
        'pytest',
        'setuptools',
    ],
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
    name='IENDLoader_ARM64.exe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for stealth
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='arm64',  # ARM64 Windows
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
