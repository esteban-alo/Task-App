"""
Proyect by Esteban Rodriguez
Esteban_Alo
"""

from setuptools import setup

setup(
    name='taskapp',
    packages=['taskapp'],
    include_package_data=True,
    install_requires=[
        'flask',
        'mongoengine',
    ],
)
