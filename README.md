# RedLeg

RedLeg is a simple dual entry ledger program.

## Usage

```terminal
$ redleg
usage: RedLeg [-h] [--version] [-v {0,1,2}]
              {register,transaction,accounts} ...

The simple ledger application

positional arguments:
  {register,transaction,accounts}
    register            Prints the register 'RedLeg register -h'
    transaction         Make a transaction 'RedLeg transaction -h)
    accounts            Print the value of all accounts 'RedLeg accounts -h'

options:
  -h, --help            show this help message and exit
  --version             Displays the version then exits
  -v, --verbose {0,1,2}
                        Increases the verbosity of the logging system

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

dd-mm-YY
