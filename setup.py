from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: Apache License',
  'Programming Language :: Python :: 3'
]

setup(
  name='MechaK.py',
  version='0.0.3',
  description='Offical API Wrapper for the Mecha Karen API',
  long_description=open('README.md').read(),
  long_description_content_type = "text/markdown",
  url = "https://github.com/Seniatical/MechaK.py/", 
  project_urls={
   "Documentation": "https://github.com/Seniatical/MechaK.py/",
   "Issue tracker": "https://github.com/Seniatical/MechaK.py/issues",
   },
  author='Seniatical',
  license='Apache', 
  classifiers=classifiers,
  keywords='Wrapper,Python', 
  packages=find_packages(),
  install_requires=['requests', 'aiohttp', 'aiofiles'] 
)
