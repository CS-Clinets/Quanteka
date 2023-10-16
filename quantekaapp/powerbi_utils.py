# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import os


class Utils:

    def check_config():
        '''Returns a message to user for missing configuration

        Args:
            app (Flask): Flask app object

        Returns:
            string: Error info
        '''

        if os.environ['AUTHENTICATION_MODE'] == '':
            return 'Please specify one of the two authentication modes'
        if os.environ['AUTHENTICATION_MODE'].lower() == 'serviceprincipal' and os.environ['TENANT_ID'] == '':
            return 'Tenant ID is not provided in the config.py file'
        elif os.environ['REPORT_ID'] == '':
            return 'Report ID is not provided in config.py file'
        elif os.environ['WORKSPACE_ID'] == '':
            return 'Workspace ID is not provided in config.py file'
        elif os.environ['CLIENT_ID'] == '':
            return 'Client ID is not provided in config.py file'
        elif os.environ['AUTHENTICATION_MODE'].lower() == 'masteruser':
            if os.environ['POWER_BI_USER'] == '':
                return 'Master account username is not provided in config.py file'
            elif os.environ['POWER_BI_PASS'] == '':
                return 'Master account password is not provided in config.py file'
        elif os.environ['AUTHENTICATION_MODE'].lower() == 'serviceprincipal':
            if os.environ['CLIENT_SECRET'] == '':
                return 'Client secret is not provided in config.py file'
        elif os.environ['SCOPE'] == '':
            return 'Scope is not provided in the config.py file'
        elif os.environ['AUTHORITY_URL'] == '':
            return 'Authority URL is not provided in the config.py file'

        return None
