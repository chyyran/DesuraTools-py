# -*- mode: python -*-
a = Analysis(['desuratools.py', 'build.spec'],
             pathex=['D:\\Coding\\Python\\DesuraTools'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='desuratools.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
