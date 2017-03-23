Rogue Dungeon
=============

Learn programming in Python while building a classical Hack-and-Slash game!

## Requirements

- Python3.5+
- virtualenv
- SDL2+

## Installation

As a good practice make sure you use a virtualenv for this project.

Navigate to the project directory and run the ff:

Linux:

```
> python3 -m venv venv
> ./venv/bin/activate
> pip install -r requirements.txt
```

Windows:

```
> python3 -m venv venv
> venv/Scripts/activate
> pip install -r requirements.txt
```


## Troubleshooting installation

### SDL issues

This module mainly requires the `libtcod-cffi` library requirements for your
OS.

Reference: https://pypi.python.org/pypi/libtcod-cffi

For Ubuntu users run the `requirements/linux_build.sh` script first before
installing the pip requirements.

Other linux users, please find equivalent packages in that script.

Once you have installed these requirements re-install the pip requirements
with:

```
pip install -I -r requirements.txt
```

### `bdist_wheel` issues

If you get an error saying:

```
error: error in setup.cfg: command 'bdist_wheel' has no such option 'py_limited_api'
```

You may safely ignore this.

