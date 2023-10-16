# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import os
import msal

class AadService:

    def get_access_token():
        '''Generates and returns Access token

        Returns:
            string: Access token
        '''

        response = None
        try:
            if os.environ['AUTHENTICATION_MODE'].lower() == 'masteruser':

                # Create a public client to authorize the app with the AAD app
                clientapp = msal.PublicClientApplication(os.environ['CLIENT_ID'], authority=os.environ['AUTHORITY'])
                accounts = clientapp.get_accounts(username=os.environ['POWER_BI_USER'])

                if accounts:
                    # Retrieve Access token from user cache if available
                    response = clientapp.acquire_token_silent(os.environ['SCOPE'], account=accounts[0])

                if not response:
                    # Make a client call if Access token is not available in cache
                    response = clientapp.acquire_token_by_username_password(os.environ['POWER_BI_USER'], os.environ['POWER_BI_PASS'], scopes=os.environ['SCOPE'])     

            # Service Principal auth is the recommended by Microsoft to achieve App Owns Data Power BI embedding
            elif os.environ['AUTHENTICATION_MODE'].lower() == 'serviceprincipal':
                authority = os.environ['AUTHORITY'].replace('organizations', os.environ['TENANT_ID'])
                clientapp = msal.ConfidentialClientApplication(os.environ['CLIENT_ID'], client_credential=os.environ['CLIENT_SECRET'], authority=authority)

                # Make a client call if Access token is not available in cache
                response = clientapp.acquire_token_for_client(scopes=os.environ['SCOPE'])

            try:
                return response['access_token']
            except KeyError:
                raise Exception(response['error_description'])

        except Exception as ex:
            raise Exception('Error retrieving Access token\n' + str(ex))