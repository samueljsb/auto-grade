from setuptools import find_packages, setup


setup(
    name="auto-grade",
    version="0.1.1",
    description="Automatically give feedback in Person ActiveLearn",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["selenium", "pyyaml", "click"],
    extras_require={"dev": ["black", "isort", "mypy", "flake8", "flake8-docstrings"]},
    entry_points={"console_scripts": ["auto-grade=auto_grade.cli:cli"]},
)
