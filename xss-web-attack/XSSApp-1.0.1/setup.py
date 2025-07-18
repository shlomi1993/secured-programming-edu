from distutils.core import setup
from setuptools import find_packages

import os

requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
with open(requirements_path, "r") as f:
    dependencies = list(f)


setup(name='XSSApp',
      version='1.0.1',
      description='Secure Programming XSS application',
      author='Secure Programming BIU 2022',
      packages=find_packages(),
      install_requires=dependencies,
      include_package_data=True,
      entry_points={
          "console_scripts": [
              "start_xss_app = XSSApp.app:start_app"
          ]
      }
      )
