from setuptools import setup, find_packages

setup(
    name="data-eng-cli",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "click",
        "pandas",
        "requests",
        "pyyaml"
    ],
    entry_points={
        "console_scripts": [
            "data-eng-cli = data_eng_cli.cli:cli"
        ]
    },
)
