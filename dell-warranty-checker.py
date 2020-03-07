#!/usr/bin/python3

from datetime import datetime
import sys
import requests
import json


'''
    dell-warranty-checker.py - check the warranty of dell equipments.
    -----------------------------------------------------------------------------------
    This script will first get the access token through sending the CLIENT_ID and CLIENT_SECRET
    information to the Dell API Endpoint for Auth, then send a request to the Dell API Endpoint
    for Asset Warranty with the products service tags that were passed as arguments to the script.
    Finally, with the response data about the products, it will print the info about the warranty
    of each one of them.
    ./dell-warranty-checker.py 'BB0MKF2,B41KKF2,6W842V1,W233F67'
        ./dell-warranty-checker.py 'BB3PKF2,B41JKF2,6W742V1,W433F67'

        W433F67 - ERROR - This tag may not exist
        BB3PKF2 - LATITUDE E7470 - Warranty OK - 561 days remaining.
        6W742V1 - VOSTRO 3550 - Warranty CRITICAL - 2476 days past.
        B41JKF2 - POWEREDGE R730XD - Warranty CRITICAL - 175 days past.
    -----------------------------------------------------------------------------------
    Tested:
        Python 3.6.9
'''


# Test
if (len(sys.argv) != 2):
    print("ERROR - This script should receive just one argument. As follows:\n./dell-warranty-checker.py 'BB0MKF2,B41KKF2,6W842V1,W233F67'")
    sys.exit(1)


# Functions
def get_access_token(c_id, c_secret):
    '''
        This method will send the c_id and c_secret to the Dell API Endpoint for authentication
        and returns the access token.
    '''
    try:
        dell_API_endpoint_for_auth = 'https://apigtwb2c.us.dell.com/auth/oauth/v2/token'

        client_id = c_id
        client_secret = c_secret

        auth_params = {'grant_type': 'client_credentials',
                       'client_id': client_id, 'client_secret': client_secret}
        auth_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'}

        auth_response = requests.post(
            dell_API_endpoint_for_auth, params=auth_params, headers=auth_headers)

        if (auth_response.status_code != 200):
            sys.exit('ERROR - Coult not retrieve the access token!')

        return auth_response.json()["access_token"]
    except:
        sys.exit('ERROR - Coult not retrieve the access token!')


def get_warranty_data(tok):
    '''
        This method send the service tags, given as argument to the script, to the Dell API Endpoint
        for Asset Warranty and returns a JSON with the data about the products.
    '''
    try:
        dell_API_endpoint_for_asset_warranty = 'https://apigtwb2c.us.dell.com/PROD/sbil/eapi/v5/asset-entitlements'
        tags = sys.argv[1]  # Service TAG as argument

        payload = {'servicetags': tags}
        head = {'Accept': 'application/json',
                'Authorization': 'Bearer ' + tok}

        response = requests.get(
            dell_API_endpoint_for_asset_warranty, params=payload, headers=head)

        if (response.status_code != 200):
            print("UNKNOWN - code %s REQUEST ERROR." % response.status_code)
            sys.exit(1)
        else:
            return json.loads(response.content)
    except:
        sys.exit('ERROR - Coult not get the response data!')


def print_remaining_days(s_tag, p_model, i_date, f_date, r_days):
    '''
        This method will print the warranty information for the given product.
    '''
    if (i_date < f_date) and r_days > 90:
        print(s_tag + ' - ' + p_model +
              ' - Warranty OK - %d days remaining.' % r_days)
    if (i_date < f_date) and r_days < 90 and r_days > 30:
        print(s_tag + ' - ' + p_model +
              ' - Warranty WARNING - %d days remaining.' % r_days)
    if (i_date < f_date) and r_days < 30:
        print(s_tag + ' - ' + p_model +
              ' - Warranty CRITICAL - %d days remaining.' % r_days)
    if (i_date > f_date):
        print(s_tag + ' - ' + p_model +
              ' - Warranty CRITICAL - %d days past.' % r_days)


# Variables
CLIENT_ID = 'xxxxxxxxxxxxxxxxx'
CLIENT_SECRET = 'xxxxxxxxxxxxxxxxx'


# Execution
if __name__ == "__main__":
    token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    response_data = get_warranty_data(token)

    for item in response_data:
        try:
            if (item['invalid'] == True):
                print(item['serviceTag'] + ' - ERROR - This tag may not exist')
            else:
                service_tag = item['serviceTag']
                model = item['productLineDescription']

                if (item['entitlements'] != []):
                    item_end_date = item['entitlements'][-1]['endDate']

                    if (item_end_date is not None):
                        item_end_date = item_end_date.split('T')[0]
                    else:
                        print(service_tag + ' - ERROR - NONE as end_date')

                    end_date = datetime.strptime(item_end_date, "%Y-%m-%d")
                    today_date = datetime.now()

                    remaining_days = abs((today_date-end_date).days)

                    print_remaining_days(service_tag, model,
                                         today_date, end_date, remaining_days)
                else:
                    print(service_tag + ' - ' + model +
                          ' - ERROR - entitlements is empty')
        except:
            print(item['serviceTag'] + ' - UNKNOWN ERROR!!!')
