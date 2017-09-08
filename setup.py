from setuptools import setup

setup(
    name = "wizard",
    packages = ["wizard"],
    entry_points = {
        "console_scripts": ['wizard = wizard.wizard:main',
                            'wd = wizard.wizard:main',
                            'gdl = wizard.gdrive_download:main']
        },
    version = 1.0,
    description = "the wizard.",
    author = "b",
    )
