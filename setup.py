#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from pathlib import Path

# 讀取 README.md 做為長描述
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="tw-tech-terminology-converter",
    version="1.0.0",
    author="Taiwan Tech Terminology Converter Contributors",
    description="繁體中文（台灣）與簡體中文（中國大陸）技術術語轉換工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LZong-tw/tw-tech-terminology-converter",
    packages=find_packages(),
    py_modules=["tech_terminology_converter", "cli"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: Chinese (Traditional)",
        "Natural Language :: Chinese (Simplified)",
    ],
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "tw-tech-converter=cli:main",
        ],
    },
    package_data={
        "": ["terminology.json"],
    },
    include_package_data=True,
    keywords="chinese taiwan terminology converter tech translation 繁體中文 台灣 術語轉換",
)