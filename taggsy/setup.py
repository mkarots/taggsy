from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='taggsy',
    version='0.1.0',
    description='Count most common words in a collection of documents',
    long_description=readme,
    author='Michael Karotsieris',
    author_email='michael.karotsieris@gmail.com',
    url='https://github.com/michael-karotsieris/taggsy',
    license=license,
    setup_requires=['nose==1.0'],
    packages=find_packages(exclude=('tests'))
)