import os
import shlex
import subprocess
import sys

from setuptools import setup

pkg_name = "astronomia"

version = open("VERSION").readline().strip()

if sys.argv[-1] == "publish":
    subprocess.run(shlex.split("cleanpy ."), check=True)
    subprocess.run(shlex.split("python setup.py sdist"), check=True)
    subprocess.run(
        shlex.split(f"twine upload dist/{pkg_name}-{version}.tar.gz"), check=True
    )
    sys.exit()

setup(
    data_files=[
        (
            os.path.join("share", "astronomia"),
            [os.path.join("params", "astronomia_params.txt")],
        )
    ],
)
