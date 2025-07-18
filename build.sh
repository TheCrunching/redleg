#!/bin/bash

# Check if were in virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]
then
    # Build and install
    python3 -m build
else
    echo "Not in virtual environment"
fi
