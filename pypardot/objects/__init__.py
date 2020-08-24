from .accounts import Accounts
from .customfields import CustomFields
from .customredirects import CustomRedirects
from .dynamiccontent import DynamicContent
from .emailclicks import EmailClicks
from .emailtemplates import EmailTemplates
from .forms import Forms
from .lifecyclehistories import LifecycleHistories
from .lifecyclestages import LifecycleStages
from .lists import Lists
from .listmemberships import ListMemberships
from .emails import Emails
from .prospects import Prospects
from .opportunities import Opportunities
from .prospectaccounts import ProspectAccounts
from .tags import Tags
from .tagobjects import TagObjects
from .users import Users
from .visits import Visits
from .visitors import Visitors
from .visitoractivities import VisitorActivities
from .campaigns import Campaigns


def load_objects(client):
    client.accounts = Accounts(client)
    client.campaigns = Campaigns(client)
    client.customfields = CustomFields(client)
    client.customredirects = CustomRedirects(client)
    client.dynamiccontent = DynamicContent(client)
    client.emailclicks = EmailClicks(client)
    client.emails = Emails(client)
    client.emailtemplates = EmailTemplates(client)
    client.forms = Forms(client)
    client.lifecyclehistories = LifecycleHistories(client)
    client.lifecyclestages = LifecycleStages(client)
    client.listmemberships = ListMemberships(client)
    client.lists = Lists(client)
    client.opportunities = Opportunities(client)
    client.prospects = Prospects(client)
    client.prospectaccounts = ProspectAccounts(client)
    client.tags = Tags(client)
    client.tagobjects = TagObjects(client)
    client.users = Users(client)
    client.visits = Visits(client)
    client.visitors = Visitors(client)
    client.visitoractivities = VisitorActivities(client)
