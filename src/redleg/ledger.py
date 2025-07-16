#!/usr/bin/env python3
"""Ledger code"""

import io
import re
import sys
import json
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

# The accepted date format
DATE_FORMAT = "%Y-%m-%d"
# Account name pattern
NAME_PATTERN = re.compile(r"^(Assets|Liabilities|Equity|Revenue|Expenses).")


class LedgerFile:
    """Handles ledger file access
    """

    def __init__(self, file: str, mode: str):
        self.filename = Path(file)
        self.mode = mode
        self.file = None
        self.account_data = None

    def __enter__(self):
        try:
            if self.filename.stat().st_size == 0:
                self.create()
                logger.warning("Ledger file empty so created a blank ledger")
            self.open_file()
        # In case the file does not exist
        except FileNotFoundError:
            logger.error(
                "File: %s not found. Attempting to create an empty ledger",
                self.file
            )
            try:
                self.create()
                self.open_file()
            except FileNotFoundError:  # Only raised if dirs are missing
                logger.error(
                    "Directory's in the path to the file were missing."
                )
                sys.exit(1)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        if exc_type is not None:
            logger.error("%s: %s", exc_type, traceback)

    def create(self):
        """Creates and empty ledger file
        """
        empty_ledger = {
            "transactions": []
        }
        with open(
            self.file,
            mode="w",
            encoding="utf-8"
        ) as account_file:
            json.dump(
                empty_ledger,
                account_file,
                indent=4
            )

        logger.info("Created an empty ledger file")

    def open_file(self):
        """Open the ledger file
        """

        logger.debug("Opening ledger file %s", self.filename)
        try:
            # My linter say I should open this with a with statement
            # Not gonna do that though because the class is already
            # Gonna be run within a with statement
            self.file = open(
                file=self.filename,
                mode=self.mode,
                encoding="utf-8"
            )
        except ValueError as e:
            logger.critical(
                "Invalid mode '%s' passed to LedgerFile.open_file()",
                e
            )

    def read(self) -> dict:
        """Reads the ledger file

        Returns:
            dict: Ledger information
        """

        try:
            self.account_data = json.load(self.file)
        except json.JSONDecodeError as e:
            logger.error("Ledger file not a JSON file: '%s'", e)
            sys.exit(1)

        if isinstance(self.account_data, dict):
            return self.account_data
        logger.critical("Ledger file seems to be corrupted")
        sys.exit(1)

    def write(self, data: dict) -> dict:
        """Writes all changes to the ledger file
        """

        if isinstance(data, dict):
            self.account_data = data
        else:
            logger.critical("Non dict passed to LedgerFile.modify()")
            sys.exit(1)

        try:
            json.dump(
                self.account_data,
                self.file,
                indent=4
            )
        except io.UnsupportedOperation:
            logger.error("Tried to right file in read only mode")
            sys.exit(1)

        return self.account_data

    def close(self):
        """Closes the file
        """

        if not self.file:  # Check if file is open
            self.file.close()
            self.file = None


class LedgerCommands:
    """Different supported commands"""
    def __init__(self, account_data: dict):
        if isinstance(account_data, dict):
            self.account_data = account_data
        else:
            raise TypeError(
                f"'account_data' must be a dict was a '{type(account_data)}'"
            )

    def register_command(self) -> str:
        """Prints out all transactions"""
        # Iterate over the transactions
        ledger = ""
        for transaction in self.account_data['transactions']:
            ledger += f"Date: {transaction['date']}\n"
            ledger += f"Description: {transaction['description']}\n"
            ledger += "Accounts: \n"
            # Iterate over the accounts
            for accounts in transaction['accounts']:
                ledger += f"\t{accounts}: {transaction['accounts'][accounts]}\n"
            # Print the transaction
            ledger += "\n"

        return ledger

    def transaction_command(
        self,
        date: str,
        description: str,
        accounts: dict,
        file: str
    ) -> str:
        """Adds a transaction to the ledger"""
        # Set up accounts dict
        try:
            # Set if date adheres to the date format
            datetime.strptime(date, DATE_FORMAT)
        except ValueError:
            raise ValueError(
                "Date entered does not conform to the date format (YY-mm-dd)"
            )
        assets = 0
        liabilities = 0
        for account, amount in accounts.items():
            if not re.compile(NAME_PATTERN).match(account):
                raise ValueError(
                    "Name does not conform to naming conventions"
                )
            if re.compile(r"^(Assets|Expenses).").match(account):
                assets += amount
            else:
                liabilities += amount
        if assets != liabilities:
            raise ValueError(
                "The transaction does not balance out"
            )
        # Append the transaction to the ledger
        self.account_data['transactions'].append(
            {
                "date": date,
                "description": description,
                "accounts": accounts
            }
        )
        # Write changes to file
        with LedgerFile(file, "w") as ledger_file:
            ledger_file.write(self.account_data)

    def account_balance_command(self) -> str:
        """Returns current account balances"""
        # Set up balances dict
        balances = {}
        # Iterate over all the transactions
        for transaction in self.account_data['transactions']:
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
            raise ValueError("Your accounts do not balance out")

        return accounts

    def statement_command(self, period: str) -> str:
        """Generates a statement for a period"""
        try:
            # Sett if date adheres to the date format
            datetime.strptime(period, "%Y-%m")
        except ValueError:
            try:  # Might be a year
                datetime.strptime(period, "%Y")
            except ValueError:
                raise ValueError(
                    "Period does not match: YY-mm or YY"
                )

        accounts = {}
        statement = ""

        for transaction in self.account_data['transactions']:
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
            return "Period had no  transactions"

        statement += "\n\n"
        statement += "=====END=====\n"
        for account, amount in accounts.items():
            statement += f"\t{account}: {amount}\n"

        return statement
