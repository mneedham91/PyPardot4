# PyPardotSF

PyPardotSF is yet another fork of PyPardot/PyPardot4. The main driver for the
fork is to address Pardot's authentication change in Spring 2021 to use
Salesforce OAuth.
(As seen on [PyPardot4 Issue #46](https://github.com/mneedham91/PyPardot4/issues/46))

Another new features of PyPardotSF includes:

- Support both Versions 3 & 4 of Pardot API
- Support Version 3 & 4 [Import API (for Prospects)](https://developer.salesforce.com/docs/marketing/pardot/guide/import-v4.html)

This is a working prototype and the code is currently being cleaned up and
more detailed documentation is underway.

I'm keeping the original MIT License by the previous contributors.
Any contributions, including code, documentations, issue reporting are welcome.

## Install

```
pip install PyPardotSF
```

## Salesforce OAuth

### Get keys and tokens

Do this once when you do not have consumer key, secret, refresh token:

1. Open Python's interactive shell and run the following command:

```
$ python3

>>> from pypardot.client import PardotAPI
>>> p = PardotAPI(version=3)  # verion=4 available
>>> p.setup_salesforce_auth_keys()
```

2. Follow the instruction in the command line to get the keys and
refresh token.

3. After you answer all the questions in the console, you should be able to
access API commands:

```
>>> p.prospects.read_by_email(email="daigo@anelen.co")
```

4. You can check the values of business unit id, consumer key, secret, and
refresh token:

```
>>> p.business_unit_id
'0Uv*****'
>>> p.sf_consumer_key
'xxxx'
>>> p.sf_consumer_secret
'yyyy'
>>> p.sftoken_refresh
'zzzz'
```

5. Please note them for the secondary and/or programmatic access.
(See the next section)

### Using the API client

```
from pypardot.client import PardotAPI

version = 3  # 3 or 4
sf_consumer_key = "xxxx"
sf_consumer_secret = "yyyy"
sf_refresh_token = "zzzz"
business_unit_id = "0Uv*****"

p = PardotAPI(
    sf_consumer_key=sf_consumer_key,
    sf_consumer_secret=sf_consumer_secret,
    sf_refresh_token=sf_refresh_token,
    business_unit_id=business_unit_id,
    version=version)
p.prospects.read_by_email(email="daigo@anelen.co")
```

## Bulk Prospect Import

```
file_name = "data.csv"
columns = [
    {
        "field": "email"
    },
    {
        "field": "pardot_field_a",
        "overwrite": False,
        "nullOverwrite": False
    },
    {
        "field": "pardot_field_b",
        "overwrite": False,
        "nullOverwrite": False
    },
}
results = client.importapi.create(
    file_name=file_name,
    operation="Upsert",
    object="Prospect",
    columns=columns,
    restoreDeleted=config.get("restore_deleted", False),
    )
batch_id = results["id"]
results = client.importapi.update(id=batch_id, state="Ready")
```

Check the import status at:

API Imports section at 
[Admin->Import->Prospects](https://pi.pardot.com/import/wizardStep1)

## Other endpoints

Please see the original
[PyPardot](https://github.com/joshgeller/PyPardot) /
[PyPardot4](https://github.com/mneedham91/PyPardot4)
docs.

## Contributors wanted

My (Daigo Tanaka) access to Pardot may not be permanent and I curently have
access to Ver 3 API. So I would like this repository to be collaborative as
possible with the active Python programmers who uses Pardot API. This includes
the release process. I don't want to be a gate-keeper or a blocker.

Any bug fixes and enhancements are welcome and I trust your good intentions.
Together with the fellow contributors, I will help review the code from
good design and coding stand point, but I may not be able to run tests myself
for the reason I stated above. So please DO include the following sections
in your pull requests:

1. Reason for code modification. Include GitHub Issue # (create if not exists)
2. Supporting API version (3, 4 or both)
3. Manual test description: Method and result.
4. Risks of change.

## Code of Conduct

Please read and acknowledge our
[Code of Conduct](https://github.com/anelendata/PyPardotSF/blob/master/CODE_OF_CONDUCT.md).
before using or contributing to this project.

## Related projects

- target-pardot: A singer.io specification that bulk-updates prospect records
  to Pardot. The program uses PyPardotSF.

# About this project

This project is developed by 
ANELEN and friends. Please check out the ANELEN's
[open innovation philosophy and other projects](https://anelen.co/open-source.html)

![ANELEN](https://avatars.githubusercontent.com/u/13533307?s=400&u=a0d24a7330d55ce6db695c5572faf8f490c63898&v=4)
---

Copyright &copy; 2020~ Anelen Co., LLC

PyPardot4
=========

*This is README from the original PyPardot4 by Matt Needham, as of this [commit](5b26b871b7d4f6385755b2f3737a299509659ce1).*

PyPardot was originally created by Josh Geller as a wrapper for Version 3 of the Pardot API.
I, Matt Needham, have edited PyPardot for compatibility with Version 4 of the Pardot API.
Version 4 accommodates multiple prospects with the same email address. If your Pardot org does not have this featured enabled, you must use version 3.
To determine if your Pardot org has this feature enabled, [check out this guide](http://developer.pardot.com/kb/api-version-4/).

PyPardot is an API wrapper for [Pardot](http://www.pardot.com/), written in Python.

Using it is simple:

```python
from pypardot.client import PardotAPI

p = PardotAPI(
  email='email@email.com',
  password='password',
  user_key='userkey'
)
                
p.authenticate()

# Create a new prospect
p.prospects.create(email='joe@company.com', first_name='Joe', last_name='Schmoe')

# Read data about our prospect
print(p.prospects.read_by_email(email='joe@company.com'))

```

Features
---

+ Includes all documented Pardot API operations
+ Handles API key expiration
+ Detailed API error handling

Object Types & Operations
---

Support for the following object types:

+ Accounts
+ Campaigns
+ Custom Fields
+ Custom Redirects
+ Dynamic Content
+ Emails
+ Email Clicks
+ Email Templates
+ Forms
+ Lifecycle Histories
+ Lifecycle Stages
+ Lists
+ List Memberships
+ Opportunities
+ Prospects
+ Prospect Accounts
+ Tags
+ TagObjects
+ Users
+ Visitor Activities
+ Visitors
+ Visits

Required
---

+ [requests](http://docs.python-requests.org/en/latest/)

Installation
---

Install PyPardot by running:
```shell
pip install pypardot4
```

Usage
---

### Authentication

To connect to the Pardot API, you'll need the e-mail address, password, and user key associated with your Pardot account. Your user key is available in the Pardot application under My Settings.

The client will authenticate before performing other API calls, but you can manually authenticate as well:


```python
p = PardotAPI(
  email='your_pardot_email',
  password='your_pardot_password',
  user_key='your_pardot_user_key'
)
                
p.authenticate()
```

### Querying Objects

Supported search criteria varies for each object. Check the [official Pardot API documentation](http://developer.pardot.com/) for supported parameters. Most objects support `limit`, `offset`, `sort_by`, and `sort_order` parameters. PyPardot returns JSON for all API queries.

**Note**: Pardot only returns 200 records with each request. Use `offset` to retrieve matching records beyond this limit.

```python
# Query and iterate through today's prospects
prospects = p.prospects.query(created_after='yesterday')
total = prospects['total_results'] # total number of matching records
for prospect in prospects['prospect']
  print(prospect.get('first_name'))
```

### Editing/Updating/Reading Objects

Supported fields varies for each object. Check the [official Pardot API documentation](http://developer.pardot.com/kb/object-field-references/) to see the fields associated with each object. 

```python
# Create a new prospect
p.prospects.create_by_email(email='joe@company.com', first_name='Joe', last_name='Schmoe')

# Update a prospect field (works with default or custom field)
p.prospects.update_field_by_id(id=23839663, field_name='company', field_value='Joes Plumbing')

# Send a one-off email
p.emails.send_to_email(prospect_email='joe@company.com', email_template_id=123)
```

### Error Handling

#### Handling expired API keys

Pardot API keys expire after 60 minutes. If PyPardot detects an 'Invalid API key' error during any API call, it will automatically attempt to re-authenticate and obtain a new valid API key. If re-authentication is successful, the API call will be re-issued. If re-authentication fails, a `PardotAPIError` is thrown.

#### Invalid API parameters

If an API call is made with missing or invalid parameters, a `PardotAPIError` is thrown. Error instances contain the error code and message corresponding to error response returned by the API. See [Pardot Error Codes & Messages](http://developer.pardot.com/kb/error-codes-messages/) in the official documentation.

Performing API calls is inherently unsafe, so be sure to catch exceptions:

```python
try:
  p.prospects.create_by_email(email='existing.email.address@company.com')
except PardotAPIError, e:
  print(e)
```
