# PyPardot4 Single Sign On Enhancements

The upcoming Spring '21 release of Salesforce requires that all access to Pardot
be authenticated via Single Sign On with Salesforce via OAuth2.  This branch provides
an approach to enhancing PyPardot4 to extend it's functionality to be ready for 
the new release.  This branch is **NOT** meant to actually be merged, as is, into 
the PyPardot4 project.  Rather, it was committed to provide an example of an approach
and to discuss with the community if it would be a valuable approach, and what changes
would move it towards code that should be merged with the project.

## Approach

1. To show additional functionality through a subclass of PardotAPI, so as to highlight the 
   methodology for supporting SSO without changing existing code.
1. To separate authentication from api through the use of a hierarchy of authenticators.

## Demonstration

There is demonstration code provided in `oauth_demo.py` to show retroactive support for Pardot-Only 
authentication, raw `requests` level construction of working with Pardot using
OAuth2 authentication, and use of the AuthPardotAPI extension to PardotAPI to
work with the pardot api exactly as before with the extended ability to authenticate
using SSO credentials.

The demonstration program requires a configuration file, `oauth_demo.ini` which by default
is sought in the users home directory.  This can be changed at the top level of the
demo program.  The content needed in that file is described in `pardot_demo.ini` next to 
the demonstration program.  Since the config file will have private credentials in it, 
it is purposefully located outside of the project by default.  If your environment
does not support the sandboxes or you do not want to hit your production instances you 
can leave out sections, the demo program will skip the demonstrations it can not perform.

## Issues for Discussion

### Retroactive Support

Given that Pardot-Only authentication is fully going away, retroactive support for 
this authentication is not really necessary.  However, for the short time that both exist, it
is useful for testing.  Given this, it is not necessary to truly subclass the Pardot API class.
That was done here to show a clean seperation between what was and what can be.

### Separating Authentication from PardotAPI

That said, it is suggested strongly that authentication functionality be taken out of the 
ultimate PardotAPI class and be shifted to a proper hierarchy of authentication classes.
A quick review of the 
[`simple_salesforce`](https://github.com/simple-salesforce/simple-salesforce) package shows
three or more different ways in which one can authenticate with the Salesforce API.  
The code in this branch demonstrates achieving SSO using only one of them.  By separating
the authentication from the API class, it allows the PyPardot4 package to be easily extendable
to other methods of Salesforce authentication.

### Context Managers

It would seem very appropriate to enhance the PardotAPI class to be a context manager, such 
that it is authenticated as part of entering the context.  This branch does not yet include
those extensions in the AuthPardotAPI sub-class to not confuse the primary objective of
accomplishing SSO.  However, if this code is to be cleaned up for true integration into 
the project, it is strongly suggested that this enhancement be included.

## Caveats - IMPORTANT

### 3.7

This code was developed and tested under Python 3.7.4.  
It was not tested under any other version. 

### Relative Imports

This demonstration code made every effort to not change any of the existing code and demonstrate
the SSO functionality simply by adding code (for now).  However, there were changes made to 
remove all relative imports to enable the code to execute in our 3.7.4 environment.
This is another good reason not to merge this code as is.  If the community decides
that we should move ahead with this branch, the continued use of relative imports should
be discussed and if it is decided that they should continue to be utilized, we will need
assistance in figuring out how to get them to work in our environment.

