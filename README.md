# VENV Agilizer

Why install virtualenv when Python has its own internal virtual environment
manager? [venv](https://docs.python.org/3/tutorial/venv.html)

I made a script that makes Python's venv way easier to use in a more universal
way. Instead of creating the environment in your project folder ALWAYS, if a
`VENV_DIR` environment variable is set, you can by default make environments in
that directory and maybe reuse environments later.

Why install this instead of virtualenv? No reason at all. I did this to practice
argparse and other python modules. However, it takes full advantage of Python's
default modules and there is no need to install external packages in addition to
the virtual enviroment manager, potentially making this more light-weight.


### Usage

Download this repository. Then add a `venv.bat` file on windows or `venv.sh`
file in Linux with the script. Finally, add this repository's folder to PATH to
access the `venv` command pretty much universally. All that's left is to run

`venv help`

And the script will set you on your way to easily create and manage your virtual
environments. It should be very intuitive and easy to set up
