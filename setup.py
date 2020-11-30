import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arithmatic-parsing-wireboy5", # Replace with your own username
    version="0.0.1",
    author="Riley Wilton",
    author_email="riley.j.wilton@gmail.com",
    description="A simple, easy to use, arithmatic parsing tool, with minimal dependancies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)