# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from xivo.chain_map import ChainMap
from xivo.config_helper import parse_config_dir, read_config_file_hierarchy

logger = logging.getLogger(__name__)

_APP_NAME = 'wazo-confd-cli'
_DEFAULT_CONFIG = {
    'config_file': '/etc/{}/config.yml'.format(_APP_NAME),
    'extra_config_files': '/etc/{}/conf.d/'.format(_APP_NAME),
    'confd': {'host': 'localhost', 'port': 9486, 'prefix': None, 'https': False},
}


def _args_to_dict(parsed_args):
    confd_config = {}
    if parsed_args.hostname:
        confd_config['host'] = parsed_args.hostname
    if parsed_args.port:
        confd_config['port'] = parsed_args.port
    if parsed_args.ssl:
        confd_config['https'] = True
    if parsed_args.no_ssl:
        confd_config['https'] = False
    if parsed_args.token:
        confd_config['token'] = parsed_args.token
    if parsed_args.verify:
        confd_config['verify_certificate'] = True
    elif parsed_args.insecure:
        confd_config['verify_certificate'] = False
    elif parsed_args.cacert:
        confd_config['verify_certificate'] = parsed_args.cacert

    config = {'confd': confd_config}
    return config


def _read_user_config(parsed_args):
    if not parsed_args.config:
        return {}
    configs = parse_config_dir(parsed_args.config)
    return ChainMap(*configs)


def build(parsed_args):
    cli_config = _args_to_dict(parsed_args)
    user_file_config = _read_user_config(parsed_args)
    system_file_config = read_config_file_hierarchy(
        ChainMap(cli_config, user_file_config, _DEFAULT_CONFIG)
    )
    final_config = ChainMap(
        cli_config, user_file_config, system_file_config, _DEFAULT_CONFIG
    )
    return final_config
