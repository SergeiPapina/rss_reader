from setuptools import setup, find_packages

with open("requirements/requirements.txt") as f:
    required = f.read().splitlines()

setup(
    version="1.0",
    packages=find_packages(where="rss_reader", exclude=["tests"]),
    install_requires=required,
    name="rss_reader",
    author="Siarhei_Papina",
    author_email="Siarhei_Papina@epam.com",
    description="RSS feed reader",
    classifiers=["Programming Language :: Python :: 3"],
    python_requires=">=3.9",
    package_dir={"": "rss_reader"},
    include_package_data=True
)