import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="titulus",
    version="0.0.1",
    author="Antoine Simoulin",
    author_email="antoine.simoulin@gmail.com",
    description="Text visualization python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AntoineSimoulin/titulus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
