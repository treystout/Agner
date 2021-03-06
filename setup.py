from setuptools import setup, Command

class PyTest(Command):
  user_options = []
  def initialize_options(self):
    pass
  def finalize_options(self):
    pass
  def run(self):
    import sys, subprocess
    errno = subprocess.call([sys.executable, 'runtests.py'])
    raise SystemExit(errno)

setup(
    name="Agner",
    description="simple data-only queueing system backed by Redis",
    author="Trey Stout",
    author_email="treystout@gmail.com",
    url="https://github.com/treystout/agner",
    version="0.2.1",
    include_package_data=True,
    packages=['agner'],
    package_data={
      '': ['lua/*.lua']
    },
    cmdclass={'test':PyTest},
)

