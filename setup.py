from setuptools import setup, find_packages


with open( "requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

setup(
    name="acoustid-match",
    version="0.1.0",
    description="Demonstration of the AcoustID algorithm, packaged as a Django app",
    license="MIT",
    author="dnknth",
    url="https://github.com/dnknth/acoustid-match",
    packages=find_packages('.'),
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries'
    ],
)
