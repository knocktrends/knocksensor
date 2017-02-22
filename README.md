# Knock Server

## Setup

1. Install [Python 3.6](https://www.python.org/downloads/)

2. It comes with a package manager, pip. Open a terminal and run 
```
$ sudo pip install virtualenv
```

3. Create a folder for the project
```
$ mkdir myproject
$ cd myproject
```

4. Run virtualenv setup
```
$ virtualenv venv
New python executable in venv/bin/python
Installing setuptools, pip............done.
```

5. Clone the repository
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

To exit, use
```
$ deactivate
```

## Running the Server
After entering a virtual environment with the activate command, check for any dependency updates with

```
$ pip install -r requirements.txt
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