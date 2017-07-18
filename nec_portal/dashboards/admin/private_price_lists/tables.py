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

from django.core import exceptions as django_exceptions
from django.core.urlresolvers import reverse
from django.utils.translation import string_concat
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions as horizon_exceptions
from horizon import forms
from horizon import messages
from horizon import tables

from nec_portal.api import ticket as ticket_api
from nec_portal.dashboards.admin.private_price_lists import constants
from nec_portal.local import nec_portal_settings as nec_set

LOG = logging.getLogger(__name__)
PRICE_FORMAT = getattr(nec_set, 'PRICE_FORMAT', [',', '.', 2])
PRICE_UNIT = getattr(nec_set, 'PRICE_UNIT', 'USD')

RANGE_PUBLIC = 'public'
RANGE_PRIVATE = 'private'


class EditPublicPriceLink(tables.LinkAction):
    name = "public_price"
    verbose_name = _("Edit Public Price List")
    icon = "pencil"

    def get_link_url(self):
        url = constants.PUBLIC_PRICE_URL
        base_url = reverse(url)
        return base_url


class EditPriceFilterAction(tables.FilterAction):
    def filter(self, table, tenants, filter_string):
        q = filter_string.lower()

        def comp(tenant):
            if q in tenant.name.lower():
                return True
            return False

        return filter(comp, tenants)


class EditPrivatePriceLink(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit Private Price List")
    url = constants.PRIVATE_PRICE_URL
    icon = "pencil"


class TenantsTable(tables.DataTable):
    name = tables.Column('name',
                         verbose_name=_('Project Name'))
    description = tables.Column('description', verbose_name=_('Description'))
    id = tables.Column('id', verbose_name=_('Project ID'))

    class Meta(object):
        name = "tenants"
        verbose_name = _("Price Lists")
        multi_select = False

        table_actions = (EditPriceFilterAction,
                         EditPublicPriceLink)
        row_actions = (EditPrivatePriceLink,)


class PriceUpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, object_id):
        catalog_id, scope, seq_no, project_id, range = object_id.split('|')

        catalog_scope_list, unused_p, self.unused_m = \
            ticket_api.catalog_scope_list(request,
                                          scope,
                                          sort_key='catalog_id',
                                          sort_dir='asc',
                                          filters={'catalog_id': catalog_id, })
        catalog_wk = catalog_scope_list[0]

        return ticket_api.ValidCatalog(catalog_wk.catalog_id,
                                       catalog_wk.catalog_name,
                                       catalog_wk.public_seq_no,
                                       catalog_wk.public_price,
                                       catalog_wk.private_seq_no,
                                       catalog_wk.private_price,
                                       project_id)


class PriceUpdateCell(tables.UpdateAction):

    def update_cell(self, request, datum, object_id,
                    cell_name, new_cell_value):
        catalog_id, scope, seq_no, project_id, range = object_id.split('|')

        try:
            now = ticket_api.get_datetime_now()
            fields = {}
            del_flg = False

            update_price = input_price_check(new_cell_value)
            if update_price and 0 < len(update_price):
                fields = {'price': update_price}
            else:
                del_flg = True

            ticket_api.price_update_or_create(request,
                                              datum.catalog_id,
                                              scope,
                                              fields,
                                              now,
                                              del_flg)

            fields = {}
            ticket_api.catalog_scope_update_or_create(request,
                                                      datum.catalog_id,
                                                      scope,
                                                      fields,
                                                      now,
                                                      del_flg)

        except horizon_exceptions.Conflict:
            message = _("This price is already taken.")
            messages.warning(request, message)
            raise django_exceptions.ValidationError(message)
        except django_exceptions.ValidationError as e:
            msg = _(e.message)  # noqa
            messages.error(request, msg)
            horizon_exceptions.handle(request, ignore=True)
            return False
        except Exception:
            horizon_exceptions.handle(request, ignore=True)
            return False
        return True


class PrivatePriceTable(tables.DataTable):
    catalog_id = tables.Column('catalog_id',
                               hidden=True,
                               verbose_name=_('ID'))
    catalog_name = tables.Column('catalog_name', verbose_name=_('Items'))
    catalog_scope_id = tables.Column('project_id', hidden=True,
                                     verbose_name=_('Scope ID'))
    scope = tables.Column('project_id', hidden=True, verbose_name=_('Scope'))
    public_seq_no = tables.Column('public_seq_no', hidden=True,
                                  verbose_name=_('Public Seq No'))
    private_seq_no = tables.Column('private_seq_no', hidden=True,
                                   verbose_name=_('Private Seq No'))

    tax_str = _('*Tax excluded')

    public_price_str = _('Public Price')
    public_price = tables.Column(
        'public_price',
        form_field=forms.CharField(),
        verbose_name=string_concat(public_price_str,
                                   '(' + PRICE_UNIT + ') ',
                                   tax_str))

    private_price_str = _('Private Price')
    private_price = tables.Column(
        'private_price',
        form_field=forms.CharField(required=False),
        update_action=PriceUpdateCell,
        verbose_name=string_concat(private_price_str,
                                   '(' + PRICE_UNIT + ') ',
                                   tax_str))

    def get_object_id(self, price):
        return '|'.join([price.catalog_id,
                         price.project_id,
                         price.private_seq_no,
                         self.kwargs['project_id'],
                         RANGE_PRIVATE])

    class Meta(object):
        name = "private_price_lists_update"
        verbose_name = _("Edit Private Price List")

        multi_select = False

        table_actions = (EditPriceFilterAction,)
        row_class = PriceUpdateRow


class PublicPriceTable(tables.DataTable):
    catalog_id = tables.Column('catalog_id',
                               hidden=True,
                               verbose_name=_('ID'))
    catalog_name = tables.Column('catalog_name', verbose_name=_('Items'))
    catalog_scope_id = tables.Column('project_id', hidden=True,
                                     verbose_name=_('Scope ID'))
    scope = tables.Column('project_id', hidden=True, verbose_name=_('Scope'))
    public_seq_no = tables.Column('public_seq_no',
                                  hidden=True,
                                  verbose_name=_('Public Seq No'))

    tax_str = _('*Tax excluded')
    public_price_str = _('Public Price')
    public_price = tables.Column(
        'public_price',
        form_field=forms.CharField(required=False),
        update_action=PriceUpdateCell,
        verbose_name=string_concat(public_price_str,
                                   '(' + PRICE_UNIT + ') ',
                                   tax_str))

    def get_object_id(self, price):
        return '|'.join([price.catalog_id,
                         price.project_id,
                         price.public_seq_no,
                         ticket_api.SCOPE_DEFAULT,
                         RANGE_PUBLIC])

    class Meta(object):
        name = "public_price_lists_update"
        verbose_name = _("Edit Public Price List")

        multi_select = False

        table_actions = (EditPriceFilterAction,)
        row_class = PriceUpdateRow


def input_price_check(new_cell_value):
    error_message = _("Invalid price format.")

    update_price = new_cell_value.replace(PRICE_FORMAT[0], '')
    if 1 > len(update_price):
        return update_price

    if update_price.count(PRICE_FORMAT[1]) == 0:
        if not update_price.isdigit() or len(update_price) > 9:
            raise django_exceptions.ValidationError(error_message)

    elif update_price.count(PRICE_FORMAT[1]) == 1:
        inte, deci = update_price.split(PRICE_FORMAT[1])
        if not inte.isdigit() or not deci.isdigit() \
                or len(inte) > 9 or len(deci) > PRICE_FORMAT[2]:
            raise django_exceptions.ValidationError(error_message)
        update_price = '.'.join([inte, deci])

    else:
        raise django_exceptions.ValidationError(error_message)

    return update_price
