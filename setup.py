from setuptools import setup, find_packages

app_name = "rssr-daemon"

setup(
    name=appname,
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': ['{} = {}.__main__:main'.format(appname)]
    },
)
