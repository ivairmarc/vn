
import os
import py_compile





try:
    os.mkdir('C:\\ProgramData\\ts-bin')
    print('.....')
    
except Exception as e:
    pass
py_compile.compile('fomm\\main-cli.py')



exit(69)