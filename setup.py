from setuptools import setup, find_packages

setup(
    name="skill_matcher",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "spacy",
        "skillNer",
    ],
    python_requires=">=3.9",
)