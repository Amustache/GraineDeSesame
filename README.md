# GraineDeSesame

Application de vulgarisation sur les mots de passe.

## How to setup

Needed: Python 3.12+

- [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)/[Download](https://docs.github.com/en/get-started/start-your-journey/downloading-files-from-github)/[Fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) that repository.
  - e.g., `git clone https://github.com/Amustache/GraineDeSesame; cd GraineDeSesame`
- Create a [virtual environment](https://docs.python.org/3/library/venv.html) and activate it.
  - `python -m venv env; source env/bin/activate`
- [Install the dependencies](https://docs.python.org/3/installing/index.html).
  - `pip install -r requirements.txt`
- Copy the `config.py.dist` file into a `config.py` file and modify it.
  - e.g., `cp app/config.py.dist app/config.py; nano app/config.py`

## How to use

- If not done already, go into your project folder.
  - e.g., `cd /path/to/GraineDeSesame`
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

## Workflow

```mermaid
flowchart TD
    A[Password input + stats] --> B([Comment fonctionne un mot de passe ?]) --> C([Explications sur le chiffrage]) --> D[Tentative de crack + cluster] --> E([Résultats])
    E --> F([Pas bien faut faire mieux])
    E --> G([Bravo c'est très bien + diplôme])
    F --> H([Conseils + bonbon])
    G --> H
```

## Credits
- [Hive Systems](https://www.hivesystems.com/)'s [Are Your Passwords in the Green?](https://www.hivesystems.com/blog/are-your-passwords-in-the-green) (2025).
- [Connor Finley](https://gist.github.com/cofinley)'s [French Frequency List](https://gist.github.com/cofinley/262765821e4defbc8ff2bdb3356a853b) (2025).
- [Maxime Alay-Eddine](https://github.com/tarraschk)'s [Richelieu](https://github.com/tarraschk/richelieu), a list of the most common French passwords (2019).
- [Dropbox](https://github.com/dropbox)'s [zxcvbn](https://github.com/dropbox/zxcvbn), a a password strength estimator (2017).
  - I modified it to add the two previous lists + translate strings into French.