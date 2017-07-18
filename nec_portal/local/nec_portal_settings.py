from django.utils.translation import ugettext_lazy as _

# After application of the NECCSPORTAL, please be postscript.
REQUEST_GROUP_NAME = _('Request')
CONTRACT_GROUP_NAME = _('Contract')
CATALOG_GROUP_NAME = _('Catalog')

CURRENCY_FORMAT = _('{0:,.2f}')
CURRENCY_UNIT = _('USD')

PRICE_FORMAT = [',', '.', 2]
PRICE_UNIT = 'USD'

# Region Contract links list.
# NOTE: If you want to add an external link,
# please add the specified name and url.
#   name: Specifies the name of the external link.
#   root_url: Specifies the ROOT URL(ex http://XXX.XXX.XXX.XXX/)
#             of the external link.
#   role: Specifies the roles for display links(ex ['A Role', 'B Role',]).
# NOTICE: This setting is assumed
#   that SSO(Single sign on) is enabled between sites of 'root_url'.
REGION_CONTRACTS_LINKS = [
    {
        'name': _('RegionPortal(DC1)'),
        'root_url': 'https://xxxx/',
        'role': ['T__DC1__ProjectMember',]
    },
    {
        'name': _('RegionPortal(DC2)'),
        'root_url': 'https://xxxx/',
        'role': ['T__DC2__ProjectMember',]
    },
    {
        'name': _('RegionPortal(DC3)'),
        'root_url': 'https://xxxx/',
        'role': ['T__DC3__ProjectMember',]
    },
]
