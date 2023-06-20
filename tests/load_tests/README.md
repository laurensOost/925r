# Automated availability and load time testing for Django admin interface

## Usage
This script has the same dependencies as the 925r project, so if you already have installed the virtual env, running it should work out-of-box.

The script requires three arguments (listed in order):
- URL of the django server (without /admin)
- Django superuser username
- Django superuser password
- $ python3 load_tests.py "URL" "username" "pw"

Afterwards the script will output URLs that are being currently crawled. At the end it will generate a `test_results.html` file in the directory where the script was run.