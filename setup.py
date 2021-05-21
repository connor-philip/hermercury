from sys import modules
from setuptools import setup, find_packages

setup(name="hermercury",
      version="1.0.0",
      author="Connor Philip",
      author_email="connorphilip12@hotmail.com",
      package_dir={"hermercury": "modules"},
      packages=["hermercury"]
      )
