#!/usr/bin/env zsh
source .venv/bin/activate
pip list
alias pytu='pytest tests/unit --cache-clear -s'
alias pyti='pytest tests/integration --cache-clear -s'
alias pyt='pytest --cache-clear -s'
alias pyl='pylint . --output-format=colorized'
alias flk='flake8'
alias pyrt='pyright src'
alias pyrtw='pyright src --watch'
alias pyrtv='pyright src --verbose'
echo "You are now good for development"
