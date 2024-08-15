from pathlib import Path

import setuptools

__version__ = "0.1.2"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def get_install_requires() -> list:
    """Returns requirements.txt parsed to a list"""
    requirements_filepath = Path(__file__).parent / "requirements.txt"
    targets = []
    if requirements_filepath.exists():
        with open(requirements_filepath, "r") as f:
            targets = f.read().splitlines()
    return targets


setuptools.setup(
    name="tempmail-python3",
    version=__version__,
    author="shadMod",
    author_email="support@shadmod.it",
    description="Handle tempmail with 1secmail API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shadMod/tempmail/",
    download_url=f"https://github.com/shadMod/tempmail/archive/refs/tags/{__version__}.tar.gz",
    project_urls={
        "Documentation": "https://docs.shadmod.it/tempmail/index",
        "GitHub": "https://github.com/shadMod/tempmail/",
        "Bug Tracker": "https://github.com/shadMod/tempmail/issues/",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=["src"],
    install_requires=get_install_requires(),
    python_requires=">=3.10",
)
