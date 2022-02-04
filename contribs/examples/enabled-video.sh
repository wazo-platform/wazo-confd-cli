#!/usr/bin/env bash
# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

set -e
set -u  # fail if variable is undefined
set -o pipefail  # fail if command before pipe fails

usage() {
    echo "Usage: $0 -t <tenant-uuid> [-u <auth-username>]"
    exit 1
}

# Check for dependencies
if ! command -v wazo-auth-cli &> /dev/null; then
    echo "wazo-auth-cli is required to execute this script"
    exit 2
fi

if ! command -v wazo-confd-cli &> /dev/null; then
    echo "wazo-confd-cli is required to execute this script"
    exit 2
fi

# Parse command line arguments
while getopts t:u: flag
do
    case "${flag}" in
        t) TENANT_UUID="${OPTARG}";;
        u) AUTH_USERNAME="${OPTARG}";;
        :) usage;;
    esac
done

if [[ -z ${TENANT_UUID} ]]; then
    usage
fi

# Get a TOKEN
if [[ -v AUTH_USERNAME ]]; then
    echo -n "Password for ${AUTH_USERNAME}: "
    read -s AUTH_PASSWORD
    echo

    TOKEN=$(wazo-auth-cli token create --auth-username=${AUTH_USERNAME} --auth-password=${AUTH_PASSWORD})
else
    TOKEN=$(wazo-auth-cli token create)
fi

# Delete token when done
delete_token() {
    wazo-auth-cli token revoke "${TOKEN}"
}
trap delete_token EXIT

# Find WebRTC templates
while IFS= read -r row; do
    columns=( $row )
    case "${columns[1]}" in
        webrtc) 
            WEBRTC_TEMPLATE_UUID=${columns[0]}
            ;;
        webrtc_video)
            WEBRTC_VIDEO_TEMPLATE_UUID=${columns[0]}
            ;;
    esac
done < <(wazo-confd-cli --token ${TOKEN} endpoint sip template list --tenant ${TENANT_UUID} -fvalue)


if [[ ! -v WEBRTC_TEMPLATE_UUID ]]; then
    echo 'Missing "webrtc" template cannot continue'
    exit 3
fi

if [[ ! -v WEBRTC_VIDEO_TEMPLATE_UUID ]]; then
    echo 'Missing "webrtc_video" template cannot continue'
    exit 3
fi

# Fetch all WebRTC video endpoints
readarray -t WEBRTC_VIDEO_ENDPOINT_UUIDS < <(wazo-confd-cli --token ${TOKEN} endpoint sip list --template ${WEBRTC_VIDEO_TEMPLATE_UUID} --tenant ${TENANT_UUID} -f value | awk -F ' ' '{ print $1 }')

# Find WebRTC endpoints that do not have Video enabled
echo -n 'Updating WebRTC endpoints'
for endpoint_uuid in $(wazo-confd-cli --token ${TOKEN} endpoint sip list --template ${WEBRTC_TEMPLATE_UUID} --tenant ${TENANT_UUID} -f value | awk -F ' ' '{ print $1 }'); do
    if [[ ! "${WEBRTC_VIDEO_ENDPOINT_UUIDS[*]}" =~ "${endpoint_uuid}" ]]; then
        echo -n '.'
        wazo-confd-cli --token "${TOKEN}" endpoint sip add --template "${WEBRTC_VIDEO_TEMPLATE_UUID}" "${endpoint_uuid}"
    fi
done
echo
echo 'done'
