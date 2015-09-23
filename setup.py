from setuptools import setup, find_packages

setup(
    name=appname,
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': ['rssr-daemon = rssr.__main__:main']
    },
)
