from setuptools import setup, find_packages
classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'License :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(
    name                ='FaBo3Axis-ADXL345-Python',
    version             ='1.0.0',
    description         ="This is a library for the FaBo 3AXIS I2C Brick.",
    author              ='FaBo',
    author_email        ='info@fabo.io',
    url                 ='https://github.com/FaBoPlatform/FaBo3Axis-ADXL345-Python/',
    license             ='MIT',
    classifiers         = classifiers,
    packages            =find_packages(),
    include_package_data=True,
    zip_safe            =True,
    long_description    =read_md('README.md')
)
