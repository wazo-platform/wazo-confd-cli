#!/usr/bin/env python3
# Copyright 2022-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import find_packages, setup

setup(
    name='wazo-confd-cli',
    version='1.0',
    author='Wazo Authors',
    author_email='dev@wazo.community',
    url='http://wazo.community',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['wazo-confd-cli = wazo_confd_cli.main:main'],
        'wazo_confd_cli.commands': [
            'user_list = wazo_confd_cli.commands.user:UserList',
            'endpoint_sip_add = wazo_confd_cli.commands.endpoint:EndpointSIPAdd',
            'endpoint_sip_list = wazo_confd_cli.commands.endpoint:EndpointSIPList',
            'endpoint_sip_template_list = wazo_confd_cli.commands.endpoint:EndpointSIPTemplateList',  # noqa: E501
        ],
    },
)
