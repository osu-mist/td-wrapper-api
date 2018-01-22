import json
import requests
import time
import sys

from bs4 import BeautifulSoup
from configuration import td_api_url, td_api_user, td_api_pass


# Get an access token for authenticating API requests
def get_access_token():
    post_data = {'username': td_api_user, 'password': td_api_pass}
    url = td_api_url + '/auth'
    request = requests.post(url, json=post_data)
    if request.status_code != 200:
        print("Error: Unable to get access token.")
        print(request.text)
        sys.exit(1)

    return request.text


# Find span html tags and create a dict of their id and value
def get_parsed_html(raw_html):
    parsed_html = BeautifulSoup(raw_html, 'html.parser')
    span_dict = {}
    spans = parsed_html.find_all('span')

    for span in spans:
        span_id = span.get('id')
        if span_id:
            span_contents = span.contents
            span_full_string = ""

            # need a better way to get the literal contents of tag.
            # span.text strips out html tags
            for content in span_contents:
                span_full_string += str(content)

            span_dict[span_id] = span_full_string

    return span_dict


# Split category text into list
def get_parsed_categories(raw_categories):
    categories = raw_categories.split(' / ')

    return categories


# Get long description from individual service API
# and add it to object with all services. The API to
# get all services doesn't include each service's long description
def get_services_with_long_descriptions(access_token):
    service_url = td_api_url + '/services'

    # Field names used for parsing
    long_description_field = 'LongDescription'
    full_category_field = 'FullCategoryText'

    parsed_long_description_field = 'SpanTagsParsedFromLongDescription'
    parsed_categoires_field = 'CategoriesParsedFromFullCategoryText'

    error = False

    auth_header = {'Authorization': 'Bearer ' + access_token}
    all_services = requests.get(service_url, headers=auth_header)
    all_services_with_long_descriptions = {}

    for service in all_services.json():
        service_id = str(service['ID'])

        print("----Processing Service ID: %s----" % service_id)

        single_service_url = service_url + '/' + service_id
        single_service = requests.get(single_service_url, headers=auth_header)

        if single_service.status_code == 200:
            single_service_json = single_service.json()

            long_description = single_service_json[long_description_field]
            service[long_description_field] = long_description
            service[parsed_long_description_field] = get_parsed_html(
                    long_description)
            all_services_with_long_descriptions[service_id] = service
            print("Added long description and parsed HTML object")

            raw_categories = single_service_json[full_category_field]
            service[parsed_categoires_field] = get_parsed_categories(
                    raw_categories)
            print("Added parsed categories from FullCategoryText field")
        else:
            error = True
            print("Error: " + single_service_url)

        # TD's API allows 60 requests per minute,
        # so we should delay the execution of this loop
        delay(single_service.elapsed.total_seconds())

    return all_services_with_long_descriptions, error


# Delays the script if the API response took a given amount of time
def delay(api_request_elapsed_seconds):
    if api_request_elapsed_seconds < 1:
        delay_seconds = 1 - api_request_elapsed_seconds
        time.sleep(delay_seconds)


if __name__ == '__main__':
    access_token = get_access_token()
    services, error = get_services_with_long_descriptions(access_token)

    with open('services.json', 'w') as output_file:
        json.dump(services,
                  output_file,
                  indent=4,
                  sort_keys=True)

    if error:
        sys.exit(1)
