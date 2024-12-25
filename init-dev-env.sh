#!/usr/bin/env zsh
source .venv/bin/activate
pip list
alias pyt='pytest --cache-clear -s'
alias pyl='pylint . --output-format=colorized "$FilePath$"'
alias flk='flake8'
echo "You are now good for development"
