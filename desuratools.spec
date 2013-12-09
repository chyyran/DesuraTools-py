# -*- mode: python -*-
a = Analysis(['desuratools.py'],
             pathex=['D:\\Coding\\Python\\DesuraTools'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='desuratools.exe',
          debug=False,
          strip=None,
          upx=False,
          console=False , version='versioninfo.txt', icon='icons\\desuratools.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=False,
               name='desuratools')
