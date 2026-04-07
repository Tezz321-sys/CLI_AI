from setuptools import setup, find_packages

setup(
    name="chatgpt-cli-os-independent",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0"
    ],
    entry_points={
        "console_scripts": [
            "chatgpt=chatgpt_cli.main:main",
        ]
    },
)
