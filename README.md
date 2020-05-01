# Auto Grade

## Automatically give feedback in Person ActiveLearn

This is a script to automate Chrome to automatically provide feedback to all completed tasks in Pearson ActiveLearn.
The script will only give feedback for configured groups.

## Installation

Make sure you have [Python 3.8.0][python] or higher and [Poetry][poetry] installed.

```shell
poetry install --no-dev
```

## Usage and Configuration

Copy the `config.yaml` file:

```shell
cp config.yaml.example config.yaml
```

and fill in the values for your ActiveLearn teacher's username and password.

Run the tool with

```shell
poetry run python -m auto_grade
```

[python]: https://www.python.org/
[poetry]: https://python-poetry.org
