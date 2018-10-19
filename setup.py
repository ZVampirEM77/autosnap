import os
import shutil
from setuptools import setup, find_packages
import distutils.command.install_scripts

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'autosnap', '__version__.py')) as f:
    exec(f.read(), about)

class StripExtension(distutils.command.install_scripts.install_scripts):
    def run(self):
        distutils.command.install_scripts.install_scripts.run(self)
        for script in self.get_outputs():
            if script.endswith(".py"):
                shutil.move(script, script[:-3])


setup(
    name = "autosnap",
    version = about['__version__'],
    author = 'Enming Zhang',
    author_email = 'zvampirem77@gmail.com',
    url = 'https://github.com/ZVampirEM77/autosnap',
    packages = find_packages(),
    scripts = ['auto_snap.py'],
    cmdclass = {"install_scripts": StripExtension}
)
