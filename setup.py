from distutils.core import setup

setup(name="hermercury",
      version="1.0.0",
      author="Connor Philip",
      author_email="connorphilip12@hotmail.com",
      package_dir={"hermercury": "modules"},
      py_modules=["hermercury.notify", "hermercury.rss", "hermercury.process_control", "hermercury.helper_functions"],
      )
