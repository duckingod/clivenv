# CLI\_VENV

Fast access/manage to [virtualenv](https://github.com/pypa/virtualenv) between different python versions.

Like
```bash=
user@host$ . venv
Virtual env: Python3.6.4
(3.6.4) user@host$ python -V
Python 3.6.4
(3.6.4) user@host$ unvenv
user@host$
```

Install by
```
pip install cli_venv
```

## Example

Use/create default/specific virtualenv in this directory
```bash=
    . venv

    Virtual env: Python2.7.13
    Environment not exists.
    Create one? [Y/n]y
    ...
    (2.7.13) duck@host:~/venv$
```
```
    . venv python3

    Virtual env: Python3.6.4
    Environment not exists.
    Create one? [Y/n]y
    ...
    (3.6.4) duck@host:~/venv$
```

Sync packages in other virtualenv to current virtualenv
```bash=
    venv sync
```

Exit virtual env
```bash=
    unvenv
```

Delete default/specific virtualen
```bash=
    venv delete 
    venv delete python3
```

