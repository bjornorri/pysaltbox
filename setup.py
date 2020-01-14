import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysaltbox",
    version="0.1.0",
    author="Björn Orri Saemundsson",
    author_email="bjornorri@gmail.com",
    description="Interface with your Salt Fiber Box router in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bjornorri/pysaltbox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
