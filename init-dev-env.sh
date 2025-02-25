#!/usr/bin/env zsh
source .venv/bin/activate
pip list
alias pytu='pytest tests/unit --cache-clear -s'
alias pyti='pytest tests/integration --cache-clear -s'
alias pyt='pytest --cache-clear -s'
alias pyl='pylint . --output-format=colorized'
alias flk='flake8'
alias pyr='pyright'
alias pyrw='pyright --watch'
alias pyrv='pyright --verbose'
echo "You are now good for development"
