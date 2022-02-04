# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class ListBuildingMixin:

    _columns = []
    _removed_columns = []

    def extract_column_headers(self, item):
        headers = item.keys()
        missing_columns = set(headers) - set(self._columns) - set(self._removed_columns)
        columns = self._columns + list(missing_columns)
        return columns

    def extract_items(self, headers, items):
        results = []
        for item in items:
            result = [item[header] for header in headers]
            results.append(result)
        return results
