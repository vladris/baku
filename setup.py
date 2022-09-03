from setuptools import setup, find_packages
import baku

long_desc = 'Baku is a simple, Markdown-based blogging engine/static website generator.'

requires = ["Pygments>=2.13.0", "misaka>=2.1.1"]

setup(
    name = "Baku",
    version = baku.__version__,
    url = "http://github.com/vladris/baku/",
    download_url = "http://pypi.python.org/pypi/baku",
    license = "MIT",
    author = "Vlad Riscutia",
    author_email = "vladris@outlook.com",
    description = "Simple, Markdown-based blogging engine",
    long_description = long_desc,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Communications",
        "Topic :: Internet"
    ],
    platforms = "any",
    include_package_data = True,
    entry_points = {
        "console_scripts": [
            "baku = baku.cmdline:main"
        ]
    },
    install_requires = requires,
)