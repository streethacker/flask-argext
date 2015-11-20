from setuptools import setup, find_packages


requires = []

setup(
    name='flask_argext',
    version='0.1',
    description='Auto-check and convert parameters of request',
    author='YUCHI',
    author_email='wei.chensh@ele.me',
    packages=find_packages(),
    url='https://github.com/streethacker/flask_argext',
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
)
