#!/usr/bin/env python3
"""Simple ledger application"""

import re
import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime


__version__ = "0.1.0"

# ? Constants
# The format for the logging msg
LOGGING_FORMAT = "%(asctime)s [%(levelname)s]: \"%(message)s\""
# The format for the date in the logging message
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
# The accepted date format
DATE_FORMAT = "%d-%m-%Y"
# Account name pattern
NAME_PATTERN = re.compile(r"^(Assets|Liabilities|Equity|Revenue|Expenses).")
# Account file
ACCOUNT_FILE_DIR = Path(Path.home(), ".redleg")
if not ACCOUNT_FILE_DIR.exists():
    ACCOUNT_FILE_DIR.mkdir()
ACCOUNT_FILE = Path(ACCOUNT_FILE_DIR, "ledger.json")


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
# Set up subparser
subparsers = parser.add_subparsers(
    required=True,
    dest="command"  # Put this here so we know what command is called
)
registerCommand = subparsers.add_parser(
    "register",
    help="Prints the register"
)
transactionCommand = subparsers.add_parser(
    "transaction",
    help="Make a transaction"
)
accountCommand = subparsers.add_parser(
    "accounts",
    help="Print the value of all accounts"
)

# Parse the arguments
args = parser.parse_args()

# Get the logger for the module
logger = logging.getLogger(__name__)
# Set up the formatter object
formatter = logging.Formatter(fmt=LOGGING_FORMAT, datefmt=LOGGING_DATE_FORMAT)
# Set up console handler
streamHandler = logging.StreamHandler()
# Set the formatter for the console handler
streamHandler.setFormatter(formatter)
# Add the handler to logger
logger.addHandler(streamHandler)
# Set logging level
if args.verbose == 0:
    logger.setLevel(30)  # Warning
elif args.verbose == 1:
    logger.setLevel(20)  # Info
elif args.verbose == 2:
    logger.setLevel(10)  # Debug
else:
    logger.setLevel(0)  # Notset


def main() -> int:
    """All application function code

    Returns:
        int: The exit code
    """

    try:
        # Open account file
        with open(ACCOUNT_FILE, mode="r", encoding="utf-8") as account_file:
            # Parse the data
            account_data = json.load(account_file)
        # Command register
        if args.command == "register":
            # Iterate over the transactions
            for transaction in account_data['transactions']:
                transactions = ""
                # Iterate over the accounts
                for accounts in transaction['accounts']:
                    transactions += f"\t{accounts}: {transaction['accounts'][accounts]}\n"
                # Print the transaction
                print(f"Date: {transaction['date']}")
                print(f"Description: {transaction['description']}")
                print("Accounts:")
                print(transactions)
        # Command transaction
        elif args.command == "transaction":
            # Set up accounts dict
            accounts = {}
            # Get the date
            date = input("Date (dd-mm-YY): ")
            try:
                # Sett if date adheres to the date format
                datetime.strptime(date, DATE_FORMAT)
            except ValueError:
                logger.error(
                    "Date does not conform to date format: %s", DATE_FORMAT
                )
                return 1
            description = input("Input transaction description: ")
            get_accounts = True
            while get_accounts:
                # Get account
                name = input("Account name: ")
                # If equal to DONE the return
                if name == "DONE":
                    get_accounts = False
                    break
                # Make sure it matches name pattern
                if not NAME_PATTERN.match(name):
                    logger.error("Name does not conform to naming conventions")
                    return 1
                # Make sure account not already used during this transaction
                if name in accounts:
                    logger.error("You input an account twice")
                    return 1
                try:
                    # Get change in value
                    accounts[name] = int(input("Amount: "))
                except ValueError:
                    logger.error("You inputted a non int as a number.")
                    return 1
            transaction_balance = 0
            for account in accounts:
                transaction_balance += accounts[account]
            if transaction_balance != 0:
                logger.error("The transaction does not balance out.")
                return 1
            # Append the transaction to the ledger
            account_data['transactions'].append(
                {
                    "date": date,
                    "description": description,
                    "accounts": accounts
                }
            )
            # Open the file
            with open(ACCOUNT_FILE, "w", encoding="utf-8") as account_file:
                # Write the json
                json.dump(
                    account_data,  # The ledger data
                    account_file,  # The ledger file
                    indent=4  # Indent 4 spaces, nice thing to have
                )
        # Command accounts
        elif args.command == "accounts":
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
            # Iterate over all the accounts in balances
            for account, balance in balances.items():
                # Print the account name and the balance
                print(f"{account}: {balance}")
    # In case the file does not exist
    except FileNotFoundError:
        logger.critical("File: %s not found.", ACCOUNT_FILE)
        empty_ledger = {
            "transactions": []
        }
        with open(
            ACCOUNT_FILE,
            mode="x",
            encoding="utf-8"
        ) as account_file:
            json.dump(empty_ledger, account_file)
        logger.info("Created an empty ledger file")
    # In case a name is missing in the json file

    return 0  # Success


if __name__ == "__main__":
    sys.exit(main())
