# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from cliff.lister import Lister

from ..helpers import ListBuildingMixin


class EndpointSIPList(ListBuildingMixin, Lister):
    'List SIP endpoints'
    _columns = [
        'uuid',
        'label',
        'name',
        'tenant_uuid',
    ]
    _removed_columns = [
        'aor_section_options',
        'asterisk_id',
        'auth_section_options',
        'endpoint_section_options',
        'identify_section_options',
        'line',
        'links',
        'outbound_auth_section_options',
        'registration_outbound_auth_section_options',
        'registration_section_options',
        'templates',
        'transport',
        'trunk',
    ]

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            '--recurse',
            help='Show SIP endpoints in all subtenants',
            action='store_true',
        )
        parser.add_argument(
            '--tenant',
            help='Show SIP endpoints in a specific tenant',
        )
        return parser

    def take_action(self, parsed_args):
        kwargs = {'recurse': parsed_args.recurse}

        if parsed_args.tenant:
            # TODO(pc-m): aventually add the auth client to be able to use by name?
            kwargs['tenant_uuid'] = parsed_args.tenant

        result = self.app.client.endpoints_sip.list(**kwargs)
        if not result['items']:
            return (), ()

        raw_items = result['items']
        headers = self.extract_column_headers(raw_items[0])
        items = self.extract_items(headers, raw_items)

        return headers, items
