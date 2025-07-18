# RedLeg

RedLeg is a simple dual entry ledger program.

Join my [discord](https://discord.com/invite/X9SB5Znm2D) if you have any questions.

## Install

You can install with `pip install redleg`.

## Usage

```terminal
$ redleg -h
usage: RedLeg [-h] [--version]
              file {register,transaction,accounts,statement} ...

The simple ledger application

positional arguments:
  file                  The ledger file
  {register,transaction,accounts,statement}
    register            Prints the register
    transaction         Make a transaction
    accounts            Print the value of all accounts
    statement           Prints out a statement

options:
  -h, --help            show this help message and exit
  --version             Displays the version then exits

...
```

## Exit codes

| Code       | Meaning        |
|------------|----------------|
| 0          | Success        |
| 1          | Error          |
| 2          | Argparse error |
| 3221225786 | Ctrl+C         |

## FAQ

### Why does it allow me to set the date and not get the date from datetime?

The reasoning behind this is that you might record a transaction a day or two after it happens
