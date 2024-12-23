#!/usr/bin/env zsh
source .venv/bin/activate
pip list
alias pyt='pytest --cache-clear -s'
echo "You are now good for development"
