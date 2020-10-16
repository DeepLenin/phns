import setuptools

setuptools.setup(
    name="phns",
    version="0.0.1",
    author="Deep Lenin",
    description="A small package",
    python_requires=">=3.6",
    packages=setuptools.find_packages(),
    install_requires=["scipy"],
    include_package_data=True,
)
