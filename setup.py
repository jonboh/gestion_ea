from distutils.core import setup
import py2exe

# execute in terminal with:
# python setup.py py2exe

setup(
    windows=[{'script': 'ui_tk.py'}],
)