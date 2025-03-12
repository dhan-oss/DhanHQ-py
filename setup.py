import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '2.1.0'
PACKAGE_NAME = 'dhanhq'
AUTHOR = 'Dhan'
AUTHOR_EMAIL = 'dhan-oss@dhan.co'
URL = 'https://dhanhq.co/'

LICENSE = 'MIT LICENSE'
DESCRIPTION = 'The official Python client for communicating with the DhanHQ API'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    "pandas>=1.4.3",
    "requests>=2.28.1",
    "websockets>=12.0.1",
    "pyOpenSSL>=20.0.1",
    ]

TEST_SUITE="tests"
TEST_REQUIRES = [
    "python-dotenv>=1.0.1",
    "flake8>=7.1.1",
    "pylint>=3.3.3",
    "pytest>=8.3.4",
    "pytest-cov>=6.0.0",
    "responses>=0.25.3",
    ]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      package_dir={'': 'src'}, # Tells setuptools where your code is
      packages=find_packages(where='src'), # Automatically find packages
      install_requires=INSTALL_REQUIRES,
      extras_require={
          'dev': TEST_REQUIRES
      },
      )
