#!/usr/bin/env python3
"""UI code"""

import logging
from .ledger import LedgerFile, LedgerCommands

logger = logging.getLogger(__name__)


class UI:
    """Simple UI class"""
    def __init__(self, file: str):
        self.file = file

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def command(self, command: str) -> str:
        """Runs the specified command"""
        with LedgerFile(self.file, mode="r") as ledger_file:
            account_data = ledger_file.read()

        commands = LedgerCommands(account_data)

        # Command register
        if command == "register":
            print(commands.register_command())
        # Command transaction
        elif command == "transaction":
            # Get the date
            date = input("Date (YY-mm-dd): ")
            description = input("Input transaction description: ")
            get_accounts = True
            accounts = {}
            while get_accounts:
                # Get account
                name = input("Account name: ")
                # If enter pressed then break
                if name == "":
                    get_accounts = False
                    break
                # Make sure account not already used during this transaction
                if name in accounts:
                    raise ValueError("You have input an account twice")
                while True:
                    try:
                        accounts[name] = int(input("Amount: "))
                        break
                    except ValueError:
                        logger.warning("You inputted a non int as a number.")
                        continue
            commands.transaction_command(
                date=date,
                description=description,
                accounts=accounts,
                file=self.file
            )
        # Command accounts
        elif command == "accounts":
            print(commands.account_balance_command())
        # Command statement
        elif command == "statement":
            period = input(
                "Please input a month or a year (YY-mm or YY): "
            )
            statement = commands.statement_command(period)
            print(statement)
            save_to_file = input("Save to file? [Y/n]: ").lower()
            if save_to_file in ("y", ""):
                with open(
                    f"statement-{period}.txt", mode="w", encoding="utf-8"
                ) as statement_file:
                    statement_file.write(statement)
                print(f"Statement saved: 'statement-{period}.txt'")
            else:
                print("Not saving to file")
        else:
            print(f"Invalid command passed: '{command}'")
