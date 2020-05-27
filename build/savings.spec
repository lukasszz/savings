# -*- mode: python -*-

block_cipher = None


a = Analysis(['../savings/savings.py'],
             pathex=['../savings'],
             binaries=[],
             datas=[('../savings/alembic/env.py', 'alembic'), ('../savings/alembic/versions/*', 'alembic/versions'), ('../savings/alembic.ini', '.'), ('../resources/Savings.ico', '.')],
             hiddenimports=['PySide2.QtXml'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='savings',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='../resources/Savings.ico')

additional_files = [
    ('db_template.sqlite', '../savings/db_template.sqlite', 'DATA'),
]
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               additional_files,
               strip=False,
               upx=True,
               name='savings')
