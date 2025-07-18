#!/usr/bin/env python3
"""Handles TUI (curses) code"""

import curses
import logging
from curses import panel
from .ledger import LedgerFile, LedgerCommands

logger = logging.getLogger(__name__)


class Menu():
    """A menu thingy"""
    # https://stackoverflow.com/questions/14200721/how-to-create-a-menu-and-submenus-in-python-curses#14205494
    def __init__(self, items, stdscreen):
        self.window = stdscreen.subwin(0, 0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items
        self.items.append(("exit", "exit"))

    def navigate(self, n):
        """Navigates the menu"""
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items) - 1

    def display(self):
        """Show the panel"""
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = f"{index} {item[0]}"
                self.window.addstr(1 + index, 1, msg, mode)

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord("\n")]:
                if self.position == len(self.items) - 1:
                    break
                self.items[self.position][1]()

            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()


class TUI():
    """TUI code"""
    def __init__(self, file):
        self.stdscr = None
        self.file = file
        with LedgerFile(self.file, mode="r") as ledger_file:
            self.account_data = ledger_file.read()
            self.commands = LedgerCommands(self.account_data)

    def __enter__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def command(self):
        """Main window function"""
        items = [
            ("register", self.register_command),
            ("transaction", self.transaction_command),
            ("accounts", self.accounts_command),
            ("statement", self.statement_command)
        ]

        menu = Menu(items, self.stdscr)
        menu.display()

    def register_command(self):
        """Prints all transactions"""
        print(self.commands.register_command())

    def transaction_command(self):
        """Makes a transaction"""
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
        self.commands.transaction_command(
            date=date,
            description=description,
            accounts=accounts,
            file=self.file
        )

    def accounts_command(self):
        """Prints account balances"""
        print(self.commands.account_balance_command())

    def statement_command(self):
        """Makes a statement"""
        period = input(
            "Please input a month or a year (YY-mm or YY): "
        )
        statement = self.commands.statement_command(period)
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
