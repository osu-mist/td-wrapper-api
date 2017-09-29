import json, requests, time, sys
from configuration import *

def get_access_token():
    post_data = {'username': td_api_user, 'password': td_api_pass}
    url = td_api_url + "/auth"
    request = requests.post(url, json=post_data)
    if request.status_code is not 200:
        print("Error: Unable to get access token.")
        print(request.text)
        sys.exit(1)
    
    return request.text

def get_services_with_long_descriptions(access_token):
    service_url = td_api_url + "/services"
    long_description_field = 'LongDescription'
    error = False
    
    auth_header = {'Authorization': "Bearer " + access_token}
    all_services = requests.get(service_url, headers=auth_header)
    all_services_with_long_descriptions = []

    for service in all_services.json():
       service_id = str(service['ID'])
       
       print("----Processing Service ID: %s----" % service_id)
       
       single_service_url = service_url + "/" + service_id
       single_service = requests.get(single_service_url, headers=auth_header)
       
       if single_service.status_code is 200:
           single_service_json = single_service.json()
           service[long_description_field] = single_service_json[long_description_field]
           all_services_with_long_descriptions.append(service)
           print("Added long description")
       else:
           error = True
           print("Error: " + single_service_url) 
       
       # TD's API allows 60 requests per minute, so we should delay the execution of this loop
       delay(single_service.elapsed.total_seconds())

    return all_services_with_long_descriptions, error

# Delays the script if the API response took a given amount of time
def delay(api_request_elapsed_seconds):
    if api_request_elapsed_seconds < 1:
       delay_seconds = 1 - api_request_elapsed_seconds
       print("Delay seconds: " + str(delay_seconds))
       time.sleep(delay_seconds)

if __name__ == '__main__':
   access_token = get_access_token()
   all_services_with_long_descriptions, error = get_services_with_long_descriptions(access_token)
   
   with open('services.json', 'w') as output_file:
       json.dump(all_services_with_long_descriptions, output_file, indent=4, sort_keys=True)

   if error:
       sys.exit(1)
