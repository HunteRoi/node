# Node

This project is a Python application designed to be used as a distributed system for communities to share ideas
and opinions. It can be run on any machine that has Python 3.12 or higher installed.

## Getting started
You first need to update your pre-commit hook. For that, run the following command:
```shell
$ python -m venv venv

# On Windows
$ source "venv/Scripts/activate"
# On Linux
$ sudo bash ./venv/bin/activate.sh

$ pip install -r requirements.txt
$ pre-commit install
```

Those commands will create a virtual environment named "venv" in which the project's requirements will be installed.
The latest line does the update of your pre-commit hook (which you can find in the .git/hooks folder).

The next step is to validate that your pre-commit hook runs on your virtual environment.
For that, you can run the following command:
```shell
# On Windows
$ ./pre-commit-adapt.sh
# On Linux
$ sudo bash ./pre-commit-adapt.sh
```
