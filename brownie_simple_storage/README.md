on the terminal run:

brownie accounts new freecodecamp-account

paste your secret:
0x00000000000000000000000000000000000000

type a new password

You need to run the ganache-cli on another terminal session with:

ganache-cli

run brownie

brownie run scripts/deploy.py

## Test

brownie test

run only one test

brownie test -k test_updating_storage

brownie test -s
