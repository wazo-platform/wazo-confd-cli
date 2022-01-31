# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from cliff.lister import Lister

from ..helpers import ListBuildingMixin


class UserList(ListBuildingMixin, Lister):
    'List Users'

    _columns = ['id', 'uuid', 'firstname', 'lastname', 'tenant_uuid']
    _removed_columns = [
        'agent',
        'call_permission_password',
        'call_permissions',
        'call_pickup_target_users',
        'call_record_enabled',
        'call_record_incoming_external_enabled',
        'call_record_incoming_internal_enabled',
        'call_record_outgoing_external_enabled',
        'call_record_outgoing_internal_enabled',
        'call_transfer_enabled',
        'caller_id',
        'description',
        'dtmf_hangup_enabled',
        'email',
        'enabled',
        'fallbacks',
        'forwards',
        'groups',
        'incalls',
        'language',
        'lines',
        'links',
        'mobile_phone_number',
        'music_on_hold',
        'online_call_record_enabled',
        'outgoing_caller_id',
        'password',
        'preprocess_subroutine',
        'queues',
        'ring_seconds',
        'schedules',
        'services',
        'simultaneous_calls',
        'subscription_type',
        'supervision_enabled',
        'switchboards',
        'timezone',
        'userfield',
        'username',
        'voicemail',
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

        result = self.app.client.users.list(**kwargs)
        if not result['items']:
            return (), ()

        raw_items = result['items']
        if not raw_items:
            return (), ()

        headers = self.extract_column_headers(raw_items[0])
        items = self.extract_items(headers, raw_items)

        return headers, items
