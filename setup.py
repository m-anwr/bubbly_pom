from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='BubblyPom',

    version='0.0.1',

    description='A cute app for time management and having fun',
    long_description=long_description,

    url='https://github.com/tootis/bubbly_pom',

    author='Mohamed Anwer',
    author_email='mohammed.ahmed.anwer@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='time management pomodoro fun',
    packages=['bubbly_pom'],
    install_requires=['pyqt5'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    package_data={
        "bubbly_pom": [
            "defaults/timer_settings.json",
            "resources/lollipop.png",
            "resources/note.png",
            "resources/splash.png",
            "resources/soundcloud.png",
            "resources/timer.png",
            "resources/pinterest.png"
        ]
    },

    data_files=[],

    entry_points={
        'console_scripts': [
            'bubbly_pom=bubbly_pom.__main__:main'
        ],
        'gui_scripts': [
            'bubbly_pom=bubbly_pom.__main__:main'
        ]
    },

)