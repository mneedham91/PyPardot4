# This module (objects) was originally imported from Josh Geller's original implementation
# https://github.com/joshgeller/PyPardot/tree/349dde1fad561f32a425324005c4f2a0c4a23d9b/pypardot/objects
# The code in __init__.py was added to be integrated with PyPardot4 to support
# difference in the implementations between the versions 3 and 4.
from .lists import Lists
from .emails import Emails
from .prospects import Prospects
from .opportunities import Opportunities
from .accounts import Accounts
from .users import Users
from .visits import Visits
from .visitors import Visitors
from .visitoractivities import VisitorActivities
from .campaigns import Campaigns
from .importapi import Import

def load_objects(client):
    client.lists = Lists(client)
    client.emails = Emails(client)
    client.prospects = Prospects(client)
    client.opportunities = Opportunities(client)
    client.accounts = Accounts(client)
    client.users = Users(client)
    client.visits = Visits(client)
    client.visitors = Visitors(client)
    client.visitoractivities = VisitorActivities(client)
    client.campaigns = Campaigns(client)
    client.importapi = Import(client)
