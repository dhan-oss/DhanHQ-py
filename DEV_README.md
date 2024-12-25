# Readme For Developers

## Project structure 

```text
DhanHQ-py/
├── src/
│   └── dhanhq/
│       └── __init__.py  # Important: Make your_package a proper package
│       └── ...  # Your package code
└── tests/
    └── ...  # Your test files
├── setup.py
└── ... (other files)
```

## Development Environment Setup

Run through the following commands as shown below to set your local environment context:
```bash
pip --version
pip install --upgrade pip # To upgrade pip
pip --version
pip list # To list installed packages
pyenv version # check to see current python version is 3.9.2
pyenv local 3.9.2 # automatically select whenever you are in the current directory (or its subdirectories)
python3 -m venv .venv
source .venv/bin/activate # activate virtual environmant
deactivate # to deactivate virtual environment
pip list
```
Your mileage may vary depending on your toolset choice. The example above shows `pyenv` and `venv` as choice of tools for this and `.gitignore` files is set to reflect this.

To setup project:
```bash
pip install -e '.[dev]'
pip list
flake8 ./dhanhq/ # To run linting manually on the python code
pytest -v --flake8 # Run unit tests
```

**Important:** Also, rename the file `test.env.sample` to `test.env` and add your credentials - `client-id` and `access-token` to it, for your integration tests to run.

The next time when you enter this directory to gear-up your dev-env, all you got to do is just run the script below: 
```bash
source ./init-dev-env.sh
```

To run your unit tests only, you can try any of the following:
```bash
pytu # Run `chmod u+x init-dev-env.sh` to ensure you have exec permission on this file.
pytest tests/unit --cache-clear -s # To clear caches in case of test issues because of cacheing
pytest ./tests/test_dhanhq.py --cache-clear -v # To run all tests in specific test file
pytest ./tests/test_dhanhq.py::TestDhanhq_GetOrderList --cache-clear -v # To run specific group of tests in specific test file
```

To run your integration tests only, you can try any of the following:
```bash
pyti # Run `chmod u+x init-dev-env.sh` to ensure you have exec permission on this file.
pytest tests/integration --cache-clear -s # To clear caches in case of test issues because of cacheing
```

To run both unit and integration tests, you can try any of the following:
```bash
pyt # Run `chmod u+x init-dev-env.sh` to ensure you have exec permission on this file.
pytest --cache-clear -s
```

To deactivate virtual environment
```python
deactivate
```

## Do You Know?

1. If you modify the `setup.py` file, 
   you would do good to reinstall the package for development using command:
    ```bash
   pip install -e '.[dev]'
    ```
2. ..

## Steps to contribute to project

- Fork repository to your Github account
- Check out to your local dev box using `git checkout <remote-repo-url-of-your-forked-repo-in-github>`
- Setup your local dev environment by following steps in **Development Environment Setup** section above.
- Create new local branch for development like `git checkout -n new_feature`
- Do your feature evelopment and commit locally to that branch
- Push branch to your remote repo thus creating a new feature-branch in your repo.
- Send merge request to main branch of Dhanhq repo.
- Wait for feedback and status update.
- Once feature is merged to main project in DhanHQ, sync your forked repo's main branch to find your commit along with others.


## ToDos Before Release

- [ ] No linting issues
- [ ] All tests should pass
- [ ] Update `VERSION` field in `setup.py`.
