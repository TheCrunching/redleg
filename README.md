# RedLeg

RedLeg is a simple dual entry ledger program.

Join my [discord](https://discord.com/invite/X9SB5Znm2D) if you have any questions.

## Usage

```terminal
$ redleg -h
usage: RedLeg [-h] [--version] [-v] {register,transaction,accounts} ...

The simple ledger application

positional arguments:
  {register,transaction,accounts}
    register            Prints the register
    transaction         Make a transaction
    accounts            Print the value of all accounts

options:
  -h, --help            show this help message and exit
  --version             Displays the version then exits
  -v, --verbose         Increases the verbosity of the logging system

...

```

## Exit codes

| Code | Meaning |
|------|---------|
| 0    | Successful |
| 1    | Error |
| 2    | Argparse error |

## FAQ

### Why does it allow me to set the date and not get the date from datetime?

The reasoning behind this is that you might record a transaction a day or two after it happens

### What is the date format?

YY-mm-dd
