#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#

import logging

from django.utils.translation import string_concat
from django.utils.translation import ugettext_lazy as _

from horizon import tables
from nec_portal.dashboards.project.private_price_lists import \
    constants
from nec_portal.local import nec_portal_settings as nec_set

LOG = logging.getLogger(__name__)
PRICE_UNIT = getattr(nec_set, 'PRICE_UNIT', 'USD')


class CatalogsFilterAction(tables.FilterAction):
    """Catalogs filter action class"""
    filter_type = "server"
    filter_choices = (('catalog_name', _('Items ='), True),)


class CatalogsTable(tables.DataTable):
    """Catalogs table class"""
    catalog_name = tables.Column('catalog_name',
                                 verbose_name=_('Items'),
                                 link=constants.CATALOG_DETAIL_URL)

    price_str = _('Price')
    tax_str = _('*Tax excluded')
    price = tables.Column('price',
                          verbose_name=string_concat(price_str,
                                                     '(' + PRICE_UNIT + ') ',
                                                     tax_str))

    def get_object_id(self, catalog):
        return '|'.join([catalog.catalog_id,
                         catalog.catalog_scope_id,
                         catalog.price_seq_no])

    class Meta(object):
        name = "catalogs"
        verbose_name = _("Catalog")

        multi_select = False

        table_actions = (CatalogsFilterAction,)
        pagination_param = "catalog_marker"
