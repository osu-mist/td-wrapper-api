import json
import requests
import time
import sys

from bs4 import BeautifulSoup
from configuration import td_base_url, td_api_user, td_api_pass

# Minimum elapsed request time for a maximum of 50 requests made per minute
request_time_min = 1.2

fields_to_parse = [
    'AccessRequirements', 'AdditionalLinkTitle', 'AdditionalLinkURL',
    'AudienceAssociated', 'AudienceDepartments', 'AudienceDescription',
    'AudienceEmployees', 'AudienceStudents', 'BusinessContact',
    'BusinessImpact', 'BusinessOwner', 'BusinessPriority', 'BusinessUnit',
    'ChargesOptionsFees', 'Cost', 'EnablingServices', 'EnhancingServices',
    'EscalationContact', 'LOSLearn', 'LOSOperate', 'LOSResearch', 'LOSWork',
    'LongDescription', 'RelatedServices', 'RequestAccess', 'SLA',
    'SecurityRating', 'ServiceHours', 'ServiceManager', 'ServiceOwner',
    'ServiceType', 'ShortDescription', 'SupportAvailability', 'SynonymsList',
    'Training', 'Value'
]


# Get an access token for authenticating API requests
def get_access_token(url):
    post_data = {'username': td_api_user, 'password': td_api_pass}
    res = requests.post(f'{url}/auth', json=post_data)
    msg = res.text
    if res.status_code != 200:
        sys.exit(f'Error - Unable to get access token. API Response: {msg}')

    return msg


# Find span html tags and create a dict of their id and value
def get_parsed_html(raw_html):
    parsed_html = BeautifulSoup(raw_html, 'html.parser')
    parsed_span_dict = {}
    spans = parsed_html.find_all('span')

    for span in spans:
        span_id = span.get('id')
        if span_id:
            # need a better way to get the literal contents of tag.
            # span.text strips out html tags
            full_string = ''.join([str(content) for content in span.contents])

            if span_id == 'SynonymsList':
                parsed_span_dict[span_id] = full_string.split(', ')
            else:
                parsed_span_dict[span_id] = full_string

    span_dict = {}

    for field in fields_to_parse:
        span_dict[field] = parsed_span_dict.get(field)

    return span_dict


# Uncapitalize key or adjust key to be readable camelCase
def uncapitalize(key):
    if key.startswith('LOS'):
        return key.replace('LOS', 'los')
    elif key == 'SLA':
        return key.lower()
    else:
        return key[0].lower() + key[1:]


# Get long description from individual service API
# and add it to object with all services. The API to
# get all services doesn't include each service's long description
def get_services_with_long_descriptions(access_token, api_url):
    service_url = f'{api_url}/services'

    # Field names used for parsing
    long_description_field = 'LongDescription'
    full_category_field = 'FullCategoryText'

    error = False

    auth_header = {'Authorization': f'Bearer {access_token}'}
    all_services = requests.get(service_url, headers=auth_header)
    all_services_with_long_descriptions = {}

    for service in all_services.json():
        service_id = str(service['ID'])

        print(f'----Processing Service ID: {service_id}----')

        single_service_url = f'{service_url}/{service_id}'
        single_service = requests.get(single_service_url, headers=auth_header)

        if single_service.status_code == 200:
            single_service_json = single_service.json()

            long_description = single_service_json[long_description_field]
            service[long_description_field] = long_description
            spans = get_parsed_html(long_description)

            for key, value in spans.items():
                if key == 'LongDescription' or key == 'ShortDescription':
                    key = 'span' + key
                service[key] = value

            print('Added long description and parsed HTML object')

            raw_categories = single_service_json[full_category_field]
            service['categoires'] = raw_categories.split(' / ')
            print('Added parsed categories from FullCategoryText field')

            ticket_endpoint = '/TDClient/Requests/TicketRequests/NewForm?ID='
            ticket_url = f'{td_base_url}{ticket_endpoint}{service_id}'
            service['newTicketUrl'] = ticket_url

            clean_service = {}
            for key in service:
                # Filter out duplicated data
                if key in ['Uri', 'ID']:
                    continue

                # Change value to string if field ends with 'ID'
                value = service[key]
                if key.endswith('ID'):
                    value = str(value)
                clean_service[uncapitalize(key)] = value

            all_services_with_long_descriptions[service_id] = clean_service
        else:
            error = True
            print(f'Error: {single_service_url}')
            print(f'HTTP Status Code: {single_service}')
            print(single_service.text)

        # TD's API allows 60 requests per minute,
        # so we should delay the execution of this loop
        delay(single_service.elapsed.total_seconds())

    return all_services_with_long_descriptions, error


# Delays the script if the API response took a given amount of time
def delay(api_request_elapsed_seconds):
    if api_request_elapsed_seconds < request_time_min:
        delay_seconds = request_time_min - api_request_elapsed_seconds
        time.sleep(delay_seconds)


if __name__ == '__main__':
    td_api_url = f'{td_base_url}/TDWebApi/api'
    access_token = get_access_token(td_api_url)

    services, error = get_services_with_long_descriptions(
        access_token, td_api_url)

    with open('services.json', 'w') as output_file:
        json.dump(services, output_file, indent=4, sort_keys=True)

    if error:
        sys.exit(1)
