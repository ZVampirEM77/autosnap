from setuptools import setup, find_packages
import distutils.command.install_scripts
import shutil

class StripExtension(distutils.command.install_scripts.install_scripts):
    def run(self):
        distutils.command.install_scripts.install_scripts.run(self)
        for script in self.get_outputs():
            if script.endswith(".py"):
                shutil.move(script, script[:-3])


setup(
    name = "autosnap",
    version = "0.1",
    author = 'Enming Zhang',
    author_email = 'zvampirem77@gmail.com',
    url = 'https://github.com/ZVampirEM77/autosnap',
    packages = find_packages(),
    scripts = ['auto_snap.py'],
    cmdclass = {"install_scripts": StripExtension}
)
