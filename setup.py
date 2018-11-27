"""
Flask-ac
--------

Flask-ac provide role based access control(rbac) for Flask.

This plugin implement tree-like permission structure for access control.
Flask-ac is not implement persistent storage of user, roles and permissions,
instead using self-defined loaders to load data from anywhere you want.

"""


from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='Flask-AC',
    version='0.0.2',
    url='',
    license='MIT',
    author='Jiaqi Guo',
    author_email='gawain_guo@hotmail.com',
    description='Flaks access control extension',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    py_modules=['flask_ac'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
