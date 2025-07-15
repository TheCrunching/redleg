#!/usr/bin/env python3
"""Simple ledger application"""

import re
import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime


__version__ = "0.1.4"

# ? Constants
# The format for the logging msg
LOGGING_FORMAT = "[%(levelname)s]: %(message)s"
# The accepted date format
DATE_FORMAT = "%Y-%m-%d"
# Account name pattern
NAME_PATTERN = re.compile(r"^(Assets|Liabilities|Equity|Revenue|Expenses).")


# Set up argument parser with the program details
parser = argparse.ArgumentParser(
    prog="RedLeg",  # Program name
    description="The simple ledger application",  # Description
    epilog="..."  # Epilog (did'nt really know what to put their)
)
# Version argument
parser.add_argument(
    "--version",
    action="version",  # Make sure argparse knows its for the version
    version=__version__,  # Pass it the version
    help="Displays the version then exits"
)
# Verbosity argument
parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    help="Increases the verbosity of the logging system"
)
parser.add_argument(
    "file",
    help="The ledger file"
)
# Set up subparser
subparsers = parser.add_subparsers(
    required=True,
    dest="command"  # Put this here so we know what command is called
)
# Subparser for register command
registerCommand = subparsers.add_parser(
    "register",
    help="Prints the register"
)
# Subparser for transaction command
transactionCommand = subparsers.add_parser(
    "transaction",
    help="Make a transaction"
)
# Subparser for account command
accountCommand = subparsers.add_parser(
    "accounts",
    help="Print the value of all accounts"
)
# Subparser for statement command
statementCommand = subparsers.add_parser(
    "statement",
    help="Prints out a statement"
)

# Parse the arguments
args = parser.parse_args()

# Get the logger for the module
logger = logging.getLogger(__name__)
# Set up the formatter object
formatter = logging.Formatter(fmt=LOGGING_FORMAT)
# Set up console handler
streamHandler = logging.StreamHandler()
# Set the formatter for the console handler
streamHandler.setFormatter(formatter)
# Add the handler to logger
logger.addHandler(streamHandler)
# Set logging level
if args.verbose == 0:
    logger.setLevel(20)  # Info
elif args.verbose == 1:
    logger.setLevel(10)  # Debug
else:
    logger.setLevel(0)  # Notset


def register_func(account_data: dict) -> str:
    """Print all transactions"""
    # Iterate over the transactions
    ledger = ""
    for transaction in account_data['transactions']:
        ledger += f"Date: {transaction['date']}\n"
        ledger += f"Description: {transaction['description']}\n"
        ledger += "Accounts: \n"
        # Iterate over the accounts
        for accounts in transaction['accounts']:
            ledger += f"\t{accounts}: {transaction['accounts'][accounts]}\n"
        # Print the transaction
        ledger += "\n"

    return ledger


def transaction_func(account_data: dict):
    """Adds a new transaction"""
    # Set up accounts dict
    accounts = {}
    # Get the date
    date = input("Date (YY-mm-dd): ")
    try:
        # Sett if date adheres to the date format
        datetime.strptime(date, DATE_FORMAT)
    except ValueError:
        logger.error(
            "Date does not conform to date format: %s", DATE_FORMAT
        )
        sys.exit(1)
    description = input("Input transaction description: ")
    get_accounts = True
    while get_accounts:
        # Get account
        name = input("Account name: ")
        # If enter pressed then break
        if name == "":
            get_accounts = False
            break
        # Make sure it matches name pattern
        if not NAME_PATTERN.match(name):
            logger.error("Name does not conform to naming conventions")
            sys.exit(1)
        # Make sure account not already used during this transaction
        if name in accounts:
            logger.error("You input an account twice")
            sys.exit(1)
        while True:
            try:
                accounts[name] = int(input("Amount: "))
                break
            except ValueError:
                logger.error("You inputted a non int as a number.")
                continue
    assets = 0
    liabilities = 0
    for account, amount in accounts.items():
        if re.compile(r"^Assets.").match(account):
            assets += amount
        elif re.compile(r"^Expenses.").match(account):
            liabilities -= amount
        else:
            liabilities += amount
    if assets != liabilities:
        logger.error("The transaction does not balance out.")
        sys.exit(1)
    # Append the transaction to the ledger
    account_data['transactions'].append(
        {
            "date": date,
            "description": description,
            "accounts": accounts
        }
    )
    # Open the file
    with open(args.file, "w", encoding="utf-8") as account_file:
        # Write the json
        json.dump(
            account_data,  # The ledger data
            account_file,  # The ledger file
            indent=4  # Indent 4 spaces, nice thing to have
        )


def accounts_func(account_data: dict) -> str:
    """Run the account command"""
    # Set up balances dict
    balances = {}
    # Iterate over all the transactions
    for transaction in account_data['transactions']:
        # Iterate over all the accounts
        for account in transaction['accounts']:
            # Add the amount to the amount in balances
            if account in balances:
                balances[account] += transaction['accounts'][account]
            else:
                balances[account] = transaction['accounts'][account]
    accounts = ""
    # Iterate over all the accounts in balances
    assets = 0
    liabilities = 0
    for account, balance in balances.items():
        # Print the account name and the balance
        accounts += f"{account}: {balance}\n"
        if re.compile(r"^Assets.").match(account):
            assets += balance
        elif re.compile(r"^Expenses.").match(account):
            liabilities -= balance
        else:
            liabilities += balance
    if assets != liabilities:
        logger.warning("Your accounts do not balance out.")

    return accounts


def statement_func(period: str, account_data: dict) -> str:
    """Generates a statement"""
    try:
        # Sett if date adheres to the date format
        datetime.strptime(period, "%Y-%m")
    except ValueError:
        logger.info(
            "Date might be a year"
        )
        try:
            datetime.strptime(period, "%Y")
        except ValueError:
            logger.error("Period does not match: YY-mm or YY")

    accounts = {}
    statement = ""

    for transaction in account_data['transactions']:
        if transaction['date'].startswith(period):
            statement += f"Date: {transaction['date']}\n"
            statement += f"Description: {transaction['description']}\n"
            statement += "Accounts:\n"
            for account, amount in transaction['accounts'].items():
                try:
                    accounts[account] += amount
                except KeyError:
                    accounts[account] = amount
                statement += f"\t{account}: {amount}\n"

    if statement == "":
        logger.warning("Period had no transactions, not generating a statement")
        sys.exit(1)

    statement += "\n\n"
    statement += "=====END=====\n"
    for account, amount in accounts.items():
        statement += f"\t{account}: {amount}\n"

    return statement


def main() -> int:
    """All application function code

    Returns:
        int: The exit code
    """

    try:
        # Open account file
        try:
            with open(args.file, mode="r", encoding="utf-8") as account_file:
                # Parse the data
                account_data = json.load(account_file)
                if not isinstance(account_data, dict):
                    raise ValueError("Invalid JSON data")
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON data") from e
        # Command register
        if args.command == "register":
            print(register_func(account_data))
        # Command transaction
        elif args.command == "transaction":
            transaction_func(account_data)
        # Command accounts
        elif args.command == "accounts":
            print(accounts_func(account_data))
        # Command statement
        elif args.command == "statement":
            period = input(
                "Please input a month or a year (YY-mm or YY): "
            )
            statement = statement_func(period, account_data)
            print(statement)
            save_to_file = input("Save to file? [Y/n]: ").lower()
            if save_to_file in ("y", ""):
                with open(
                    f"statement-{period}.txt", mode="w", encoding="utf-8"
                ) as statement_file:
                    statement_file.write(statement)
                logger.info("Statement saved successfully")
            else:
                logger.info("Not saving to file")
    # In case the file does not exist
    except FileNotFoundError:
        logger.critical("File: %s not found.", args.file)
        empty_ledger = {
            "transactions": []
        }
        try:
            with open(
                args.file,
                mode="x",
                encoding="utf-8"
            ) as account_file:
                json.dump(empty_ledger, account_file)
            logger.info("Created an empty ledger file")
        except FileNotFoundError:  # Only raised if dirs are missing
            Path(args.file).parent.mkdir(exist_ok=True, parents=True)
            sys.exit(main())  # Recall main
    # In case a name is missing in the json file
    except KeyboardInterrupt:
        logger.error("\nCtrl+C pressed, quitting...")
        return 3
    # In case they tamper with the ledger file and we get a key error
    except KeyError as e:
        logger.error("Key: '%s' was missing from ledger file.", e)

    return 0  # Success


# In case we are executing this script by itself
if __name__ == "__main__":
    # Take care of exiting just like in the hatch generated script
    sys.exit(main())
