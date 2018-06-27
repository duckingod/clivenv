#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
bash_output = lambda *s: subprocess.check_output(s, stderr=subprocess.STDOUT).decode()

USE_ENV_BASH="""#!/bin/bash
export VENV_RUNNING=1
alias pip=venv_pip_recording
unvenv () {
    unset VENV_RUNNING
    unset -f unvenv
    unalias pip
    deactivate
}
"""
PYTHON_CMDS = ['python', 'python3', 'python2'] + ['python3.' + str(p) for p in range(1, 8)]
DEFAULT_PYTHON = 'python'

class Env(object):
    class TmpFile(object):
        NAME = 'tmp'
        def __init__(self, path, ss, delete=True):
            self.path = path + '/' + self.NAME
            self.ss = ss
            self.delete = delete
            with open(self.path, 'w') as f:
                for s in self.ss:
                    f.write(s+'\n')
        def __enter__(self):
            return self.path
        def __exit__(self, type, value, traceback):
            if self.delete:
                os.remove(self.path)
    BASE = '.venv/'
    base = '.venv/'
    def __init__(self, py_cmd=None):
        if py_cmd:
            try:
                self.ver = bash_output(py_cmd, '-V').split()[1]
                self.py_path = bash_output('which', py_cmd)
            except OSError as e:
                self.ver = '-1'
                self.py_path = ''
        else: # load current virtualenv
            self.ver = os.environ['VIRTUAL_ENV'].split('/')[-1]
            self.py_path = '' 
            self.base = os.path.dirname(os.environ['VIRTUAL_ENV']) + '/'
        self.name = self.ver
        self.path = self.base + self.name + '/'
        self.activate_path = self.path + 'bin/activate'
        self.pip_log_path = self.base + 'pip_log.txt'

    @property
    def exists(self):
        return os.path.exists(self.path)
        
    def use(self):
        # from https://stackoverflow.com/a/6944649
        s = [USE_ENV_BASH]
        s.append('. ' + self.activate_path)
        self.TmpFile(self.base, s, delete=False)
    def leave(self):
        os.system('unvenv')
        
    def create(self):
        return os.system('virtualenv ' + self.path + ' --python=' + self.py_path)

    def delete(self):
        os.system('rm -R ' + self.path + '*')
        pip_log = self.path[:-1] + '-pip'
        if os.path.exists(pip_log):
            os.system('rm ' + pip_log)
        os.rmdir(self.path)

    def make_requirements(self, backward):
        from collections import defaultdict
        packages = defaultdict(lambda: [])
        for f in os.listdir(self.base):
            if f[-4:] == '-pip':
                with open(self.base + f) as f:
                    for l in f:
                        n, v = l.split('==')
                        packages[n] = packages[n] + [v]
        with open(self.base + 'requirements.txt', 'w') as f:
            oper = '<=' if backward else '>='
            for p, vs in packages.items():
                f.write(p + ','.join([oper+v for v in vs]))
        return self.base + 'requirements.txt'

def main():
    description="""
    Create virtual env and enter by
    >>> . venv

    Create virtual env for python3 and enter by
    >>> . venv python3

    Delete virtual env and enter by
    >>> venv delete

    Delete virtual env for python3 by
    >>> venv delete python3

    Sync pip packages among all virtual env
    >>> venv sync

    If inside a venv, and python command not provided, then current venv is used.
    """
    parser = argparse.ArgumentParser(
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    actions = ['use', 'delete', 'sync', 'updatepip']
    parser.add_argument(
            'actions',
            nargs='*', help='{auto, python, python3, ...} or {'+', '.join(actions)+'}, default: auto and use')
    parser.add_argument('-b', help='Using older package when sync pip', dest='pip_backward', action='store_true')
    args = parser.parse_args()
    args.py_cmd = ([a for a in args.actions if a not in actions] + ['auto'])[0]
    args.action = ([a for a in args.actions if a     in actions] + ['use'])[0]
    if args.py_cmd != 'auto':
        env = Env(args.py_cmd)
    elif 'VENV_RUNNING' in os.environ:
        env = Env()
    else:
        pythons = [p for p in PYTHON_CMDS if Env(p).exists] + [DEFAULT_PYTHON]
        env = Env(pythons[0])
    print('Virtual env: Python' + env.ver)
    if not env.exists:
        print('Environment not exists.')
        res = input('Create one? [Y/n]')
        if res != 'n':
            env.create()
        else:
            exit()
    if args.action == 'use':
        env.use()
    if args.action == 'delete':
        res = input('Delete virtual env? [y/N]')
        if res == 'y':
            print('Deleting ...')
            env.delete()
            print('Done')
    if args.action == 'sync':
        print('Syncing pip')
        requirements = env.make_requirements(args.pip_backward)
        os.system('pip install -r ' + requirements)

if __name__ == '__main__':
    main()

