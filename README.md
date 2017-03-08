# Knock Server

## Setup

Install [Python 3.6](https://www.python.org/downloads/)

It comes with a package manager, pip. Open a terminal and run 
```
$ sudo pip install virtualenv
```

Create a folder for the project
```
$ mkdir myproject
$ cd myproject
```

Run virtualenv setup
```
$ virtualenv venv
New python executable in venv/bin/python
Installing setuptools, pip............done.
```

Clone the repository
```
$ git clone https://github.com/knocktrends/knocksensor.git
```

## Using venv

To do development or run the server, enter the environment using:

OSX/Linux
```
$ . venv/bin/activate
```

Windows
```
$ venv\Scripts\activate
```

When you are done coding, to exit, use
```
$ deactivate
```

## Running the Server
After entering a virtual environment with the activate command, check for any dependency updates with

```
$ pip install -r requirements.txt
```

Initialize the database. This must be done any time the schema of a model changes. (rm the old db first)
```
$ python
>>> from knockserver.database import init_db
>>> init_db()
```

Then to run use
```
$ python run.py

* Running on http://127.0.0.1:5000/ (Press CTRL+C) to quit)
* Restarting with stat
* Debugger is active!
* Debugger pin code: 122-640-557
```

Enter the [URL](http://127.0.0.1:5000/) into your web browser and the index page should load
