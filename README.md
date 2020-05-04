# Auto Grade

## Automatically give feedback in Person ActiveLearn

This is a script to automate Chrome to automatically provide feedback to all completed tasks in Pearson ActiveLearn.
The script will only give feedback for configured groups.

## Installation

Make sure you have [Python 3.6][python] installed.

```shell
python -m pip install .
```

## Usage and Configuration

Copy the `config.yaml` file:

```shell
cp config.yaml.example config.yaml
```

and fill in the values for your ActiveLearn teacher's username and password.

Run the tool with

```shell
auto-grade
```

You can also specify the config file:

```shell
auto-grade my-config.yaml
```

[python]: https://www.python.org/
