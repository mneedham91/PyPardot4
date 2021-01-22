# PyPardot4 Single Sign On Enhancements

The upcoming Spring '21 release of Salesforce requires that all access to Pardot
be authenticated via Single Sign On with Salesforce via OAuth2.  This branch provides
an approach to enhancing PyPardot4 to extend it's functionality to be ready for 
the new release.  This branch is **NOT** meant to actually be merged, as is, into 
the PyPardot4 project.  Rather, it was committed to provide an example of an approach
and to discuss with the community if it would be a valuable addition, and if so, what changes
would be needed to prepare the code to be merged with the project.

## Approach

1. To show additional functionality through a subclass of PardotAPI, so as to highlight the 
   methodology for supporting SSO without changing existing code.
1. To separate authentication methodology from the api through the 
   use of a hierarchy of authenticator classes.

## Demonstration

There is demonstration code provided in `oauth_demo.py` that shows:
1. Retroactive support for Pardot-Only authentication.
1. Example of how to perform SSO via OAuth2 authentication using raw `requests` level construction.
1. Support for SSO via OAuth2 authentication via the AuthPardotAPI subclass of PardotAPI

The demonstration program requires a configuration file, `oauth_demo.ini` which by default
is sought in the users home directory.  This can be changed at the top level of the
demo program.  The content needed in that file is described in `pardot_demo.ini` next to 
the demonstration program.  Since the config file will have private credentials in it, 
it is purposefully located outside of the project by default.  The configuration file has sections
for different pardot and salesforce instances, both production and sand box.  If you do not desire to 
hit against any of these while running the demo, or you do not have access to any of these, you 
can eleminate those sections.  The demo program will skip code that requires the missing sections.

## Issues for Discussion

### Retroactive Support

Given that Pardot-Only authentication is fully going away, retroactive support for 
the old style of authentication is not really necessary.  However, for the short time that both exist, it
is useful for testing.  Given this, it is not necessary to truly subclass the Pardot API class as shown here.
That architecture was used in this version to show a clean separation between what was and what can be.

### Separating Authentication from PardotAPI

That said, it is suggested strongly that authentication functionality be taken out of the 
updated PardotAPI class and be shifted to a proper hierarchy of authentication classes.
A quick review of the 
[`simple_salesforce`](https://github.com/simple-salesforce/simple-salesforce) package shows
three or more different ways in which one can authenticate with the Salesforce API.  
The code in this branch demonstrates achieving SSO using only one of them.  By separating
the authentication from the API class, it allows the PyPardot4 package to be easily extendable
to other methods of Salesforce authentication to be used for SSO if necessary.

### Context Managers

It would seem very appropriate to enhance the PardotAPI class to be a context manager, such 
that it is authenticated as part of entering the context.  This branch does not yet include
those extensions in the AuthPardotAPI sub-class to not confuse the primary objective of
accomplishing SSO.  However, if this code is to be re-worked in order to be merged into 
the project, it is strongly suggested that this enhancement be included.

## Caveats - IMPORTANT

### 3.7

This code was developed and tested under Python 3.7.4.  
It was not tested under any other version. 

### Relative Imports

This demonstration code made every effort to not change any of the existing code and demonstrate
the SSO functionality simply by adding code (for now).  However, there were changes made 
removing all relative imports from existing files to enable the code to execute in our 3.7.4 environment.
This is another good reason not to merge this code as is.  If the community decides
that we should move ahead with this branch, the continued use of relative imports should
be discussed and if it is decided that they should continue to be utilized, we will need
assistance in figuring out how to get them to work in our environment.
