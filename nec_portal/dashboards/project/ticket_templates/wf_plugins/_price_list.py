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
#

from nec_portal.api import ticket as ticket_api
from nec_portal.dashboards.project.ticket_list \
    import utils as ticket_utils
from nec_portal.dashboards.project.ticket_templates.wf_engine.common \
    import plugin as base_plugin

VIEW_TICKET_TYPE = ['flat-rate']


class PriceList(base_plugin.BasePlugin):
    """Price list plugin"""

    def set_context_data(
            self, called_object, context, form_template, **kwargs):

        context['price_currency'] = ticket_utils.get_currency_unit()
        context['catalog'] = self._get_catalog(
            called_object,
            kwargs['template_contents'].get('target_id'),
            kwargs['template_contents'].get('target_key'))
        context['display_catalog_total'] = kwargs['template_contents'].get(
            'ticket_template_name').get('Default') in VIEW_TICKET_TYPE
        context['price_notice'] = \
            kwargs['template_contents'].get('price_notice', [])

    def _get_catalog(self, called_object, catalog_ids, catalog_keys):
        catalog = []

        for (catalog_id, catalog_key) in zip(catalog_ids, catalog_keys):
            # Get a catalog information
            catalog_data = ticket_api.catalog_get_detailed(
                called_object.request,
                catalog_id)
            price = ticket_utils.get_price_from_catalog(called_object.request,
                                                        catalog_id)
            catalog.append({
                'key': catalog_key,
                'catalog_name': catalog_data.catalog_name,
                'price': price,
            })

        return catalog
