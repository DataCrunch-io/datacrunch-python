import setuptools

version = {}
with open("datacrunch/__version__.py") as fp:
    exec(fp.read(), version)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datacrunch",
    version=version['VERSION'],
    author="DataCrunch Oy",
    author_email="info@datacrunch.io",
    description="Official Python SDK for DataCrunch Public API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DataCrunch-io",
    packages=setuptools.find_packages(),
    install_requires=['requests>=2.25.1,<3'],
    extras_require={
        'dev': [''],
        'test': ['pytest>=6.2.1,<7',
                 'pytest-cov>=2.10.1,<3',
                 'pytest-responses>=0.4.0,<1',
                 'responses>=0.12.1,<1']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English"
    ],
    python_requires='>=3.6',
)
