# Flask Project Base

I got fed up of doing the same thing over and over again.

## What's inside?

- A very simple [Flask](https://flask.palletsprojects.com/en/stable/) boilerplate, with [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/) and [blueprints](https://flask.palletsprojects.com/en/stable/blueprints/).
- [Bootstrap](https://getbootstrap.com/) v5.3.5.
- [An HTML base](https://getbootstrap.com/docs/5.3/examples/) for showcase.

## How to setup

Needed: Python 3.12+

- [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)/[Download](https://docs.github.com/en/get-started/start-your-journey/downloading-files-from-github)/[Fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) that repository.
  - e.g., `git clone https://github.com/Amustache/Flask-Project-Base; cd Flask-Project-Base`
- Create a [virtual environment](https://docs.python.org/3/library/venv.html) and activate it.
  - `python -m venv env; source env/bin/activate`
- [Install the dependencies](https://docs.python.org/3/installing/index.html).
  - `pip install -r requirements.txt`
- Copy the `config.py.dist` file into a `config.py` file and modify it.
  - e.g., `cp app/config.py.dist app/config.py; nano app/config.py`

## How to use

- If not done already, go into your project folder.
  - e.g., `cd /path/to/Flask-Project-Base`
- If not done already, activate your virtual environment.
  - `source env/bin/activate`
- Launch Flask webapp.
  - `python wsgi.py`

## How to dev

- This project uses various tool with `pre-commit` for code quality.
  - `pre-commit install`
- Once it is done, code quality will be done for each commit.
  - e.g., `git add .; git commit -m "commit message"`
- You can run `pre-commit` on all files to clean everything.
  - `pre-commit run --all-files`
- You can skip `pre-commit` if needed.
  - e.g., `git commit --no-verify -m "commit message"`
