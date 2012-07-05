from distutils.core import setup

from pypercube import __version__

setup(
        name='pypercube',
        version=__version__,
        description='A Cube API client in python.',
        long_description="An easy way to use Cube's API in python",
        author='Steven Buss',
        author_email='steven.buss@gmail.com',
        url='https://github.com/sbuss/pypercube',
        download_url='https://github.com/sbuss/pypercube/'\
                'tarball/v%s' % __version__,
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2.7",
        ],
        packages=[
            'pypercube',
        ],
)
