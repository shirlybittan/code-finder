# Secret Code finder
This code searches for AWS secret access key and RSA private key in GitHub repositories.

## Requirements
`pip3 install GitPython PyGithub`

require token from your personal github account. You can generate one at https://github.com/settings/tokens
save it as github_token.txt

## Usage

test: 
`python3 testRegex.py`
normal run:
`python3 secretsFinder.py`

The codes found will be in the file "resultsFound/Results.txt"
