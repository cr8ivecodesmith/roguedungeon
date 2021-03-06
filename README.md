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
(venv) > pip install -r requirements.txt
```

Windows:

```
> python3 -m venv venv
> venv/Scripts/activate
(venv) > pip install -r requirements.txt
```


## Running the game

Make sure the virtualenv is activated.

```
(venv) > python play.py
```

## Movement

```
h (left)
j (down)
k (up)
l (right)
y (up, left)
u (up, right)
b (down, left)
n (down, right)

i (show inventory)
d (drop inventory)
g (pick item)
< (go downstairs)
> (go upstairs)

[esc] (save and exit game)
```


## Module overview

#### Handle controls

```
rogue\handlers\action.py
rogue\utils\controls.py
```

#### Handle entity generation

```
rogue\spawn.py
```

#### Handle entity behavior and attributes

```
rogue\entities\generic.py
rogue\entities\player.py
rogue\entities\components\fighters.py
rogue\entities\components\loot.py
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

