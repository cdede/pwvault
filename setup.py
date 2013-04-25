import sys

from distutils import sysconfig
from distutils.core import setup

try:
    import os
except:
    print ('')
    sys.exit(0)

setup(
    name = "lewm",
    author = "",
    author_email = "",
    version = "0.9.13",
    license = "GPL3",
    description = "commandline get keepassx password",
    long_description = "README.md",
    url = "http://github.com/cdede/lewm/",
    platforms = 'POSIX',
    packages = ['lib_lewm' ],
    data_files = [
        (
            sysconfig.get_python_lib() + '/lib_lewm',
            [
                './README.md'
            ]
        )
    ],
    scripts = ['lewm']
)
