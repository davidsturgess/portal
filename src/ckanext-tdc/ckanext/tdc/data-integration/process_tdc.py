import requests
import json
import sys
from urllib.parse import urljoin
import os
from dotenv import load_dotenv
import time

load_dotenv()              
# CKAN Configuration
CKAN_URL = os.getenv('CKAN_URL')
API_KEY = os.getenv('API_KEY')

def create_resource_remote_url_with_format(dataset_name, resource_remote_url,resource_name, resource_format):
    '''
    Add resource in datasets
    '''
    print('CREATING RESOURCE')
    data = {
      'package_id': dataset_name,
      'url': resource_remote_url,
      'name': resource_name,
      'format': resource_format,
      'resource_type': 'data'
    }
    resp = requests.post(
        urljoin(CKAN_URL, '/api/3/action/resource_create'),
        data=data,
        headers={'Authorization': API_KEY},
    )

def create_resource_remote_url(dataset_name, resource_remote_url,resource_name):
    '''
    Add resource in datasets
    '''
    print('CREATING RESOURCE')
    data = {
      'package_id': dataset_name,
      'url': resource_remote_url,
      'name': resource_name,
      'resource_type': 'data'
    }
    resp = requests.post(
        urljoin(CKAN_URL, '/api/3/action/resource_create'),
        data=data,
        headers={'Authorization': API_KEY},
    )

def create_resource_local_file(dataset_name,resource_name):
    # File to upload
    FILE_PATH = resource_name         # Replace with the path to your local CSV file

    # CKAN resource_create endpoint
    endpoint = f'{CKAN_URL}/api/3/action/resource_create'

    # Set up headers including the API key
    headers = {
        'Authorization': API_KEY,
    }
    if "/" in resource_name:
        resource_name = resource_name.split("/")[1]
    # Set up the data and file to be sent in the request
    data = {
        'package_id': dataset_name,  # Dataset ID
        'name': resource_name, # Optional: Name of the resource
        'format': 'csv',          # Optional: Format of the file
        'resource_type': 'data'
    }
    
    # Read the file in binary mode
    with open(FILE_PATH, 'rb') as file:
        files = {
            'upload': file,
        }

        # Send the POST request
        resp = requests.post(endpoint, headers=headers, data=data, files=files)
    file.close()
    # Check response
    if resp.status_code == 200:
        print('Resource created successfully:', resp.json())
    else:
        print('Error creating resource:', resp.text)

def create_resource_local_file_with_format(dataset_name,resource_name,resource_format):
    # File to upload
    FILE_PATH = resource_name         # Replace with the path to your local CSV file

    # CKAN resource_create endpoint
    endpoint = f'{CKAN_URL}/api/3/action/resource_create'

    # Set up headers including the API key
    headers = {
        'Authorization': API_KEY,
    }

    # Set up the data and file to be sent in the request
    data = {
        'package_id': dataset_name,  # Dataset ID
        'name': resource_name, # Optional: Name of the resource
        'format': resource_format,          # Optional: Format of the file
        'resource_type': 'data'
    }

    # Read the file in binary mode
    with open(FILE_PATH, 'rb') as file:
        files = {
            'upload': file,
        }

        # Send the POST request
        resp = requests.post(endpoint, headers=headers, data=data, files=files)

    # Check response
    if resp.status_code == 200:
        print('Resource created successfully:', resp.json())
    else:
        print('Error creating resource:', resp.text())
# Our World in Data - Road Travel
def dataset_1(org_id, dataset_title, resource_name):
    '''
    Add dataset in the organizations
    '''
    
    dataset_name = dataset_title.lower().replace(' ', '-')
    data = {
        'title': dataset_title,  # Replace with your actual dataset title
        'name': dataset_name,    # Replace with your actual dataset name
        'notes': ' ',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,     # Replace with your organization ID
        'temporal_coverage_start': '2013-01-01',
        'temporal_coverage_end': '2019-01-01',
        "geographies": ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'},
            {'title': 'EEA', 'url': 'https://www.eea.europa.eu/en'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger Vehicle Fleet',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['#','%'],
        'dimensioning': 'registrations by type'
    }
    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json'
    }
    # whenever we cannot find information on  data updates, we will use "as_needed" for frequency
    # overview_text will be provided manually later
    # topic is missing/null vehicle-read-traffic
    # indicators we need a similar approach as for tags
    
    try:
        json_data = json.dumps(data)
        print("JSON Payload to be sent:", json_data) 
    except Exception as e:
        print("Error converting data to JSON:", str(e))
    
    response = requests.post(
        urljoin(CKAN_URL, '/api/3/action/package_create'),
        data=json_data,
        headers=headers
    )
    
    if response.status_code == 200 or response.status_code==409:
        print('Dataset created successfully:', response.json())
        create_resource_local_file(dataset_name, resource_name)
    else:
        print('Error creating dataset:', response.text)
def dataset_2(org_id, dataset_title, resource_name):
    '''
    Add dataset in the organizations
    '''
    
    dataset_name = dataset_title.lower().replace(' ', '-')
    data = {
        'title': dataset_title,  # Replace with your actual dataset title
        'name': dataset_name,    # Replace with your actual dataset name
        'notes': 'Based on new passenger vehicle registrations and for battery electric vehicles only',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,     # Replace with your organization ID
        'temporal_coverage_start': '2001-01-01',
        'temporal_coverage_end': '2019-01-01',
        "geographies": ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'},
            {'title': 'EEA', 'url': 'https://www.eea.europa.eu/en'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Electric vehicle fleet',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'Share of new battery electric passenger vehicles'
    }
    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json'
    }

    try:
        json_data = json.dumps(data)
        print("JSON Payload to be sent:", json_data) 
    except Exception as e:
        print("Error converting data to JSON:", str(e))
    
    response = requests.post(
        urljoin(CKAN_URL, '/api/3/action/package_create'),
        data=json_data,
        headers=headers
    )
    
    if response.status_code == 200 or response.status_code == 409:
        print('Dataset created successfully:', response.json())
        create_resource_local_file(dataset_name, resource_name)
    else:
        print('Error creating dataset:', response.text)
def dataset_3(org_id, dataset_title, resource_name):
    '''
    Add dataset in the organizations
    '''
    
    dataset_name = dataset_title.lower().replace(' ', '-')
    data = {
        'title': dataset_title,  # Replace with your actual dataset title
        'name': dataset_name,    # Replace with your actual dataset name
        'notes': 'Carbon intensity of newly registered passenger vehicles is measured in grams of carbon dioxide emitted per kilometer driven (grams CO₂ per km).',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,     # Replace with your organization ID
        'temporal_coverage_start': '2001-01-01',
        'temporal_coverage_end': '2019-01-01',
        "geographies": ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'},
            {'title': 'EEA', 'url': 'https://www.eea.europa.eu/en'}        
            ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Carbon intensity of new passenger vehicles',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['g/km'],
        'dimensioning': 'CO2 emissions (averaged across all types of passenger vehicles)'
    }
    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json'
    }

    try:
        json_data = json.dumps(data)
        print("JSON Payload to be sent:", json_data) 
    except Exception as e:
        print("Error converting data to JSON:", str(e))
    
    response = requests.post(
        urljoin(CKAN_URL, '/api/3/action/package_create'),
        data=json_data,
        headers=headers
    )
    
    if response.status_code == 200:
        print('Dataset created successfully:', response.json())
        create_resource_local_file(dataset_name, resource_name)
    else:
        print('Error creating dataset:', response.text)
def dataset_4(org_id, dataset_title, resource_name):
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-'),
        'notes': 'Fuel economy is measured in liters per 100 kilometers traveled. This is shown as the average for new passenger vehicle registrations.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2001-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'},
            {'title': 'EEA', 'url': 'https://www.eea.europa.eu/en'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Fuel economy of new passenger vehicles',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['litres/100km'],
        'dimensioning': 'fuel economy (averaged across all types of passenger vehicles)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        if response.status_code == 200 or response.status_code == 409:
            print('Dataset created successfully:', response.json())
            create_resource_local_file(data['name'], resource_name)
        else:
            print('Error creating dataset:', response.text)
    except Exception as e:
        print('Error creating dataset:', str(e))
# Our World in Data - Aviation
def dataset_5(org_id, dataset_title, resource_name):
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-'),
        'notes': 'Available kilometers measure carrying capacity: the number of seats available multiplied by the number of kilometers flown. Passenger-seat kilometers measure the actual number of kilometers flown by paying customers.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1929-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICAO', 'url': 'https://www.icao.int/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Global airline passenger capacity and traffic',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['seat km','passenger seat km'],
        'dimensioning': 'passenger capacity and traffic'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_6(org_id, dataset_title, resource_name):
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-'),
        'notes': ' ',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1950-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICAO', 'url': 'https://www.icao.int/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Global airline passenger load factor',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'passenger load factor'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_7(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name':'per-capita-co2-emissions-from-domestic-aviation-2018',
        'notes': 'Domestic aviation represents flights which depart and arrive within the same country.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Carbon Footprint Domestic Flights',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['kg/capita'],
        'dimensioning': 'CO2 emissions'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_8(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name':'co2-emissions-from-domestic-air-travel-2018',
        'notes': 'Domestic aviation represents flights which depart and arrive within the same country.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Carbon Footprint Domestic Flights',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'CO2 emissions'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_9(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name':'share-of-global-co2-emissions-from-domestic-air-travel-2018',
        'notes': 'Domestic aviation represents flights which depart and arrive within the same country.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Carbon Footprint Domestic Flights',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'Share of CO2 emissions from aviation on total CO2 emissions'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_10(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name':'per-capita-co2-emissions-from-international-aviation-2018',
        'notes': 'International aviation emissions are here allocated to the country of departure of each flight.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Carbon Footprint International Flights',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['kg/capita'],
        'dimensioning': 'CO2 emissions (allocated to country of departure)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_11(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name':'co2-emissions-from-international-aviation-2018',
        'notes': 'International aviation emissions are here allocated to the country of departure of each flight.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Carbon Footprint International Flights',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'CO2 emissions (allocated to country of departure)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_12(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name':'share-of-global-co2-emissions-from-international-aviation-2018',
        'notes': 'International aviation emissions are here allocated to the country of departure of each flight.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Graver et al. (2019)', 'url': 'https://ourworldindata.org/grapher/share-co2-international-aviation'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['international-aviation'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Carbon Footprint International Flights',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'Share of CO2 emissions from aviation in total CO2 emissions'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e))    
def dataset_13(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name':'per-capita-co2-emissions-from-international-passenger-flights-tourism-adjusted-2018',
        'notes': 'International aviation emissions are allocated to the country of departure, then adjusted for tourism.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Graver et al. (2019)', 'url': 'https://ourworldindata.org/grapher/per-capita-co2-international-flights-adjusted'},
            {'title': 'World Bank data', 'url': 'https://data.worldbank.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Carbon Footprint International Flights',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['kg/capita'],
        'dimensioning': 'CO2 emissions (tourism adjusted)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_14(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name':'per-capita-co2-emissions-from-commercial-aviation-tourism-adjusted-2018',
        'notes': 'This includes both domestic and international flights. International aviation emissions are allocated to the country of departure, and then adjusted for tourism.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Graver et al. (2019)', 'url': 'https://ourworldindata.org/grapher/per-capita-co2-aviation-adjusted'},
            {'title': 'World Bank data', 'url': 'https://data.worldbank.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Carbon Footprint Domestic and International',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['kg/capita'],
        'dimensioning': 'CO2 emissions (tourism adjusted)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e))  
def dataset_15(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name':'per-capita-co2-emissions-from-aviation-2018',
        'notes': 'This includes both domestic and international flights. International aviation emissions are allocated to the country of dAviation emissions include both domestic and international flights. International aviation emissions are allocated to the country of departure of each flight.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Graver et al. (2019)', 'url': 'https://ourworldindata.org/grapher/per-capita-co2-aviation'},
            {'title': 'UN Population Prospects', 'url': 'https://population.un.org/wpp/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Carbon Footprint Domestic and International',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['kg/capita'],
        'dimensioning': 'CO2 emissions (allocated to country of departure)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e))  
def dataset_16(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name':'co2-emissions-from-aviation-2018',
        'notes': 'Aviation emissions include both domestic and international flights. International aviation emissions are here allocated to the country of departure of each flight.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Carbon Footprint Domestic and International',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'CO2 emissions (allocated to country of departure)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_17(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name':'share-of-global-co2-emissions-from-aviation-2018',
        'notes': 'Aviation emissions include both domestic and international flights. International aviation emissions are allocated to the country of departure of each flight.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Carbon Footprint Domestic and International',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'Share of CO2 emissions from aviation in total CO2 emissions'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_18(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name':'per-capita-domestic-aviation-passenger-kilometers-2018',
        'notes': 'Revenue Passenger Kilometers (RPK) measures the number of kilometers traveled by paying passengers. It is calculated as the number of revenue passengers multiplied by the total distance traveled.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Most domestic flights',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['PKM/capita'],
        'dimensioning': 'passenger demand'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_19(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name':'share-of-global-domestic-aviation-passenger-kilometers-2018',
        'notes': 'Revenue Passenger Kilometers (RPK) measures the number of kilometers traveled by paying passengers. It is calculated as the number of revenue passengers multiplied by the total distance traveled.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Most domestic flights',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'Share of passenger demand in total air traffic'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_20(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name':'total-domestic-aviation-passenger-kilometers-2018',
        'notes': 'Revenue Passenger Kilometers (RPK) measures the number of kilometers traveled by paying passengers. It is calculated as the number of revenue passengers multiplied by the total distance traveled.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Most domestic flights',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['PKM/year'],
        'dimensioning': 'passenger demand'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_21(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name':'per-capita-international-aviation-passenger-kilometers-2018',
        'notes': 'Revenue Passenger Kilometers (RPK) measures the number of kilometers traveled by paying passengers. It is calculated as the number of revenue passengers multiplied by the total distance traveled. International RPKs are allocated to the country of departure.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Graver et al. (2019)', 'url': 'https://ourworldindata.org/grapher/per-capita-international-aviation-km'},
            {'title': 'UN Population Prospects', 'url': 'https://population.un.org/wpp/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Most international flights',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['PKM/capita'],
        'dimensioning': 'passenger demand'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_22(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name':'share-of-global-passenger-kilometers-from-international-aviation-2018',
        'notes': 'Revenue Passenger Kilometers (RPK) measures the number of kilometers traveled by paying passengers. It is calculated as the number of revenue passengers multiplied by the total distance traveled. International aviation is here allocated to the country of departure.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Graver et al. (2019)', 'url': 'https://ourworldindata.org/grapher/share-international-aviation-km'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Most international flights',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'Share of passenger demand in total air traffic'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_23(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',',''),
        'notes': 'Revenue Passenger Kilometers (RPK) measures the number of kilometers traveled by paying passengers. It is calculated as the number of revenue passengers multiplied by the total distance traveled. International aviation is here allocated to the country of departure.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Most international flights',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['PKM/year'],
        'dimensioning': 'passenger demand'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_24(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',',''),
        'notes': 'Revenue Passenger Kilometers (RPK) measures the number of kilometers traveled by paying passengers. Both domestic and international air travel are included here. International flights are allocated to the country of departure.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Total air travel',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['PKM/capita'],
        'dimensioning': 'passenger demand'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_25(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',',''),
        'notes': 'Revenue Passenger Kilometers (RPK) measures the number of kilometers traveled by paying passengers. Both domestic and international air travel are included here. International flights are allocated to the country of departure.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Total air travel',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'Share of passenger demand in total air traffic'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_26(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',',''),
        'notes': 'Revenue Passenger Kilometers (RPK) measures the number of kilometers traveled by paying passengers. Both domestic and international air travel are included here. International flights are allocated to the country of departure.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-12-31',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICCT', 'url': 'https://theicct.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Total air travel',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['PKM/year'],
        'dimensioning': 'passenger demand'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_27(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',',''),
        'notes': 'Air freight is the volume of freight, express, and diplomatic bags carried on each flight stage (operation of an aircraft from takeoff to its next landing), measured in metric tonnes times kilometers traveled.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICAO (via World Bank)', 'url': 'https://www.icao.int/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Air transport freight ',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['TKM/year'],
        'dimensioning': 'freight transport demand'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
# Our World in Data - Rail
def dataset_28(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',',''),
        'notes': 'The number of passengers transported by rail, multiplied by the kilometers traveled. This is measured in passenger-kilometers.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1995-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'International Union of Railways(via World Bank)', 'url': 'https://uic.org/'},
            {'title': 'OECD (via World Bank)', 'url': 'https://www.oecd.org/en.html'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Railway passengers',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['PKM/year'],
        'dimensioning': 'passenger demand'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
# Our World in Data - Energy intensity of transport
def dataset_29(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',',''),
        'notes': 'Energy intensity is measured as kilowatt-hours of energy needed per passenger kilometer. This is based on data from the US.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1960-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'United States department of Transportation, Bureau of Transportation Statistics (BTS)', 'url': 'https://www.usa.gov/agencies/bureau-of-transportation-statistics'}
        ],
        'language': 'en',
        'sectors': ['rail','road','water','aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Average energy intensity of transport across different modes of travel',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['kWh/PKM'],
        'dimensioning': 'Energy intensity'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
# Our World in Data - CO2 emissions from transport
def dataset_30(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': 'per-capita-co2-emissions-from-transport-2020',
        'notes': 'Emissions are measured in tonnes per person. International aviation and shipping emissions are not included.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1990-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Climate Watch', 'url': 'https://www.climatewatchdata.org/'},
            {'title': 'Climate Watch', 'url': 'https://www.climatewatchdata.org/'}
        ],
        'language': 'en',
        'sectors': ['rail','road','aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Per Capita transport emissions from transport',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['tonnes/capita'],
        'dimensioning': 'CO2 emissions (road, rail, bus, domestic air travel)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_31(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': 'co2-emissions-from-transport-2020',
        'notes': 'Emissions are measured in tonnes. Domestic aviation and shipping emissions are included at the national level. International aviation and shipping emissions are included only at the global level.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1990-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Climate Watch', 'url': 'https://www.climatewatchdata.org/'}
        ],
        'language': 'en',
        'sectors': ['rail','road','aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'total transport emissions',
        'data_provider': 'Our World in Data',
        'url': 'https://ourworldindata.org/',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'total CO2 emissions (road, rail, bus, domestic air travel)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
# Climatetrace
def dataset_32(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': 'domestic-aviation-country-emissions-climate-trace',
        'notes': 'Annual country-level emissions by greenhouse gas from 2015-2022.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Climate trace', 'url': 'https://climatetrace.org/downloads'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Transport GHG emissions',
        'data_provider': 'Climate trace',
        'url': 'https://climatetrace.org',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'emissions of CO2,N2O,CH4, CO2e 20yr, CO2e 100yr sorted by country and year'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_33(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': 'international-aviation-country-emissions-climate-trace',
        'notes': 'Annual country-level emissions by greenhouse gas from 2015-2022.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Climate trace', 'url': 'https://climatetrace.org/downloads'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['international-aviation'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Transport GHG emissions',
        'data_provider': 'Climate trace',
        'url': 'https://climatetrace.org',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'emissions of CO2,N2O,CH4, CO2e 20yr, CO2e 100yr sorted by country and year'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_34(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': 'other-transport_country-emissions-climate-trace',
        'notes': 'Annual country-level emissions by greenhouse gas from 2015-2022.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Climate trace', 'url': 'https://climatetrace.org/downloads'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Transport GHG emissions',
        'data_provider': 'Climate trace',
        'url': 'https://climatetrace.org',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'emissions of CO2,N2O,CH4, CO2e 20yr, CO2e 100yr sorted by country and year'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_35(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': 'railways_country-emissions-climate-trace',
        'notes': 'Annual country-level emissions by greenhouse gas from 2015-2022.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Climate trace', 'url': 'https://climatetrace.org/downloads'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Transport GHG emissions',
        'data_provider': 'Climate trace',
        'url': 'https://climatetrace.org',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'emissions of CO2,N2O,CH4, CO2e 20yr, CO2e 100yr sorted by country and year'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_36(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': 'road-transportation-country-emissions-climate-trace',
        'notes': 'Annual country-level emissions by greenhouse gas from 2015-2022.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Climate trace', 'url': 'https://climatetrace.org/downloads'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','two-three-wheelers','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Transport GHG emissions',
        'data_provider': 'Climate trace',
        'url': 'https://climatetrace.org',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'emissions of CO2,N2O,CH4, CO2e 20yr, CO2e 100yr sorted by country and year'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_37(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': 'domestic-shipping-country-emissions-climate-trace',
        'notes': 'Annual country-level emissions by greenhouse gas from 2015-2022.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Climate trace', 'url': 'https://climatetrace.org/downloads'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Transport GHG emissions',
        'data_provider': 'Climate trace',
        'url': 'https://climatetrace.org',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'emissions of CO2,N2O,CH4, CO2e 20yr, CO2e 100yr sorted by country and year'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e))   
def dataset_38(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': 'international-shipping-country-emissions-climate-trace',
        'notes': 'Annual country-level emissions by greenhouse gas from 2015-2022.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Climate trace', 'url': 'https://climatetrace.org/downloads'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Transport GHG emissions',
        'data_provider': 'Climate trace',
        'url': 'https://climatetrace.org',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'emissions of CO2,N2O,CH4, CO2e 20yr, CO2e 100yr sorted by country and year'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e))   
# WorldBank AIR
def dataset_39(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',',''),
        'notes': 'International Civil Aviation Organization, Civil Aviation Statistics of the World and ICAO staff estimates.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'International Civil Aviation Organization', 'url': 'https://www.icao.int/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['freight','passenger'],
        'frequency': 'as_needed',
        'indicators': 'Registered carrier departures (domestic takeoffs and takeoffs abroad of air carriers registered in the country) in line, bar and map diagram',
        'data_provider': 'World Bank',
        'url': 'https://data.worldbank.org/indicators/IS.AIR.DPRT?view=chart',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_40(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')',''),
        'notes': 'International Civil Aviation Organization, Civil Aviation Statistics of the World and ICAO staff estimates.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'International Civil Aviation Organization', 'url': 'https://www.icao.int/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Air freight',
        'data_provider': 'World Bank',
        'url': 'https://data.worldbank.org/indicators/IS.AIR.GOOD.MT.K1',
        'data_access': 'publicly available',
        'units': ['TKM'],
        'dimensioning': ''
        
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e))    
def dataset_41(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')',''),
        'notes': 'International Civil Aviation Organization, Civil Aviation Statistics of the World and ICAO staff estimates.',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'International Civil Aviation Organization', 'url': 'https://www.icao.int/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passengers carried (domestic and international aircraft passengers of air carriers registered in the country)',
        'data_provider': 'World Bank',
        'url': 'https://data.worldbank.org/indicators/IS.AIR.PSGR',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e))  
# WorldBank RAIL
def dataset_42(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')',''),
        'notes': 'Internation Union of Railways ( UIC )',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1995-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'International Union of Railways (UIC)', 'url': 'https://uic.org/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Total route network',
        'data_provider': 'World Bank',
        'url': 'https://data.worldbank.org/indicators/IS.RRS.TOTL.KM',
        'data_access': 'publicly available',
        'units': ['km'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_43(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')',''),
        'notes': 'Internation Union of Railways ( UIC ), OECD Statistics',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1995-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'International Union of Railways (UIC)', 'url': 'https://uic.org/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Rail freight',
        'data_provider': 'World Bank',
        'url': 'https://data.worldbank.org/indicators/IS.RRS.GOOD.MT.K6',
        'data_access': 'publicly available',
        'units': ['TKM'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_44(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')',''),
        'notes': 'Internation Union of Railways ( UIC Railisa Database ), OECD Statistics',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1995-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'International Union of Railways (UIC)', 'url': 'https://uic.org/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Rail passenger travel',
        'data_provider': 'World Bank',
        'url': 'https://data.worldbank.org/indicators/IS.RRS.PASG.KM',
        'data_access': 'publicly available',
        'units': ['PKM'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
# WorldBank PORT
def dataset_45(org_id, dataset_title, resource_name):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')','').replace(':',''),
        'notes': 'UNCTAD ( unctad.org/en/Pages/statistics.aspx )',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2000-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'UNCTAD', 'url': 'https://unctad.org/'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['international-maritime','coastal-shipping'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Container port traffic (flow of containers from land to sea transport modes and vice versa)',
        'data_provider': 'World Bank',
        'url': 'https://data.worldbank.org/indicators/IS.SHP.GOOD.TU',
        'data_access': 'publicly available',
        'units': ['TEU'],
        'dimensioning': 'emissions of CO2,N2O,CH4, CO2e 20yr, CO2e 100yr sorted by country and year'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        create_resource_local_file(data['name'], resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
# OICA REMOTE RESOURCE
def dataset_46(org_id, dataset_title, resource_url):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')','').replace(':',''),
        'notes': 'Registration or sales of new passenger cars, commercial vehicles, all vehicles',
        'license_id': 'notspecified',
        'owner_org': org_id,
        'temporal_coverage_start': '2019-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Cooperation with Ward Auto (America)', 'url': 'https://www.wardsauto.com/'},
            {'title': 'Asian Automotive Analysis Fourin (Asia)', 'url': 'https://aaa.fourin.com/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','private-cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Sales new cars',
        'data_provider': 'OICA',
        'url': 'https://www.oica.net/category/sales-statistics/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'Registration or sales of new passenger cars, commercial vehicles, all vehicles'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        print(response.text)
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        filename = resource_url.split('/')[-1]  
        resource_name = filename.split('.')[0] 
        create_resource_remote_url(data['name'], resource_url,resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_47(org_id, dataset_title, resource_url):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')','').replace(':',''),
        'notes': 'Passenger cars, commercial vehicles, all vehicles, motorization rate',
        'license_id': 'notspecified',
        'owner_org': org_id,
        'temporal_coverage_start': '2005-01-01',
        'temporal_coverage_end': '2015-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Cooperation with Ward Auto (America)', 'url': 'https://www.wardsauto.com/'},
            {'title': 'Asian Automotive Analysis Fourin (Asia)', 'url': 'https://aaa.fourin.com/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','private-cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Vehicle fleet',
        'data_provider': 'OICA',
        'url': 'https://www.oica.net/category/vehicles-in-use/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'Passenger cars, commercial vehicles, all vehicles, motorization rate'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        print(response.text)
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        filename = resource_url.split('/')[-1]  
        resource_name = filename.split('.')[0] 
        create_resource_remote_url(data['name'], resource_url,resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_48(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')','').replace(':',''),
        'notes': 'This OICA statistics web page contains world motor vehicle production statistics, obtained from national trade organizations, OICA members or correspondents.',
        'license_id': 'notspecified',
        'owner_org': org_id,
        'temporal_coverage_start': '1999-01-01',
        'temporal_coverage_end': '2023-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Cooperation with Ward Auto (America)', 'url': 'https://www.wardsauto.com/'},
            {'title': 'Asian Automotive Analysis Fourin (Asia)', 'url': 'https://aaa.fourin.com/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','private-cars','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Vehicle production',
        'data_provider': 'OICA',
        'url': 'https://www.oica.net/production-statistics/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'vehicle production by country/region and type (passenger cars, LDV, heavy trucks, buses & coaches)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        resource_url= ['https://www.oica.net/wp-content/uploads/By-country-region-2023.xlsx',
              'https://www.oica.net/wp-content/uploads/Passenger-Cars-2023.xlsx',
              'https://www.oica.net/wp-content/uploads/Light-Commercial-Vehicles-2023.xlsx',
              'https://www.oica.net/wp-content/uploads/Heavy-Trucks-2023.xlsx',
              'https://www.oica.net/wp-content/uploads/Heavy-Trucks-2023.xlsx']
        for resource in resource_url:
            filename = resource.split('/')[-1]  
            resource_name = filename.split('.')[0] 
            create_resource_remote_url(data['name'], resource, resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
# ACEA
def dataset_49(org_id, dataset_title,resource_url):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')','').replace(':',''),
        'notes': ' ',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ACEA - European Automobile Manufacturers Association', 'url': 'https://www.acea.auto/files/ACEA-report-vehicles-in-use-europe-2022.pdf'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','private-cars','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Vehicle Fleet',
        'data_provider': 'ACEA',
        'url': 'https://www.acea.auto',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'Vehicles in use, distinguished by age and by fuel type, motorization rates'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        filename = resource_url.split('/')[-1]  
        resource_name = filename.split('.')[0]
        create_resource_remote_url(data['name'], resource_url, resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_50(org_id, dataset_title,resource_url):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')','').replace(':',''),
        'notes': ' ',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2006-01-01',
        'temporal_coverage_end': '2024-07-01',
        'geographies': ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ACEA - European Automobile Manufacturers Association', 'url': 'https://www.acea.auto/nav/?content=passenger-car-registrations'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','private-cars','truck','bus'],
        'services': ['passenger'],
        'frequency': 'monthly',
        'indicators': 'Vehicle Registration',
        'data_provider': 'ACEA',
        'url': 'https://www.acea.auto',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'New passenger car registrations distinguished by country and manufacturer'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        filename = resource_url.split('/')[-1]  
        resource_name = filename.split('.')[0]
        create_resource_remote_url(data['name'], resource_url, resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_51(org_id, dataset_title,resource_url):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')','').replace(':',''),
        'notes': ' ',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2005-01-01',
        'temporal_coverage_end': '2024-07-01',
        'geographies': ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ACEA - European Automobile Manufacturers Association', 'url': 'https://www.acea.auto/nav/?content=commercial-vehicle-registrations'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','private-cars','truck','bus'],
        'services': ['passenger'],
        'frequency': 'monthly',
        'indicators': 'Vehicle Registration',
        'data_provider': 'ACEA',
        'url': 'https://www.acea.auto',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'New passenger car registrations distinguished by country and manufacturer'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        filename = resource_url.split('/')[-1]  
        resource_name = filename.split('.')[0]
        create_resource_remote_url(data['name'], resource_url, resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_52(org_id, dataset_title,resource_url):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')','').replace(':',''),
        'notes': ' ',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ACEA - European Automobile Manufacturers Association', 'url': 'https://www.acea.auto/nav/?content=fuel-types-of-new-passenger-cars'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','private-cars','truck','bus'],
        'services': ['passenger'],
        'frequency': 'monthly',
        'indicators': 'Vehicle Registration',
        'data_provider': 'ACEA',
        'url': 'https://www.acea.auto',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'New passenger car registrations by country and fuel type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        filename = resource_url.split('/')[-1]  
        resource_name = filename.split('.')[0]
        create_resource_remote_url(data['name'], resource_url, resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_53(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')','').replace(':',''),
        'notes': ' ',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2020-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ACEA - European Automobile Manufacturers Association', 'url': 'https://www.acea.auto/nav/?content=fuel-types-of-new-commercial-vehicles'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','private-cars','truck','bus'],
        'services': ['passenger'],
        'frequency': 'annually',
        'indicators': 'Vehicle Registration',
        'data_provider': 'ACEA',
        'url': 'https://www.acea.auto',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'New commercial vehicle registrations distinguished by country and fuel type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        resource_url= ['https://www.acea.auto/files/ACEA_buses_by_fuel_type_full-year-2022.pdf',
              'https://www.acea.auto/files/ACEA_Trucks_by_fuel_type_full-year-2022.pdf',
              'https://www.acea.auto/files/ACEA_vans_by_fuel_type_FY2022.pdf']
        for resource in resource_url:
            filename = resource.split('/')[-1]  
            resource_name = filename.split('.')[0] 
            create_resource_remote_url(data['name'], resource, resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_54(org_id, dataset_title,resource_url):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')','').replace(':',''),
        'notes': ' ',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2006-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ACEA - European Automobile Manufacturers Association', 'url': 'https://www.acea.auto/figure/co2-emissions-from-car-production-in-eu/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','private-cars','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Car Production CO2 emissions',
        'data_provider': 'ACEA',
        'url': 'https://www.acea.auto',
        'data_access': 'publicly available',
        'units': ['tonnes/year','tonnes/car'],
        'dimensioning': 'CO2 emissions per year and per vehicle'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        resource_name = resource_url.split('/')[-1]  
        #resource_name = filename.split('.')[0]
        create_resource_remote_url(data['name'], resource_url, resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_55(org_id, dataset_title,resource_url):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')','').replace(':',''),
        'notes': 'ENERGY CONSUMPTION DURING CAR PRODUCTION',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2006-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ACEA - European Automobile Manufacturers Association', 'url': 'https://www.acea.auto/figure/energy-consumption-during-car-production-in-eu/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','private-cars','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Car Production energy consumption',
        'data_provider': 'ACEA',
        'url': 'https://www.acea.auto',
        'data_access': 'publicly available',
        'units': ['MWh/year','MWh/car'],
        'dimensioning': 'Energy consumption per year and per vehicle'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        resource_name = resource_url.split('/')[-1]  
        #resource_name = filename.split('.')[0]
        create_resource_remote_url(data['name'], resource_url, resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_56(org_id, dataset_title,resource_url):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')','').replace(':',''),
        'notes': 'WATER USED IN CAR PRODUCTION',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2006-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ACEA - European Automobile Manufacturers Association', 'url': 'https://www.acea.auto/figure/water-used-in-car-production-in-eu/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','private-cars','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Car Production water consumption',
        'data_provider': 'ACEA',
        'url': 'https://www.acea.auto',
        'data_access': 'publicly available',
        'units': ['m³/year','m³/car'],
        'dimensioning': 'water consumption per year and per vehicle'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        resource_name = resource_url.split('/')[-1]  
        #resource_name = filename.split('.')[0]
        create_resource_remote_url(data['name'], resource_url, resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_57(org_id, dataset_title,resource_url):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')','').replace(':',''),
        'notes': 'WASTE FROM CAR PRODUCTION',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2006-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ACEA - European Automobile Manufacturers Association', 'url': 'https://www.acea.auto/figure/waste-from-car-production-in-eu/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','private-cars','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Car Production water consumption',
        'data_provider': 'ACEA',
        'url': 'https://www.acea.auto',
        'data_access': 'publicly available',
        'units': ['tonnes/year','tonnes/car'],
        'dimensioning': 'waste production per year and per vehicle'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        resource_name = resource_url.split('/')[-1]  
        #resource_name = filename.split('.')[0]
        create_resource_remote_url(data['name'], resource_url, resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
        
# CCG - Climate Compatible Growth
def dataset_58(org_id, dataset_title,resource_url):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')','').replace(':',''),
        'notes': 'Starter kits with transport&energy datasets to simplify decarbonization policies in developing countries',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'geographies': ['afg','asm','sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'UN Desa', 'url': 'https://www.un.org/en/desa'},
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'ADB', 'url': 'https://www.adb.org/'},
            {'title': 'National Statistics Institute', 'url': 'https://climatecompatiblegrowth.com/starter-kits/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger person-kilometer',
        'data_provider': 'Climate Compatible Growth',
        'url': 'https://climatecompatiblegrowth.com/starter-kits/',
        'data_access': 'publicly available',
        'units': ['PKM'],
        'dimensioning': 'by mode (rail, road, aviation, inland waterways)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        print(response.text)
        response.raise_for_status()  # Raises an error for HTTP errors
        
        print('Dataset created successfully:', response.json())
        resource_name = resource_url.split('/')[-1]  
        #resource_name = filename.split('.')[0]
        create_resource_remote_url(data['name'], resource_url, resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_59(org_id, dataset_title,resource_url):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')','').replace(':',''),
        'notes': 'Starter kits with transport&energy datasets to simplify decarbonization policies in developing countries',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'geographies': ['afg','asm','sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'UN Desa', 'url': 'https://www.un.org/en/desa'},
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'ADB', 'url': 'https://www.adb.org/'},
            {'title': 'National Statistics Institute', 'url': 'https://climatecompatiblegrowth.com/starter-kits/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight ton kilometer',
        'data_provider': 'Climate Compatible Growth',
        'url': 'https://climatecompatiblegrowth.com/starter-kits/',
        'data_access': 'publicly available',
        'units': ['TKM'],
        'dimensioning': 'by mode (rail, road, aviation, inland waterways)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        print(response.text)
        response.raise_for_status()  # Raises an error for HTTP errors
        
        print('Dataset created successfully:', response.json())
        resource_name = resource_url.split('/')[-1]  
        #resource_name = filename.split('.')[0]
        create_resource_remote_url(data['name'], resource_url, resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
def dataset_60(org_id, dataset_title,resource_url):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' ', '-').replace(',','').replace('(','').replace(')','').replace(':',''),
        'notes': 'Starter kits with transport&energy datasets to simplify decarbonization policies in developing countries',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'geographies': ['afg','asm','sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'UN Desa', 'url': 'https://www.un.org/en/desa'},
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'ADB', 'url': 'https://www.adb.org/'},
            {'title': 'National Statistics Institute', 'url': 'https://climatecompatiblegrowth.com/starter-kits/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'vehicle fleet',
        'data_provider': 'Climate Compatible Growth',
        'url': 'https://climatecompatiblegrowth.com/starter-kits/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        print(response.text)
        response.raise_for_status()  # Raises an error for HTTP errors
        
        print('Dataset created successfully:', response.json())
        resource_name = resource_url.split('/')[-1]  
        #resource_name = filename.split('.')[0]
        create_resource_remote_url(data['name'], resource_url, resource_name)
    except Exception as e:
        print('Error creating dataset:', str(e)) 
        
# Kapsarc      
def dataset_194(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Vehicle Fuel Economy Data &CO2 emissions - vehicle type, fuel type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1984-01-01',
        'temporal_coverage_end': '2024-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'fuel economy.gov (ORNL)', 'url': 'https://www.fueleconomy.gov'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Vehicle Fuel Economy Data &CO2 emissions',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': 'vehicle type, fuel type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Fuel Economy': 'https://www.fueleconomy.gov/feg/epadata/25data.zip'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='zip'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_195(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Vehicle Fuel Economy Data &CO2 emissions - vehicle type, fuel type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2016-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'EEA', 'url': 'https://www.eea.europa.eu/en'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'CO2 emissions from passenger cars',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['g/km'],
        'dimensioning': 'by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Monitoring of co2 emissions from passenger cars data 2016': 'https://datasource.kapsarc.org/explore/dataset/monitoring-of-co2-emissions-from-passenger-cars-data-2016/information/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_196(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Number of vehicles in use - vehicle type, fuel type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2005-01-01',
        'temporal_coverage_end': '2015-01-01',
        'geographies': ['bhr','kwt','omn','qat','sau','are','ind'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'OICA', 'url': 'https://www.oica.net/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Number of vehicles in use',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by country, by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Number of vehicles in use': 'https://datasource.kapsarc.org/explore/dataset/economically-active-population-15-years-and-above-by-nationality-gender-and-econ/information/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_197(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Vehicles registerd on the road - by class of vehicle',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2011-01-01',
        'temporal_coverage_end': '2013-01-01',
        'geographies': ['are'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Dubai Statistics Center', 'url': 'https://www.dsc.gov.ae/en-us/Pages/default.aspx'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Vehicles registerd on the road',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by class of vehicle'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Vehicles registerd on the road': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_198(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Road Network - by class of vehicle',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2017-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'General Authority for Statistics', 'url': 'https://www.stats.gov.sa/en'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Road Network',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['KM'],
        'dimensioning': 'length of roads inside cities by type of road; Length of dirt roads paved'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Road Network': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_199(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Distance between main cities',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2008-01-01',
        'temporal_coverage_end': '2013-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'General Authority for Statistics', 'url': 'https://www.stats.gov.sa/en'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Distance between main cities',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['KM'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Distance between main cities': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_200(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'New passenger car registrations - by fuel type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1993-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'UNECE', 'url': 'https://unece.org/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'New passenger car registrations',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by fuel type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'New passenger car registrations': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_201(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'New road vehicle registrations - by vehicle category; by fuel type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1993-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'UNECE', 'url': 'https://unece.org/'},
            {'title': 'National Center for Statistics and information', 'url': 'https://www.ncsi.gov.om/Pages/AllIndicators.aspx'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'New road vehicle registrations',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by vehicle category; by fuel type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'New road vehicle registrations': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_202(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Road vehicle fleet - by vehicle category; by fuel type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1993-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'UNECE', 'url': 'https://unece.org/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Road vehicle fleet',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by vehicle category; by fuel type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Road vehicle fleet': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_203(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passenger vehicle fleet - by vehicle category',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1993-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'UNECE', 'url': 'https://unece.org/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger vehicle fleet',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by vehicle category'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Passenger vehicle fleet': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_204(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Share of road transport - by vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1990-01-01',
        'temporal_coverage_end': '2015-01-01',
        'geographies': ['ind'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Ministry of Road Transport and Highways', 'url': 'https://morth.nic.in/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Share of road transport',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Share of road transport': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_205(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Lenght of roads inside cities - by type of road',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2007-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Ministry of Municipal and Rural Affairs', 'url': 'https://momah.gov.sa/en'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Lenght of roads inside cities',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['KM'],
        'dimensioning': 'by type of road'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Lenght of roads inside cities': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_206(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Registered motor vehicles - by type of vehicles',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1951-01-01',
        'temporal_coverage_end': '2017-01-01',
        'geographies': ['ind'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Ministry of Road Transport and Highways', 'url': 'https://morth.nic.in/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Registered motor vehicles',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by type of vehicles'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Registered motor vehicles': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_207(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Total road length - by category of roads',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1951-01-01',
        'temporal_coverage_end': '2017-01-01',
        'geographies': ['ind'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Open Government Data Platform', 'url': 'https://www.data.gov.in/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Total road length',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['KM','%'],
        'dimensioning': 'by category of roads'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Total road length': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_208(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Vehicle fleet - passenger & freight vehicles',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2017-01-01',
        'temporal_coverage_end': '2017-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'KAPSARC', 'url': 'https://datasource.kapsarc.org/pages/home/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Vehicle fleet',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'passenger & freight vehicles'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Vehicle fleet': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_209(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Registered vehicles - in use; new; cancelled from records',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2004-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['bhr'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Bahrain Open Data Portal', 'url': 'https://www.data.gov.bh/pages/homepage/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Registered vehicles',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'in use; new; cancelled from records'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Registered vehicles': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_210(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Length of paved road - by type of road',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2005-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['bhr'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Bahrain Open Data Portal', 'url': 'https://www.data.gov.bh/pages/homepage/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','taxis','private-cars'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Length of paved road',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['KM'],
        'dimensioning': 'by type of road'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Length of paved road': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_211(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passenger transport activity',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1999-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'General Authority for Statistics', 'url': 'https://www.stats.gov.sa/en'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger transport activity',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['PKM'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Passenger transport activity': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_212(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight transport activity',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1999-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'General Authority for Statistics', 'url': 'https://www.stats.gov.sa/en'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight transport activity',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['TKM'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Freight transport activity': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_213(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight transport activity',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2005-01-01',
        'temporal_coverage_end': '2016-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Eurostat', 'url': 'https://ec.europa.eu/eurostat'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight transport activity',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['TKM'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Freight transport activity': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_214(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passenger transport activity',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2004-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Eurostat', 'url': 'https://ec.europa.eu/eurostat'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger transport activity',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['PKM'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Passenger transport activity': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_215(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Rolling Stock - by type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2008-01-01',
        'temporal_coverage_end': '2013-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'General Authority for Statistics', 'url': 'https://www.stats.gov.sa/en'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Rolling Stock',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Rolling Stock': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_216(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passenger transport activity - passengers carried among railway stations',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2004-01-01',
        'temporal_coverage_end': '2008-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'General Authority for Statistics', 'url': 'https://www.stats.gov.sa/en'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger transport activity',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'passengers carried among railway stations'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Passenger transport activity': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_217(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Distance between railway stations - by age of line',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2008-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'General Authority for Statistics', 'url': 'https://www.stats.gov.sa/en'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Distance between railway stations',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['km'],
        'dimensioning': 'by age of line'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Distance between railway stations': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_218(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Number of locomotives and cars - by type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2008-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'KAPSARC', 'url': 'https://datasource.kapsarc.org/pages/home/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Number of locomotives and cars',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Number of locomotives and cars': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_219(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passenger & Cargo Traffic - by airport',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2008-01-01',
        'temporal_coverage_end': '2016-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'General Authority for Statistics', 'url': 'https://www.stats.gov.sa/en'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Passenger & Cargo Traffic',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#','kg'],
        'dimensioning': 'by airport'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Passenger & Cargo Traffic': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_220(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passenger activity',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2008-01-01',
        'temporal_coverage_end': '2013-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'General Authority for Statistics', 'url': 'https://www.stats.gov.sa/en'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger activity',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['passenger seat KM'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Passenger activity': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_221(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight activity',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2008-01-01',
        'temporal_coverage_end': '2012-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'General Authority for Statistics', 'url': 'https://www.stats.gov.sa/en'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight activity',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['TKM'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Freight activity': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_222(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Air traffic - freight, # flights, # passengers, mail',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'General Authority of Civil Aviation', 'url': 'https://gaca.gov.sa/web/en-gb/page/home'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Air traffic',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'freight, # flights, # passengers, mail'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Air traffic': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_223(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Number of airplanes - by airline',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'KAPSARC', 'url': 'https://datasource.kapsarc.org/pages/home/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Number of airplanes',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by airline'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Number of airplanes': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_224(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Cargo loaded/unloaded - by type of cargo, import/export',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1999-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'General Authority for Statistics', 'url': 'https://www.stats.gov.sa/en'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Cargo loaded/unloaded',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'by type of cargo, import/export'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Cargo loaded/unloaded': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_225(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Volume of seaports exports - by type of goods',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2005-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Saudi Central Bank (SAMA)', 'url': 'https://www.sama.gov.sa/en-us/pages/default.aspx'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Volume of seaports exports',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'by type of goods'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Volume of seaports exports': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_226(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Merchant fleet - by type of ship',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2011-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'UNCTD', 'url': 'https://unctad.org/'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Merchant fleet',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by type of ship'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Merchant fleet': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_227(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight transport activity - by type of goods',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2002-01-01',
        'temporal_coverage_end': '2015-01-01',
        'geographies': ['ind'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Ministry of Statistics and Programme Implementation ', 'url': 'https://www.mospi.gov.in/'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight transport activity',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'by type of goods'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Freight transport activity': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_228(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight transport activity - Tankers of Oil (products) by port',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2008-01-01',
        'temporal_coverage_end': '2017-01-01',
        'geographies': ['sau'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'General Authority for Statistics', 'url': 'https://www.stats.gov.sa/en'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight transport activity',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['barrels'],
        'dimensioning': 'Tankers of Oil (products) by port'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Freight transport activity': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_229(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Modal split of freight transport - By transport mode, by country',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2005-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Eurostat', 'url': 'https://ec.europa.eu/eurostat'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Modal split of freight transport',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'By transport mode, by country'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Modal split of freight transport': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_230(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passenger transport - By transport mode, by country',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'OECD/ITF', 'url': 'https://www.itf-oecd.org/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger transport',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'By transport mode, by country'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Passenger transport': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_231(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passenger, Freight and container transport',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1998-01-01',
        'temporal_coverage_end': '2017-01-01',
        'geographies': ['ind','chn'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'OECD', 'url': 'https://www.oecd.org/en.html'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Passenger, Freight and container transport',
        'data_provider': 'kapsarc',
        'url': 'https://datasource.kapsarc.org/pages/home/',
        'data_access': 'publicly available',
        'units': ['TKM','PKM','TEU'],
        'dimensioning': 'By transport mode, by country'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Passenger, Freight and container transport': 'https://datasource.kapsarc.org/pages/home/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
#ORNL
def dataset_232(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Petroleum production and consumption - by sector, by state',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1950-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['usa','worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'US Department of Energy', 'url': 'https://www.energy.gov/'},
            {'title': 'EIA', 'url': 'https://www.eia.gov/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Petroleum production and consumption',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['million barrels/day','%'],
        'dimensioning': 'by sector, by state'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Petroleum production and consumption': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table1_12_06012022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_233(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Transportation petroleum consumption - by mode',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'DOT', 'url': 'https://www.transportation.gov/'},
            {'title': ', FHWA', 'url': 'https://highways.dot.gov/'},
            {'title': 'Highway Statistics', 'url': 'https://www.fhwa.dot.gov/policyinformation/statistics.cfm'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Transportation petroleum consumption',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['thousand barrels/day'],
        'dimensioning': 'by mode'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Transportation petroleum consumption': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table1_15_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_234(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Energy consumption - by source, by sector, by state',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1950-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'US Department of Energy', 'url': 'https://www.energy.gov/'},
            {'title': 'EIA', 'url': 'https://www.eia.gov/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Energy consumption',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['Btu'],
        'dimensioning': 'by source, by sector, by state'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Distribution of Energy Consumption by Source and Sector, 1973 and 2021': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table2_03_06012022.xlsx',
            'Distribution of Transportation Energy Consumption by Source, 1950-2021': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table2_04_06012022.xlsx',
            'Transportation Energy Consumption by State, 1960-2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table2_05_06012022.xlsx',
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_235(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Fuel production, import, consumption - by fuel type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1981-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'US Department of Energy', 'url': 'https://www.energy.gov/'},
            {'title': 'EIA', 'url': 'https://www.eia.gov/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Fuel production, import, consumption',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['gallons'],
        'dimensioning': 'by fuel type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            '	Fuel Ethanol and Biodiesel Production, Net Imports, and Consumption, 1981-2021': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table2_06_06012022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_236(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Transport energy/fuel consumption - by mode, by fuel type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1973-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'DOT', 'url': 'https://www.transportation.gov/'},
            {'title': ', FHWA', 'url': 'https://highways.dot.gov/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Transport energy/fuel consumption',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['Btu/gallons'],
        'dimensioning': 'by mode, by fuel type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Domestic Consumption of Transportation Energy by Mode and Fuel Type, 2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Figure2_06_01312022.xlsx',
            'Transportation Energy Use by Mode, 2018–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table2_08_01312022.xlsx',
            'Highway Transportation Energy Consumption by Mode, 1970-2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table2_09_01312022.xlsx',
            'Nonhighway Transportation Energy Consumption by Mode, 1970–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table2_10_01312022.xlsx',
            'Off-Highway Transportation-Related Fuel Consumption, 2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table2_11_01312022.xlsx',
            'Highway Usage of Gasoline and Diesel, 1973-2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table2_12_06012022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_237(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passenger travel activity - by mode, # vehicles, vehicle miles, passenger miles, load factor, energy intensity, energy use',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2019-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'DOT', 'url': 'https://www.transportation.gov/'},
            {'title': ', FHWA', 'url': 'https://highways.dot.gov/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Passenger travel activity',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['various'],
        'dimensioning': 'by mode, # vehicles, vehicle miles, passenger miles, load factor, energy intensity, energy use'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Passenger Travel and Energy Use, 2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table2_13_06012022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_238(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Energy intensity - by mode, passenger & freight transport',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'DOT', 'url': 'https://www.transportation.gov/'},
            {'title': ', FHWA', 'url': 'https://highways.dot.gov/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Energy intensity',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['Btu/vehicle mile','Btu/passenger mile'],
        'dimensioning': 'by mode, passenger & freight transport'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Energy Intensities of Highway Passenger Modes, 1970–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table2_14_01312022.xlsx',
            'Energy Intensities of Nonhighway Passenger Modes, 1970–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table2_15_01312022.xlsx',
            'Energy Intensities of Freight Modes, 1970–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table2_16_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_239(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Carbon content - by fuel type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Argonne National Laboratory', 'url': 'https://www.anl.gov/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Carbon content',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['grams/gallon'],
        'dimensioning': 'by fuel type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Carbon Content of Transportation Fuels': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table12_12_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_240(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'CO2 emissions - by transportation mode',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1990-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Argonne National Laboratory', 'url': 'https://www.epa.gov/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'CO2 emissions',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['metric tonnes of CO2 equivalent'],
        'dimensioning': 'by transportation mode'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'U.S. Carbon Emissions from Fossil Fuel Combustion in the Transportation End-Use Sector, 1990-2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table12_07_01312022.xlsx',
            'Transportation Carbon Dioxide Emissions by Mode, 1990–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table12_08_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_241(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Carbon coefficients - by energy source, by fuel type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1990-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'EIA', 'url': 'https://www.eia.gov/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Carbon coefficients',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['metric tonnes carbon/Btu'],
        'dimensioning': 'by energy source, by fuel type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Carbon coefficients - B16': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/TEDB_40_Spreadsheets_06012022.zip'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='zip'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_242(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight transport activity - by transport mode, by distance band, by state, by flow direction',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1993-01-01',
        'temporal_coverage_end': '2017-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'US Department of transportation', 'url': 'https://www.transportation.gov/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight transport activity',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['tonnes','tonne miles'],
        'dimensioning': 'by transport mode, by distance band, by state, by flow direction'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Tons of Freight in the United States: Comparison of the 1993, 1997, 2002, 2007, 2012 and 2017 Commodity Flow Surveys': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table5_16_01312022.xlsx',
            'Ton Miles of Freight in the United States: Comparison of the 1993, 1997, 2002, 2007, 2012 and 2017 Commodity Flow Surveys': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table5_17_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_243(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Average mile per freight trip - by transport mode',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1993-01-01',
        'temporal_coverage_end': '2017-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'US Department of transportation', 'url': 'https://www.transportation.gov/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Average mile per freight trip',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['miles'],
        'dimensioning': 'by transport mode'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Average Miles per Shipment in the United States: Comparison of the 1993, 1997, 2002, 2007, 2012 and 2017 Commodity Flow Surveys': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table5_18_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_244(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Average trip length - by means of transport, by age of vehicle',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1993-01-01',
        'temporal_coverage_end': '2017-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'US Department of transportation', 'url': 'https://www.transportation.gov/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Average trip length',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['miles & minutes'],
        'dimensioning': 'by means of transport, by age of vehicle'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Household Vehicle Trips, 1990, 1995 NPTS and 2001, 2009 and 2017 NHTS': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table9_12_01312022.xlsx',
            'Daily Vehicle Miles of Travel (per Vehicle) by Number of Vehicles in the Household, 2001, 2009 and 2017 NHTS': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table9_13_01312022.xlsx',
            'Daily and Annual Vehicle Miles of Travel and Average Age for Each Vehicle in a Household, 2017 NHTS': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table9_14_01312022.xlsx',
            'Average Length and Duration of Trips To and From Work by Mode, 2017 NHTS': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table9_17_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_245(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Emission of air pollutants - by type of air pollutant, by fuel type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'US Environmental protection agency', 'url': 'https://www.epa.gov/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Emission of air pollutants',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['million short tonnes'],
        'dimensioning': 'by type of air pollutant, by fuel type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Total National Emissions of Criteria Air Pollutants by Sector, 2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table13_01_01312022.xlsx',
            'Total National Emissions of Carbon Monoxide, 1970–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table13_02_01312022.xlsx',
            'Emissions of Carbon Monoxide from Highway Vehicles, 1970-2017': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table13_03_01312022.xlsx',
            'Total National Emissions of Nitrogen Oxides, 1970–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table13_04_01312022.xlsx',
            'Emissions of Nitrogen Oxides from Highway Vehicles, 1970-2017': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table13_05_01312022.xlsx',
            'Total National Emissions of Volatile Organic Compounds, 1970–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table13_06_01312022.xlsx',
            'Emissions of Volatile Organic Compounds from Highway Vehicles, 1970-2017': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table13_07_01312022.xlsx',
            'Total National Emissions of Particulate Matter (PM-10), 1970–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table13_08_01312022.xlsx',
            'Emissions of Particulate Matter (PM-10) from Highway Vehicles, 1970-2017': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table13_09_01312022.xlsx',
            'otal National Emissions of Particulate Matter (PM-2.5), 1990–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table13_10_01312022.xlsx',
            'Emissions of Particulate Matter (PM-2.5) from Highway Vehicles, 1990-2017': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table13_11_01312022.xlsx',
            'Total National Emissions of Sulfur Dioxide, 1970–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table13_12_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_246(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Vehicle Fleet (also intermodal) - registrations & in use by vehicle type, by age, average vehicle age, government vehicles',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1960-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa','worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'wardsauto FHWA', 'url': 'https://www.wardsauto.com/'},
            {'title': 'IHS', 'url': 'https://www.usa.gov/agencies/indian-health-service'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Vehicle Fleet (also intermodal)',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'registrations & in use by vehicle type, by age, average vehicle age, government vehicles'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Car Registrations for Selected Countries, 1960–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table3_02_01312022.xlsx',
            'Truck and Bus Registrations for Selected Countries, 1960–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table3_03_01312022.xlsx',
            'U.S. Cars and Trucks in Use, 1970–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table3_04_01312022.xlsx',
            'Motor Vehicle Registrations by State and Vehicle Type, 2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table3_05_01312022.xlsx',
            'New Retail Vehicle Sales, 1970-2021': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table3_06_06012022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_247(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Modal split - share of highway vehicle miles by vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'US Department of Energy', 'url': 'https://www.energy.gov/'},
            {'title': 'FHWA', 'url': 'https://highways.dot.gov/'},
            {'title': 'Highway Statistics', 'url': 'https://www.fhwa.dot.gov/policyinformation/statistics.cfm'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Modal split',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['vehicle miles'],
        'dimensioning': 'share of highway vehicle miles by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Shares of Highway Vehicle-Miles Traveled by Vehicle Type, 1970–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table3_09_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_248(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Travel activity (also intermodal) - by type of road, by state, by vehicle type, government vehicles',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2020-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'US Department of Energy', 'url': 'https://www.energy.gov/'},
            {'title': 'FHWA', 'url': 'https://highways.dot.gov/'},
            {'title': 'Highway Statistics', 'url': 'https://www.fhwa.dot.gov/policyinformation/statistics.cfm'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Travel activity (also intermodal)',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['vehicle miles'],
        'dimensioning': 'by type of road, by state, by vehicle type, government vehicles'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Vehicle Miles of Travel by State, 2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table3_10_06012022.xlsx',
            'Annual Mileage for Cars and Light Trucks by Vehicle Age': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table3_14_01312022.xlsx',
            'Summary Statistics for Cars, 1970–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table4_01_06012022.xlsx',
            'Summary Statistics for Two-Axle, Four-Tire Trucks, 1970–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table4_02_06012022.xlsx',
            'Summary Statistics for Light Vehicles, 1970–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table4_03_06012022.xlsx',
            'Summary Statistics on Class 1, Class 2a, and Class 2b Light Trucks': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_04_01312022.xlsx',
            'Examples of Class 2b Vehicle Models, 2017': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_05_01312022.xlsx',
            'Summary Statistics for Class 3-8 Single-Unit Trucks, 1970–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table5_01_06012022.xlsx',
            'Summary Statistics for Class 7-8 Combination Trucks, 1970-2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table5_02_06012022.xlsx',
            'Summary Statistics on Transit Buses and Trolleybuses, 1994–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table7_01_09312022.xlsx',
            'Summary Statistics on Demand Response Vehicles, 1994–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table7_02_09312022.xlsx',
            'Summary Statistics for Commuter Rail Operations, 1984–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table7_03_09312022.xlsx',
            'Summary Statistics for Rail Transit Operations, 1970–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table7_04_01312022.xlsx',
            'Average Annual Vehicle-Miles of Travel for Commercial Fleet Vehicles, 2018 and 2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table8_03_01312022.xlsx',
            
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_249(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Fuel use & fuel economy (also intermodal) - by vehicle type, by speed, by fuel type, by age of vehicle, by terrain',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'US Department of Transportation', 'url': 'https://www.transportation.gov/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Fuel use & fuel economy (also intermodal)',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['gallons & miles per gallon'],
        'dimensioning': 'by vehicle type, by speed, by fuel type, by age of vehicle, by terrain'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Summary Statistics for Cars, 1970–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table4_01_06012022.xlsx',
            'Summary Statistics for Two-Axle, Four-Tire Trucks, 1970–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table4_02_06012022.xlsx',
            'Summary Statistics for Light Vehicles, 1970–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table4_03_06012022.xlsx',
            'Summary Statistics on Class 1, Class 2a, and Class 2b Light Trucks': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_04_01312022.xlsx',
            'Examples of Class 2b Vehicle Models, 2017': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_05_01312022.xlsx',
            'Summary Statistics for Class 3-8 Single-Unit Trucks, 1970–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table5_01_06012022.xlsx',
            'Summary Statistics for Class 7-8 Combination Trucks, 1970-2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table5_02_06012022.xlsx',
            'Truck Statistics by Gross Vehicle Weight Class, 2002': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table5_05_01312022.xlsx',
            'Production, Production Shares, and Production-Weighted Fuel Economies of New Domestic and Import Cars, Model Years 1975-2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_09_01312022.xlsx',
            'Definition of Car Sport Utility Vehicles in Model Year 2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_10_01312022.xlsx',
            'Production, Production Shares, and Production-Weighted Fuel Economies of New Domestic and Import Light Trucks, Model Years 1975-2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_11_01312022.xlsx',
            'Production and Production-Weighted Fuel Economies of New Domestic and Import Cars, Light Trucks and Light Vehicles, Model Years 1975-2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_12_01312022.xlsx',
            'Fuel Economy by Speed, Autonomie Model Results, Model Year 2016': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_33_01312022.xlsx',
            'Fuel Economy by Speed, 1973, 1984, 1997 and 2012 Studies': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_34_01312022.xlsx',
            'Truck Harmonic Mean Fuel Economy by Size Class, 1992, 1997 and 2002': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table5_06_01312022.xlsx',
            'Effect of Terrain on Class 8 Truck Fuel Economy': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table5_11_01312022.xlsx',
            'Fuel Economy for Class 8 Trucks as a Function of Speed and Tractor-Trailer Tire Combination': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table5_12_01312022.xlsx',
            'Summary Statistics on Transit Buses and Trolleybuses, 1994–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table7_01_09312022.xlsx',
            'Summary Statistics on Demand Response Vehicles, 1994–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table7_02_09312022.xlsx',
            'Summary Statistics for Commuter Rail Operations, 1984–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table7_03_09312022.xlsx',
            'Summary Statistics for Rail Transit Operations, 1970–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table7_04_01312022.xlsx',
            'Fuel Consumed by Federal Government Fleets, FY 2000-2021': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table8_06_06012022.xlsx',
            'A1-A7': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/TEDB_40_Spreadsheets_06012022.zip'
            
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_250(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Fuel economy comparison - by driving cycle, by operational area',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2021-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title':'US environmental protection agency', 'url':'https://www.epa.gov/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Fuel economy comparison',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['miles per gallon'],
        'dimensioning': 'by driving cycle, by operational area'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Fuel Economy Comparison Among CAFE, Window Sticker, and Real-World Estimates for the 2020 Toyota Prius Eco': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_08_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_251(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Production shares - by vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1975-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title':'US environmental protection agency', 'url':'https://www.epa.gov/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Production shares',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Light Vehicle Production Shares, Model Years 1975–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_13_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_252(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Technology penetration - by technology, by vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1996-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title':'US environmental protection agency', 'url':'https://www.epa.gov/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Technology penetration',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'by technology, by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Car Technology Penetration, 1996–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_14_01312022.xlsx',
            'Light Truck Technology Penetration, 2002-2020':'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_15_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_253(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Average material consumption - by type of material',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1995-01-01',
        'temporal_coverage_end': '2017-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'wardsauto FHWA', 'url': 'https://www.wardsauto.com/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Average material consumption',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['%','pounds'],
        'dimensioning': 'by type of material'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Average Material Consumption for a Domestic Light Vehicle, Model Years 1995, 2000, and 2017': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_20_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_254(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Refueling stations - by fuel type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1972-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Lundberg survey', 'url': 'https://www.lundbergsurvey.com/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Refueling stations',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by fuel type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Conventional Refueling Stations, 1972-2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_24_01312022.xlsx',
            'Number of Alternative Refuel Stations, 1992-2021': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table6_13_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_255(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Emission standards - by vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2017-01-01',
        'temporal_coverage_end': '2026-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Federal register', 'url': 'https://www.federalregister.gov/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Emission standards',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['miles per gallon & grams per mile'],
        'dimensioning': 'by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Fuel Economy and Carbon Dioxide Emissions Standards, MY 2017-2026': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_25_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_256(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Driving cycle attributes - by test procedure',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2022-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Fuel economy guide website', 'url': 'https://www.fueleconomy.gov/feg/printGuides.shtml'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Driving cycle attributes',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': 'by test procedure'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Driving Cycle Attributes': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_35_01312022.xlsx',
            'Comparison of U.S., European, and Japanese Driving Cycles Attributes': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_36_01312022.xlsx',
            'Example of Differing Results Using the U.S., European, and Japanese Driving Cycles': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table4_37_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_257(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Diesel share - by truck size',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1995-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'wardsauto FHWA', 'url': 'https://www.wardsauto.com/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Diesel share',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'by truck size'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Diesel Share of Medium and Heavy Truck Sales by Gross Vehicle Weight, 1995–2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table5_04_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_258(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Carshare members - by world regions',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2006-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Transportation sustainability research center', 'url': 'https://tsrc.berkeley.edu/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Carshare members',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by world regions'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Carshare Members and Vehicles by World Region, 2006–2018': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table7_08_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_259(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Car operating costs - insurance, tax, etc',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1975-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'wardsauto FHWA', 'url': 'https://www.wardsauto.com/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Car operating costs',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['dollar'],
        'dimensioning': 'insurance, tax, etc'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Fixed Car Operating Costs per Year, 1975-2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table11_16_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_260(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Fuel costs - by fuel type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1990-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['usa','worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IEA', 'url': 'https://www.iea.org/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Fuel costs',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['dollar'],
        'dimensioning': 'by fuel type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Gasoline Prices for Selected Countries, 1990-2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table11_03_01312022.xlsx',
            'Diesel Fuel Prices for Selected Countries, 1990-2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table11_04_01312022.xlsx',
            'Retail Prices for Motor Fuel, 1978-2021': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/Table11_06_06012022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_261(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Production weighted Carbon footprint - by vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1975-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title':'US environmental protection agency', 'url':'https://www.epa.gov/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Production weighted Carbon footprint',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['tonnes of CO2'],
        'dimensioning': 'by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Production-Weighted Annual Carbon Footprint of New Domestic and Import Cars, Model Years 1975-2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table12_09_01312022.xlsx',
            'Production-Weighted Annual Carbon Footprint of New Domestic and Import Light Trucks, Model Years 1975-2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table12_10_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_262(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Load factor - by vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title':'NPTS', 'url':'https://npts.net/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Load factor',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'A19': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/TEDB_40_Spreadsheets_06012022.zip'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='zip'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_263(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Fleet - by type of vehicle',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1971-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title':'Association of american railroads', 'url':'https://www.aar.org/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Fleet',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by type of vehicle'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Summary Statistics for the National Railroad Passenger Corporation (Amtrak), 1971-2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table10_10_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_264(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Average trip length',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1971-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title':'Association of american railroads', 'url':'https://www.aar.org/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Average trip length ',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['miles'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Summary Statistics for the National Railroad Passenger Corporation (Amtrak), 1971-2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table10_10_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_265(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Traffic activity',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1971-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title':'Association of american railroads', 'url':'https://www.aar.org/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Traffic activity',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['car miles & train miles & tonne miles'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Summary Statistics for the National Railroad Passenger Corporation (Amtrak), 1971-2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table10_10_01312022.xlsx',
            'Summary Statistics for Class I Freight Railroads, 1970-2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table10_08_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_266(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Energy intensity',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1971-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title':'Association of american railroads', 'url':'https://www.aar.org/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Energy intensity',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['Btu/passenger mile'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Summary Statistics for the National Railroad Passenger Corporation (Amtrak), 1971-2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table10_10_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_267(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Fuel use - freight, passenger, fuel type, operation type, vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1971-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title':'Association of american railroads', 'url':'https://www.aar.org/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Fuel use',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['gallons','kWh'],
        'dimensioning': 'freight, passenger, fuel type, operation type, vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'A13-A16': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/TEDB_40_Spreadsheets_06012022.zip'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='zip'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_268(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Fleet - by type of vehicle',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title':'US environmental protection agency', 'url':'https://www.epa.gov/'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping','international-maritime'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Fleet',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by type of vehicle'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Summary Statistics for Domestic Waterborne Commerce, 1970–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table10_05_01312022.xlsx',
            'Recreational Boat Energy Use, 1970-2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table10_06_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_269(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Energy use - by fuel type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title':'US environmental protection agency', 'url':'https://www.epa.gov/'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping','international-maritime'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Energy use',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['Btu'],
        'dimensioning': 'by fuel type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Summary Statistics for Domestic Waterborne Commerce, 1970–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table10_05_01312022.xlsx',
            'Recreational Boat Energy Use, 1970-2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table10_06_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_270(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight activity - foreign, domestic',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title':'US department of army', 'url':'https://www.army.mil/'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping','international-maritime'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight activity',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['tonne miles & tonnes shipped'],
        'dimensioning': 'foreign, domestic'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Summary Statistics for Domestic Waterborne Commerce, 1970–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table10_05_01312022.xlsx',
            'Tonnage Statistics for Domestic and International Waterborne Commerce, 1970-2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table10_04_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_271(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Fuel use - by fuel type, by vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title':'US environmental protection agency', 'url':'https://www.epa.gov/'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping','international-maritime'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Fuel use',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['gallons'],
        'dimensioning': 'by fuel type, by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'A11, A10': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/TEDB_40_Spreadsheets_06012022.zip'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='zip'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_272(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Fleet - number of aircrafts',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'US Department of Transportation', 'url': 'https://www.transportation.gov/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Fleet',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'number of aircrafts'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Summary Statistics for General Aviation, 1970–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table10_03_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_273(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Travel activity - hours flown, aircraft miles, passenger miles, seat miles, load factor, tonne miles',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'US Department of Transportation', 'url': 'https://www.transportation.gov/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Travel activity',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['various'],
        'dimensioning': 'hours flown, aircraft miles, passenger miles, seat miles, load factor, tonne miles'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Summary Statistics for General Aviation, 1970–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table10_03_01312022.xlsx',
            'Summary Statistics for U.S. Domestic and International Certificated Route Air Carriers (Combined Totals), 1970-2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table10_02_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_274(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Energy use',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'US Department of Transportation', 'url': 'https://www.transportation.gov/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Energy use',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['btu'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Summary Statistics for General Aviation, 1970–2019': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table10_03_01312022.xlsx',
            'Summary Statistics for U.S. Domestic and International Certificated Route Air Carriers (Combined Totals), 1970-2020': 'https://tedb.ornl.gov/wp-content/uploads/2022/03/Table10_02_01312022.xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_275(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Fuel use - domestic, internation, jet, aviation',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2019-01-01',
        'geographies': ['usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'US Department of Transportation', 'url': 'https://www.transportation.gov/'},
            {'title':'FAA', 'url': 'https://www.faa.gov/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Fuel use',
        'data_provider': 'Oak Ridge National Laboratory',
        'url': 'https://tedb.ornl.gov/data/',
        'data_access': 'publicly available',
        'units': ['gallons'],
        'dimensioning': 'domestic, internation, jet, aviation'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'A08, A09': 'https://tedb.ornl.gov/wp-content/uploads/2022/06/TEDB_40_Spreadsheets_06012022.zip'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='zip'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_278(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Infrastructre length - by type of road',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1993-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Common Questionnaire from Statistics Offices', 'url': 'https://unece.org/statistics'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Infrastructre length',
        'data_provider': 'UNECE',
        'url': 'https://unece.org/',
        'data_access': 'publicly available',
        'units': ['Km'],
        'dimensioning': 'by type of road'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructre length': 'https://w3.unece.org/PXWeb2015/pxweb/en/STAT/STAT__40-TRTRANS__11-TRINFRA/ZZZ_en_TRInfraRoad_r.px/table/tableViewLayout1/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_279(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Vehicle fleet and new registrations - by type of vehicle, age, weight, fueltype',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1993-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Common Questionnaire from Statistics Offices', 'url': 'https://unece.org/statistics'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Vehicle fleet and new registrations',
        'data_provider': 'UNECE',
        'url': 'https://unece.org/',
        'data_access': 'publicly available',
        'units': ['Number'],
        'dimensioning': 'by type of vehicle, age, weight, fueltype'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Vehicle fleet and new registrations': 'https://w3.unece.org/PXWeb2015/pxweb/en/STAT/STAT__40-TRTRANS__03-TRRoadFleet/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_280(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Traffic motor vehicle movements - by vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1993-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Common Questionnaire from Statistics Offices', 'url': 'https://unece.org/statistics'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Traffic motor vehicle movements',
        'data_provider': 'UNECE',
        'url': 'https://unece.org/',
        'data_access': 'publicly available',
        'units': ['Vkm'],
        'dimensioning': 'by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Traffic motor vehicle movements': 'https://w3.unece.org/PXWeb2015/pxweb/en/STAT/STAT__40-TRTRANS__02-TRROAD/01_en_TRRoadVehKm_r.px/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_281(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight transport - by location',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1980-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Common Questionnaire from Statistics Offices', 'url': 'https://unece.org/statistics'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight transport',
        'data_provider': 'UNECE',
        'url': 'https://unece.org/',
        'data_access': 'publicly available',
        'units': ['T','Tkm'],
        'dimensioning': 'by location'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Freight transport': 'https://w3.unece.org/PXWeb2015/pxweb/en/STAT/STAT__40-TRTRANS__02-TRROAD/03_en_TRRoadGoodsTkm_r.px/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_282(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passenger transport  - by vehicle type (passenger car, bus, motorbike)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1980-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Common Questionnaire from Statistics Offices', 'url': 'https://unece.org/statistics'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger transport',
        'data_provider': 'UNECE',
        'url': 'https://unece.org/',
        'data_access': 'publicly available',
        'units': ['Pkm'],
        'dimensioning': 'by vehicle type (passenger car, bus, motorbike)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Passenger transport': 'https://w3.unece.org/PXWeb2015/pxweb/en/STAT/STAT__40-TRTRANS__02-TRROAD/04_en_TRRoadPassgKm_r.px/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_283(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Safety, accidents, fatalities, and injuries  - extensive breakdown',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1993-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Common Questionnaire from Statistics Offices', 'url': 'https://unece.org/statistics'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Safety, accidents, fatalities, and injuries',
        'data_provider': 'UNECE',
        'url': 'https://unece.org/',
        'data_access': 'publicly available',
        'units': ['Number'],
        'dimensioning': 'extensive breakdown'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Safety, accidents, fatalities, and injuries': 'https://w3.unece.org/PXWeb2015/pxweb/en/STAT/STAT__40-TRTRANS__01-TRACCIDENTS/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_284(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Infrastructure length  - by track type, gauge, activity',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1993-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Common Questionnaire from Statistics Offices', 'url': 'https://unece.org/statistics'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Infrastructure length',
        'data_provider': 'UNECE',
        'url': 'https://unece.org/',
        'data_access': 'publicly available',
        'units': ['KM'],
        'dimensioning': 'by track type, gauge, activity'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure length': 'https://w3.unece.org/PXWeb2015/pxweb/en/STAT/STAT__40-TRTRANS__11-TRINFRA/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_285(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Transport equipment - by vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Common Questionnaire from Statistics Offices', 'url': 'https://unece.org/statistics'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Transport equipment',
        'data_provider': 'UNECE',
        'url': 'https://unece.org/',
        'data_access': 'publicly available',
        'units': ['Number','power'],
        'dimensioning': 'by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Transport equipment': 'https://w3.unece.org/PXWeb2015/pxweb/en/STAT/STAT__40-TRTRANS__07-TRRAILVEH/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_286(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Traffic train movements - by equipment and train type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Common Questionnaire from Statistics Offices', 'url': 'https://unece.org/statistics'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Traffic train movements',
        'data_provider': 'UNECE',
        'url': 'https://unece.org/',
        'data_access': 'publicly available',
        'units': ['Train-km'],
        'dimensioning': 'by equipment and train type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Traffic train movements': 'https://w3.unece.org/PXWeb2015/pxweb/en/STAT/STAT__40-TRTRANS__05-TRRAIL/03_en_TRRailMvmt_r.px/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_287(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight transport - by location',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Common Questionnaire from Statistics Offices', 'url': 'https://unece.org/statistics'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight transport',
        'data_provider': 'UNECE',
        'url': 'https://unece.org/',
        'data_access': 'publicly available',
        'units': ['T','Tkm'],
        'dimensioning': 'by location'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Freight transport': 'https://w3.unece.org/PXWeb2015/pxweb/en/STAT/STAT__40-TRTRANS__05-TRRAIL/02_en_TRrailtonneskm_r.px/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_288(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passenger transport - by location',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Common Questionnaire from Statistics Offices', 'url': 'https://unece.org/statistics'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger transport',
        'data_provider': 'UNECE',
        'url': 'https://unece.org/',
        'data_access': 'publicly available',
        'units': ['passengers','PKM'],
        'dimensioning': 'by location'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Passenger transport': 'https://w3.unece.org/PXWeb2015/pxweb/en/STAT/STAT__40-TRTRANS__05-TRRAIL/01_en_TRrailpassengers_r.px/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_289(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Safety, accidents, fatalities, and injuries - by victim',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2006-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Common Questionnaire from Statistics Offices', 'url': 'https://unece.org/statistics'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Safety, accidents, fatalities, and injuries',
        'data_provider': 'UNECE',
        'url': 'https://unece.org/',
        'data_access': 'publicly available',
        'units': ['Number'],
        'dimensioning': 'by victim'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Safety, accidents, fatalities, and injuries': 'https://w3.unece.org/PXWeb2015/pxweb/en/STAT/STAT__40-TRTRANS__06-TRRAILACC/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_290(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Infrastructure navigable river length - by type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1993-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Common Questionnaire from Statistics Offices', 'url': 'https://unece.org/statistics'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['inland-shipping'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Infrastructure navigable river length',
        'data_provider': 'UNECE',
        'url': 'https://unece.org/',
        'data_access': 'publicly available',
        'units': ['KM'],
        'dimensioning': 'by type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure navigable river length': 'https://w3.unece.org/PXWeb2015/pxweb/en/STAT/STAT__40-TRTRANS__11-TRINFRA/ZZZ_en_TRInfrIWW_r.px/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_291(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Vessels - by construction year, capacity',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1990-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Common Questionnaire from Statistics Offices', 'url': 'https://unece.org/statistics'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['inland-shipping'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Vessels',
        'data_provider': 'UNECE',
        'url': 'https://unece.org/',
        'data_access': 'publicly available',
        'units': ['Number','power','tonnes'],
        'dimensioning': 'by construction year, capacity'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Vessels': 'https://w3.unece.org/PXWeb2015/pxweb/en/STAT/STAT__40-TRTRANS__08-TRINLVESS/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_292(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight transport - by location',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1980-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Common Questionnaire from Statistics Offices', 'url': 'https://unece.org/statistics'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['inland-shipping'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight transport',
        'data_provider': 'UNECE',
        'url': 'https://unece.org/',
        'data_access': 'publicly available',
        'units': ['T','Tkm'],
        'dimensioning': 'by location'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Freight transport': 'https://w3.unece.org/PXWeb2015/pxweb/en/STAT/STAT__40-TRTRANS__09-TRInlWater/01_en_TRInlWaterTonKm_r.px/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_293(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passenger transport - by vehicle type (tram, metro, light rail)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2010-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Common Questionnaire from Statistics Offices', 'url': 'https://unece.org/statistics'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['high-speed-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger transport',
        'data_provider': 'UNECE',
        'url': 'https://unece.org/',
        'data_access': 'publicly available',
        'units': ['passengers','PKM'],
        'dimensioning': 'by vehicle type (tram, metro, light rail)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Passenger transport': 'https://unece.org/tram-and-metro-data'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_294(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Number of vehicles registered - vehicle type (only for individual use)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2007-01-01',
        'temporal_coverage_end': '2007-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'OMU 1st edition', 'url': 'https://www.caf.com/es/conocimiento/datos/observatorio-de-movilidad-urbana/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Number of vehicles registered',
        'data_provider': 'CAF',
        'url': 'https://www.caf.com/es/conocimiento/datos/observatorio-de-movilidad-urbana/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'vehicle type (only for individual use)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Number of vehicles registered': 'https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.caf.com%2Fmedia%2F6767%2Fomu_flota_js.xlsx&wdOrigin=BROWSELINK'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_295(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Number of vehicles registered - vehicle type (only for individual use)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2015-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'OMU 2nd edition', 'url': 'https://www.caf.com/es/conocimiento/datos/observatorio-de-movilidad-urbana/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Number of vehicles registered',
        'data_provider': 'CAF',
        'url': 'https://www.caf.com/es/conocimiento/datos/observatorio-de-movilidad-urbana/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'vehicle type (only for individual use)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Number of vehicles registered': 'https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.caf.com%2Fmedia%2F6822%2Fcaf_-_observatorio_de_movilidad_urbana_-_datos_generales_2015.xlsx&wdOrigin=BROWSELINK'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_296(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Number of vehicles per inhabitant - vehicle type (car and motorcycle)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2007-01-01',
        'temporal_coverage_end': '2007-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'OMU 1st edition', 'url': 'https://www.caf.com/es/conocimiento/datos/observatorio-de-movilidad-urbana/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Number of vehicles per inhabitant',
        'data_provider': 'CAF',
        'url': 'https://www.caf.com/es/conocimiento/datos/observatorio-de-movilidad-urbana/',
        'data_access': 'publicly available',
        'units': ['veh/1000inhab'],
        'dimensioning': 'vehicle type (car and motorcycle)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Number of vehicles per inhabitant': 'https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.caf.com%2Fmedia%2F6767%2Fomu_flota_js.xlsx&wdOrigin=BROWSELINK'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_297(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Number of vehicles per inhabitant - vehicle type (car and motorcycle)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2015-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'OMU 2nd edition', 'url': 'https://www.caf.com/es/conocimiento/datos/observatorio-de-movilidad-urbana/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Number of vehicles per inhabitant',
        'data_provider': 'CAF',
        'url': 'https://www.caf.com/es/conocimiento/datos/observatorio-de-movilidad-urbana/',
        'data_access': 'publicly available',
        'units': ['veh/1000inhab'],
        'dimensioning': 'vehicle type (car and motorcycle)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Number of vehicles per inhabitant': 'https://www.google.com/url?q=https://view.officeapps.live.com/op/view.aspx?src%3Dhttps%253A%252F%252Fwww.caf.com%252Fmedia%252F6822%252Fcaf_-_observatorio_de_movilidad_urbana_-_datos_generales_2015.xlsx%26wdOrigin%3DBROWSELINK&sa=D&source=editors&ust=1729165401341252&usg=AOvVaw3E6iffvEWXO8zMMOhNNk-s'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_298(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'vehicle type (taxi, jeep, bus, include urban rails)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2007-01-01',
        'temporal_coverage_end': '2007-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'OMU 1st edition', 'url': 'https://www.caf.com/es/conocimiento/datos/observatorio-de-movilidad-urbana/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','private-cars','taxis','bus','high-speed-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Number of public transit vehicles registered',
        'data_provider': 'CAF',
        'url': 'https://www.caf.com/es/conocimiento/datos/observatorio-de-movilidad-urbana/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'vehicle type (taxi, jeep, bus, include urban rails)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Number of public transit vehicles registered': 'https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.caf.com%2Fmedia%2F6767%2Fomu_flota_js.xlsx&wdOrigin=BROWSELINK'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_299(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Number of trips per person per day (trips/person) - "vehicle type( T individual	T colectivo	A pie/bici)"',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2015-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'OMU 2nd edition', 'url': 'https://www.caf.com/es/conocimiento/datos/observatorio-de-movilidad-urbana/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','private-cars','taxis','bus','high-speed-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Number of trips per person per day (trips/person)',
        'data_provider': 'CAF',
        'url': 'https://www.caf.com/es/conocimiento/datos/observatorio-de-movilidad-urbana/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'vehicle type( T individual	T colectivo	A pie/bici)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Number of trips per person per day': 'https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.caf.com%2Fmedia%2F6822%2Fcaf_-_observatorio_de_movilidad_urbana_-_datos_generales_2015.xlsx&wdOrigin=BROWSELINK'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_300(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Modal Split (distribution of trip per mode) - percetange per mode',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2022-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'OMU 3rd Edition (based on mobility surveys', 'url': 'https://www.caf.com/es/conocimiento/datos/observatorio-de-movilidad-urbana/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars','private-cars','taxis','bus','high-speed-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Modal Split (distribution of trip per mode)',
        'data_provider': 'CAF',
        'url': 'https://www.caf.com/es/conocimiento/datos/observatorio-de-movilidad-urbana/',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'percetange per mode'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Modal Split': 'https://omu-latam.org/indicadores/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_301(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'CO2 emissions - passenger specific; freight specific',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2017-01-01',
        'temporal_coverage_end': '2017-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'UIC', 'url': 'https://uic.org/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['high-speed-rail','heavy-rail','transit-rail'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'CO2 emissions',
        'data_provider': 'UIC',
        'url': 'https://uic.org/',
        'data_access': 'publicly available',
        'units': ['gCO2e/pkm','gCO2e/net','tkm'],
        'dimensioning': 'passenger specific; freight specific'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'CO2e emissions': 'https://uic.org/IMG/pdf/handbook_iea-uic_2017_web3.pdf'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='pdf'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_302(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Total emissions',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2017-01-01',
        'temporal_coverage_end': '2017-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'UIC', 'url': 'https://uic.org/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['high-speed-rail','heavy-rail','transit-rail'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Total emissions',
        'data_provider': 'UIC',
        'url': 'https://uic.org/',
        'data_access': 'publicly available',
        'units': ['millioin tonnes CO2eq'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Total emissions': 'https://uic.org/IMG/pdf/handbook_iea-uic_2017_web3.pdf'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='pdf'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_303(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Energy consumption - passsenger specific; freight specific',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2017-01-01',
        'temporal_coverage_end': '2017-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'UIC', 'url': 'https://uic.org/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['high-speed-rail','heavy-rail','transit-rail'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Energy consumption',
        'data_provider': 'UIC',
        'url': 'https://uic.org/',
        'data_access': 'publicly available',
        'units': ['kWh/pkm','kWh/tkm'],
        'dimensioning': 'passsenger specific; freight specific'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Energy consumption': 'https://uic.org/IMG/pdf/handbook_iea-uic_2017_web3.pdf'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='pdf'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_304(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Air pollutants emissions - PM, NOx',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2017-01-01',
        'temporal_coverage_end': '2017-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'UIC', 'url': 'https://uic.org/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['high-speed-rail','heavy-rail','transit-rail'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Air pollutants emissions',
        'data_provider': 'UIC',
        'url': 'https://uic.org/',
        'data_access': 'publicly available',
        'units': ['thousand tonnes'],
        'dimensioning': 'PM, NOx'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Air pollutants emissions': 'https://uic.org/IMG/pdf/handbook_iea-uic_2017_web3.pdf'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='pdf'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_305(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'transport activity, emissions, air quality, road safety). All major mobility modes (e.g. aviation, bus rapid transit, cycling, rail, road transport, shipping, walking',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2021-01-01',
        'temporal_coverage_end': '2023-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Transport Knowledge Base', 'url': 'https://tcc-gsr.com/3rd-edition-transport-knowledge-base-trakb/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'transport activity',
        'data_provider': 'SLOCAT',
        'url': 'https://slocat.net/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Transport Knowledge Base': 'https://tcc-gsr.com/trakb_version_0-4/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
# SDG
def dataset_306(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Death rate due to road traffic injuries',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2021-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Health Organization (WHO)', 'url': 'https://www.who.int/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Death rate due to road traffic injuries',
        'data_provider': 'UN SDG Indicator Database',
        'url': 'https://unstats.un.org/sdgs/dataportal/database',
        'data_access': 'publicly available',
        'units': ['rate per 100,000 population'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Indicator 3.6.1': 'https://unstats.un.org/sdgs/dataportal/database'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_307(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Death rate due to road traffic injuries',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'International Civil Aviation organisation (ICAO)', 'url': 'https://www.icao.int/Pages/default.aspx'},
            {'title': 'United Nations Conference on Trade and Development (UNCTAD)', 'url': 'https://unctad.org/'},
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight volume',
        'data_provider': 'UN SDG Indicator Database',
        'url': 'https://unstats.un.org/sdgs/dataportal/database',
        'data_access': 'publicly available',
        'units': ['tkm'],
        'dimensioning': 'by mode of transport'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Indicator 9.1.2': 'https://unstats.un.org/sdgs/dataportal/database'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_308(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Death rate due to road traffic injuries',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2022-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'International Civil Aviation organisation (ICAO)', 'url': 'https://www.icao.int/Pages/default.aspx'},
            {'title': 'United Nations Conference on Trade and Development (UNCTAD)', 'url': 'https://unctad.org/'},
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger volume',
        'data_provider': 'UN SDG Indicator Database',
        'url': 'https://unstats.un.org/sdgs/dataportal/database',
        'data_access': 'publicly available',
        'units': ['passenger kilometers'],
        'dimensioning': 'by mode of transport'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Indicator 9.1.2': 'https://unstats.un.org/sdgs/dataportal/database'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_309(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight loaded and uloaded',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2010-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'International Civil Aviation organisation (ICAO)', 'url': 'https://www.icao.int/Pages/default.aspx'},
            {'title': 'United Nations Conference on Trade and Development (UNCTAD)', 'url': 'https://unctad.org/'},
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight loaded and uloaded',
        'data_provider': 'UN SDG Indicator Database',
        'url': 'https://unstats.un.org/sdgs/dataportal/database',
        'data_access': 'publicly available',
        'units': ['metric tons'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Indicator 9.1.2': 'https://unstats.un.org/sdgs/dataportal/database'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_310(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight loaded and uloaded',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2012-01-01',
        'temporal_coverage_end': '2023-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'UN-Habitat', 'url': 'https://unhabitat.org/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Proportion of population that has convenient access to public transport',
        'data_provider': 'UN SDG Indicator Database',
        'url': 'https://unstats.un.org/sdgs/dataportal/database',
        'data_access': 'publicly available',
        'units': ['Percentage'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Indicator 11.2.1': 'https://unstats.un.org/sdgs/dataportal/database'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
# IRF
def dataset_311(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Road Network length - By Road types',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IRF', 'url': 'https://www.irf.global/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Road Network length',
        'data_provider': 'IRF',
        'url': 'https://www.irf.global/',
        'data_access': 'publicly available',
        'units': ['km'],
        'dimensioning': 'By Road types'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Road Network length': 'https://worldroadstatistics.org/get-data/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_312(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Road vehicle mileage - By vehicle types; by road types',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IRF', 'url': 'https://www.irf.global/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Road vehicle mileage',
        'data_provider': 'IRF',
        'url': 'https://www.irf.global/',
        'data_access': 'publicly available',
        'units': ['vkm/year'],
        'dimensioning': 'By vehicle types; by road types'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Road vehicle mileage': 'https://worldroadstatistics.org/get-data/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_313(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight ton-kilometer - Freight Transport by mode',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IRF', 'url': 'https://www.irf.global/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight ton-kilometer',
        'data_provider': 'IRF',
        'url': 'https://www.irf.global/',
        'data_access': 'publicly available',
        'units': ['tkm/year'],
        'dimensioning': 'Freight Transport by mode'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Freight ton-kilometer': 'https://worldroadstatistics.org/get-data/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_314(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passenger Person-kilometer - Passenger transport by mode & by road',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IRF', 'url': 'https://www.irf.global/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger Person-kilometer',
        'data_provider': 'IRF',
        'url': 'https://www.irf.global/',
        'data_access': 'publicly available',
        'units': ['pkm/year'],
        'dimensioning': 'Passenger transport by mode & by road'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Passenger Person-kilometer': 'https://worldroadstatistics.org/get-data/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_315(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Vehicle fleet - by vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IRF', 'url': 'https://www.irf.global/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Vehicle fleet',
        'data_provider': 'IRF',
        'url': 'https://www.irf.global/',
        'data_access': 'publicly available',
        'units': ['number'],
        'dimensioning': 'by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Vehicle fleet': 'https://worldroadstatistics.org/get-data/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_316(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Fuel Prices - Diesel & super gas price',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IRF', 'url': 'https://www.irf.global/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Fuel Prices',
        'data_provider': 'IRF',
        'url': 'https://www.irf.global/',
        'data_access': 'publicly available',
        'units': ['USD/litre'],
        'dimensioning': 'Diesel & super gas price'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Fuel Prices': 'https://worldroadstatistics.org/get-data/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_317(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Energy consumption - by sector; gas & diesel oil consumption',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IRF', 'url': 'https://www.irf.global/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Energy consumption',
        'data_provider': 'IRF',
        'url': 'https://www.irf.global/',
        'data_access': 'publicly available',
        'units': ['tonnes of oil equivalent','tonnes'],
        'dimensioning': 'by sector; gas & diesel oil consumption'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Energy consumption': 'https://worldroadstatistics.org/get-data/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_318(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Road Accidents on roads - persons killed by road type, by road user, by sex, by vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IRF', 'url': 'https://www.irf.global/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Road Accidents on roads',
        'data_provider': 'IRF',
        'url': 'https://www.irf.global/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'persons killed by road type, by road user, by sex, by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Road Accidents on roads': 'https://worldroadstatistics.org/get-data/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_319(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Number of vehicles produced - by new&used imports, by vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IRF', 'url': 'https://www.irf.global/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Number of vehicles produced',
        'data_provider': 'IRF',
        'url': 'https://www.irf.global/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by new&used imports, by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Number of vehicles produced': 'https://worldroadstatistics.org/get-data/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_320(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Vehicle Fleet - by new&used imports, by vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IRF', 'url': 'https://www.irf.global/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Vehicle Fleet',
        'data_provider': 'IRF',
        'url': 'https://www.irf.global/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by new&used imports, by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Vehicle Fleet': 'https://worldroadstatistics.org/get-data/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_321(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Number of vehicles exported - by new&used imports, by vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IRF', 'url': 'https://www.irf.global/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Number of vehicles exported',
        'data_provider': 'IRF',
        'url': 'https://www.irf.global/',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'by new&used imports, by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Number of vehicles exported': 'https://worldroadstatistics.org/get-data/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_322(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Road expenditures and revenues - by source, by type of spend',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IRF', 'url': 'https://www.irf.global/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Road expenditures and revenues',
        'data_provider': 'IRF',
        'url': 'https://www.irf.global/',
        'data_access': 'publicly available',
        'units': ['USD'],
        'dimensioning': 'by source, by type of spend'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Road expenditures and revenues': 'https://worldroadstatistics.org/get-data/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_323(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'CO2 emissions transport sector - inland transport CO2 emissions by mode (road, rail, waterways)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2015-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['worldwide'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IRF', 'url': 'https://www.irf.global/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'CO2 emissions transport sector',
        'data_provider': 'IRF',
        'url': 'https://www.irf.global/',
        'data_access': 'publicly available',
        'units': ['tonnes/year'],
        'dimensioning': 'inland transport CO2 emissions by mode (road, rail, waterways)'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'CO2 emissions transport sector': 'https://worldroadstatistics.org/get-data/'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
# ATO
def dataset_324(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passengers Kilometer Travel - Railways',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passengers Kilometer Travel - Railways',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': ['pkm'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_325(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight Transport - Tonne-km for Railways',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight Transport - Tonne-km for Railways',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': ['Tonne-km'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_326(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Efficiency of Train Services',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Efficiency of Train Services',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_327(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Land Transport Passenger Kilometers Travel',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['rail','road'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Land Transport Passenger Kilometers Travel',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_328(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Land Transport Freight Kilometers Travel',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['rail','road'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Land Transport Freight Kilometers Travel',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_329(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passengers Kilometer Travel - HSR',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Passengers Kilometer Travel - HSR',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_330(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passengers Kilometer Travel - Domestic Aviation',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passengers Kilometer Travel - Domestic Aviation',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_331(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Air transport, carrier departures',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Air transport, carrier departures',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_332(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Aviation International Passenger Kilometers',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['international-aviation'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Aviation International Passenger Kilometers',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_333(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Aviation Trips per capita',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['international-aviation'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Aviation Trips per capita',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_334(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Aviation Trips per capita -2030 Forecast (BAU)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['international-aviation'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Aviation Trips per capita -2030 Forecast (BAU)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_335(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Aviation Total Passenger Kilometers',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['international-aviation'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Aviation Total Passenger Kilometers',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_336(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight Transport - Tonne-km for Aviation (Domestic)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight Transport - Tonne-km for Aviation (Domestic)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_337(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight Transport - Tonne-km for Aviation (Domestic+International)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight Transport - Tonne-km for Aviation (Domestic+International)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_338(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Efficiency of air transport services',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Efficiency of air transport services',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_339(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passengers Kilometer Travel - Bus',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passengers Kilometer Travel - Bus',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_340(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passengers Kilometer Travel - Roads',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cycling','two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passengers Kilometer Travel - Roads',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_341(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Motorised Two Wheeler Sales',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Motorised Two Wheeler Sales',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_342(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Motorised Three Wheeler Sales',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Motorised Three Wheeler Sales',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_343(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'LDV Sales',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'LDV Sales',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_344(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Total Vehicle sales (motorised)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Total Vehicle sales (motorised)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_345(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Commercial Vehicle Sales (motorised)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Commercial Vehicle Sales (motorised)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_346(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Vehicle registration (Motorised 2W)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Vehicle registration (Motorised 2W)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_347(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Vehicle registration (Motorised 3W)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Vehicle registration (Motorised 3W)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_348(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Vehicle registration (LDV)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Vehicle registration (LDV)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_349(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Vehicle registration (Bus)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Vehicle registration (Bus)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_350(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Vehicle registration (Others)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Vehicle registration (Others)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_351(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight Vehicle registration',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight Vehicle registration',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_352(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Total Vehicle Registration',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Total Vehicle Registration',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_353(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Motorisation Index',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Motorisation Index',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_354(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'LDV Motorisation Index',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['cars'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'LDV Motorisation Index',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_355(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Two and Three Wheelers Motorisation Index',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Two and Three Wheelers Motorisation Index',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_356(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Bus Motorisation Index',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Bus Motorisation Index',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_357(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight Vehicles Motorisation Index',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight Vehicles Motorisation Index',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_358(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight Transport - Tonne-km for Roads',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight Transport - Tonne-km for Roads',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_359(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Passengers Kilometer Travel - Waterways/shipping',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping','international-maritime'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passengers Kilometer Travel - Waterways/shipping',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_360(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight Transport - Tonne-km for Waterways/shipping (Domestic)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight Transport - Tonne-km for Waterways/shipping (Domestic)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': ['Tonne-km'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_361(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight Transport - Tonne-km for Waterways/shipping (Domestic+International)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping','international-maritime'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight Transport - Tonne-km for Waterways/shipping (Domestic+International)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': ['Tonne-km'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_362(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Port call and performance statistics',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping','international-maritime'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Port call and performance statistics',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_363(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Container port traffic (TEU)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping','international-maritime'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Container port traffic (TEU)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_364(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Merchant fleet by country of beneficial ownership, annual',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping','international-maritime'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Merchant fleet by country of beneficial ownership, annual',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_365(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Efficiency of seaport services',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping','international-maritime'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Efficiency of seaport services',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_366(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Total Passenger Kilometer Travel (Domestic+International)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Total Passenger Kilometer Travel (Domestic+International)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_367(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Total Passenger Kilometer Travel/Capita (Domestic+International)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Total Passenger Kilometer Travel/Capita (Domestic+International)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_368(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Total Passenger Kilometer Travel/GDP (Domestic+International)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Total Passenger Kilometer Travel/GDP (Domestic+International)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_369(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Total Passenger Kilometer Travel Mode Share (Domestic+International)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Total Passenger Kilometer Travel Mode Share (Domestic+International)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_370(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight Transport - Tonne-km (Total) (Domestic+International)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight Transport - Tonne-km (Total) (Domestic+International)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_371(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight tonne-km/GDP (Domestic+International)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight tonne-km/GDP (Domestic+International)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_372(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Freight tonne-km/capita (Domestic+International)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight tonne-km/capita (Domestic+International)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_373(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Total Freight Kilometer Travel Mode Share (Domestic+International)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Total Freight Kilometer Travel Mode Share (Domestic+International)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_374(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Internet shoppers as a share of Population',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Internet shoppers as a share of Population',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_375(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Internet shoppers as a share of Population (Female)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Internet shoppers as a share of Population (Female)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_376(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'UNCTAD B2C E-commerce index',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'UNCTAD B2C E-commerce index',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_377(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Logistics Performance Index',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Logistics Performance Index',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_378(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Domestic LPI',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Domestic LPI',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_379(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Percent Of Firms Identifying Transportation As A Major Constraint - Services',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Percent Of Firms Identifying Transportation As A Major Constraint - Services',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_380(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&',''),
        'notes': 'Percent of firms choosing transportation as their biggest obstacle - Manufacturing',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Percent of firms choosing transportation as their biggest obstacle - Manufacturing',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_381(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Transport services (% of service imports, BoP)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Transport services (% of service imports, BoP)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_382(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Transport services (% of service exports, BoP)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Transport services (% of service exports, BoP)',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_383(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Import of Transport Services',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Import of Transport Services',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_384(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Export of Transport Services',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2018-01-01',
        'temporal_coverage_end': '2018-01-01',
        'geographies': ['afg', 'arm', 'aus', 'aze', 'bgd', 'btn', 'brn', 'khm', 'chn', 'cxr', 'cck', 'cok', 'fji', 'geo', 'hkg', 'ind', 'idn', 'irn', 'irq', 'isr', 'jpn', 'kaz', 'kir', 'prk', 'kor', 'kgz', 'lao', 'lbn', 'mac', 'mys', 'mdv', 'mhl', 'mmr', 'npl', 'nru', 'nzl', 'pak', 'plw', 'png', 'phl', 'wsm', 'sgp', 'slb', 'lka', 'syr', 'tjk', 'tha', 'tls', 'ton', 'tkm', 'tuv', 'uzb', 'vut', 'vnm', 'yem'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ATO', 'url': 'https://asiantransportoutlook.com/snd/'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Export of Transport Services',
        'data_provider': 'Asian Transport Outlook',
        'url': 'https://asiantransportoutlook.com/snd/',
        'data_access': 'publicly available',
        'units': [''],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'Infrastructure (INF)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(INFRASTRUCTURE%20(INF)).xlsx',
            'Transport Activity & Services (TAS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(TRANSPORT%20ACTIVITY%20%26%20SERVICES%20(TAS)).xlsx',
            'Access & Connectivity (ACC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ACCESS%20%26%20CONNECTIVITY%20(ACC)).xlsx',
            'Road Safety (RSA)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(ROAD%20SAFETY%20(RSA)).xlsx',
            'Air Pollution & Health (APH)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(AIR%20POLLUTION%20%26%20HEALTH%20(APH)).xlsx',
            'Climate Change (CLC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(CLIMATE%20CHANGE%20(CLC)).xlsx',
            'Socio-Economic (SEC)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Transport Policy (POL)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(SOCIO-ECONOMIC%20(SEC)).xlsx',
            'Miscellaneous (MIS)': 'https://asiantransportoutlook.com/exportdl/?orig=1&filename=ATO%20Workbook%20(MISCELLANEOUS%20(MIS)).xlsx'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='xlsx'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
#ITF-OECD
def dataset_385(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Transport Infrastructure Expenditures (capital value, investment, maintenance)',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1995-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ITF questionnaire', 'url': 'https://www.itf-oecd.org/itf-statistics-questionnaires'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Transport Infrastructure Expenditures (capital value, investment, maintenance)',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['Currency'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_386(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'infrastructure investment',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2000-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'infrastructure investment',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['per GDP or in constant USD per inhabitant'],
        'dimensioning': 'infrastructure investment'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_387(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Freight Transport activity share - Share of transport mode in total inland freight transport',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2000-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight Transport activity share',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'Share of transport mode in total inland freight transport'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_388(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Passenger Transport activity share - Share of rail passenger transport in total inland passenger transport',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2000-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger Transport activity share',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'Share of rail passenger transport in total inland passenger transport'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_389(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Transport household expenditure - Share of household expenditure mode in total household expenditure for transport',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2000-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Transport household expenditure',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'Share of household expenditure mode in total household expenditure for transport'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_390(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Transport GHG emissions - Transport GHG emissions',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2000-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IEA', 'url': 'https://www.iea.org/'},
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Transport GHG emissions',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['tonnes/ 1mio. Units of current USD GDP','tonnes/inhabitant'],
        'dimensioning': 'Transport GHG emissions'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_391(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Share of CO2 emissions from road/domestic aviation/rail in total CO2 emission - Share of CO2 emissions from road/domestic aviation/rail in total CO2 emission',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2000-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IEA', 'url': 'https://www.iea.org/'},
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Share of CO2 emissions from road/domestic aviation/rail in total CO2 emission',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'Share of CO2 emissions from road/domestic aviation/rail in total CO2 emission'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_392(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Share of CO2 emissions from transport in total CO2 emissions - Share of CO2 emissions from transport in total CO2 emissions',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2000-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IEA', 'url': 'https://www.iea.org/'},
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Share of CO2 emissions from transport in total CO2 emissions',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'Share of CO2 emissions from transport in total CO2 emissions'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_393(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Modal Split - Share of trips by mode; Trips by mode',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2010-01-01',
        'temporal_coverage_end': '2050-01-01',
        'geographies': ['ind'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'The Energy Resources Institue (TERI)', 'url': 'https://www.teriin.org/'},
            {'title': 'Indian Urban Mobility Database (IUMD) ', 'url': 'https://www.urbanmobilityindia.in/Symposium/GeneralInfo.aspx'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Modal Split',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['Percentage','Number'],
        'dimensioning': 'Share of trips by mode; Trips by mode'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_394(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Passenger transport activiity - Transport activities by mode',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2010-01-01',
        'temporal_coverage_end': '2050-01-01',
        'geographies': ['ind'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'The Energy Resources Institue (TERI)', 'url': 'https://www.teriin.org/'},
            {'title': 'Indian Urban Mobility Database (IUMD) ', 'url': 'https://www.urbanmobilityindia.in/Symposium/GeneralInfo.aspx'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger transport activiity',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['PKM'],
        'dimensioning': 'Transport activities by mode'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_395(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Freight transport activity',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2010-01-01',
        'temporal_coverage_end': '2050-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'The Energy Resources Institue (TERI)', 'url': 'https://www.teriin.org/'},
            {'title': 'Indian Urban Mobility Database (IUMD) ', 'url': 'https://www.urbanmobilityindia.in/Symposium/GeneralInfo.aspx'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight transport activity',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['TKM'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_396(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Fuel consumption',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2010-01-01',
        'temporal_coverage_end': '2050-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'The Energy Resources Institue (TERI)', 'url': 'https://www.teriin.org/'},
            {'title': 'Indian Urban Mobility Database (IUMD) ', 'url': 'https://www.urbanmobilityindia.in/Symposium/GeneralInfo.aspx'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Fuel consumption',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['litres'],
        'dimensioning': 'Fuel consumption'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_397(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'CO2 emission transport',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2010-01-01',
        'temporal_coverage_end': '2050-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'The Energy Resources Institue (TERI)', 'url': 'https://www.teriin.org/'},
            {'title': 'Indian Urban Mobility Database (IUMD) ', 'url': 'https://www.urbanmobilityindia.in/Symposium/GeneralInfo.aspx'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'CO2 emission transport',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'Emissions'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_398(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Public transport access',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2010-01-01',
        'temporal_coverage_end': '2050-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'The Energy Resources Institue (TERI)', 'url': 'https://www.teriin.org/'},
            {'title': 'Indian Urban Mobility Database (IUMD) ', 'url': 'https://www.urbanmobilityindia.in/Symposium/GeneralInfo.aspx'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Public transport access',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['VKM by bus/inhabitant'],
        'dimensioning': 'Public transport access'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_399(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Air pollutants emissions - Sulphur Oxides, Nitrogen Oxides, PM10, PM2.5, Carbon Monoxide, Non-methane volatile organic compounds',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1990-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'UNECE-EMEP emissions database', 'url': 'https://aarhusclearinghouse.unece.org/resources/uneceemep-activity-data-and-emission-database'}
        ],
        'language': 'en',
        'sectors': ['all'],
        'modes': ['all'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Air pollutants emissions',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['tonnes'],
        'dimensioning': 'Sulphur Oxides, Nitrogen Oxides, PM10, PM2.5, Carbon Monoxide, Non-methane volatile organic compounds'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_400(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Freight transport activity',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ITF transport statistics based on transport ministries, statistical offices', 'url': 'https://www.itf-oecd.org/transport-data-and-statistics'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight transport activity',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['TKM','EU (twenty foot equivalent unit)','TKM per 1000 units of current USD GDP'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_401(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Road injuries/ casualties - Road injury crashes, road casualties',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Survey Trends in the Transport Sector', 'url': 'https://www.oecd-ilibrary.org/transport/trends-in-the-transport-sector_19991223'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Road injuries/ casualties',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['number'],
        'dimensioning': 'Road injury crashes, road casualties'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_402(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'New vehicle registration - first registrations of brand new road vehicles',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1975-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'New vehicle registration',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['#/1000 inhabitants','#/1 Mio. units of current USD GDP'],
        'dimensioning': 'first registrations of brand new road vehicles'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_403(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Inland total, by passenger cars and buses&coaches',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Survey Trends in the Transport Sector', 'url': 'https://www.oecd-ilibrary.org/transport/trends-in-the-transport-sector_19991223'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger Transport activity',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['PKM'],
        'dimensioning': 'Inland total, by passenger cars and buses&coaches'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_404(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'vehicle fleet - passenger cars, road motor vehicles, motorcycles, goods road motor vehicles, ',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1995-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'vehicle fleet',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['#/1000 inhabitants','#/1 Mio. units of current USD GDP'],
        'dimensioning': 'passenger cars, road motor vehicles, motorcycles, goods road motor vehicles'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_405(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Density of road - Density of road and rail lines',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2000-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'UIC', 'url': 'https://uic.org/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Density of road',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['km / 100 sq. Km'],
        'dimensioning': 'Density of road and rail lines'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_406(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Share of motorways/urban roads in total road network',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2000-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'IRTAD database (ITF)', 'url': 'https://www.itf-oecd.org/irtad-road-safety-database#:~:text=The%20IRTAD%20database%20contains%20validated,country%20and%20year%20from%201970.'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Share of motorways/urban roads in total road network',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'Share of motorways/urban roads in total road network'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_407(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Mileage',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2000-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Mileage',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['VKM / 1000 units of current USD GDP','1000 VKM / road motor vehicle'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_408(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Fuel demand - Motor fuel deliveries',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2000-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Fuel demand',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['tonnes per 1mio. Units of currents USD GDP/ inhabitant/ road motor vehicle'],
        'dimensioning': 'Motor fuel deliveries'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_409(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'vehicle fleet  - Vehicles by type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2010-01-01',
        'temporal_coverage_end': '2050-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'The Energy Resources Institue (TERI)', 'url': 'https://www.teriin.org/'},
            {'title': 'Indian Urban Mobility Database (IUMD) ', 'url': 'https://www.urbanmobilityindia.in/Symposium/GeneralInfo.aspx'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'vehicle fleet',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['#'],
        'dimensioning': 'Vehicles by type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_410(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'length of road infrastructure  - length of road network/footpaths/bike lanes',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2010-01-01',
        'temporal_coverage_end': '2050-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'The Energy Resources Institue (TERI)', 'url': 'https://www.teriin.org/'},
            {'title': 'Indian Urban Mobility Database (IUMD) ', 'url': 'https://www.urbanmobilityindia.in/Symposium/GeneralInfo.aspx'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'length of road infrastructure',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['KM'],
        'dimensioning': 'length of road network/footpaths/bike lanes'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_411(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Road density',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2010-01-01',
        'temporal_coverage_end': '2050-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'The Energy Resources Institue (TERI)', 'url': 'https://www.teriin.org/'},
            {'title': 'Indian Urban Mobility Database (IUMD) ', 'url': 'https://www.urbanmobilityindia.in/Symposium/GeneralInfo.aspx'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Road density',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['KM'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_412(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Passenger vehicle load Factor - Load Factor by vehicle type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2010-01-01',
        'temporal_coverage_end': '2050-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'The Energy Resources Institue (TERI)', 'url': 'https://www.teriin.org/'},
            {'title': 'Indian Urban Mobility Database (IUMD) ', 'url': 'https://www.urbanmobilityindia.in/Symposium/GeneralInfo.aspx'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger vehicle load Factor',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['persons'],
        'dimensioning': 'Load Factor by vehicle type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_413(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Number of passenger trips',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2010-01-01',
        'temporal_coverage_end': '2050-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'The Energy Resources Institue (TERI)', 'url': 'https://www.teriin.org/'},
            {'title': 'Indian Urban Mobility Database (IUMD) ', 'url': 'https://www.urbanmobilityindia.in/Symposium/GeneralInfo.aspx'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Number of passenger trips',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['number','KM'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_414(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Average trip length',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2010-01-01',
        'temporal_coverage_end': '2050-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'The Energy Resources Institue (TERI)', 'url': 'https://www.teriin.org/'},
            {'title': 'Indian Urban Mobility Database (IUMD) ', 'url': 'https://www.urbanmobilityindia.in/Symposium/GeneralInfo.aspx'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Average trip length',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['KM'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_415(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'vehicle fleet - Vehicle and fuel type',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2010-01-01',
        'temporal_coverage_end': '2050-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'ITF', 'url': 'https://www.itf-oecd.org/'},
            {'title': 'The Energy Resources Institue (TERI)', 'url': 'https://www.teriin.org/'},
            {'title': 'Indian Urban Mobility Database (IUMD) ', 'url': 'https://www.urbanmobilityindia.in/Symposium/GeneralInfo.aspx'}
        ],
        'language': 'en',
        'sectors': ['road'],
        'modes': ['two-three-wheelers','cars','private-cars','taxis','truck','bus'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'vehicle fleet',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['number'],
        'dimensioning': 'Vehicle and fuel type'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_416(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Freight transport activity',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ITF transport statistics based on transport ministries, statistical offices', 'url': 'https://www.itf-oecd.org/transport-data-and-statistics'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight transport activity',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['TKM','TEU (twenty foot equivalent unit)','TKM per 1000 units of current USD GDP'],
        'dimensioning': ''
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_417(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Passenger Transport activity - Inland passenger transport by Rail',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'Survey Trends in the Transport Sector', 'url': 'https://www.oecd-ilibrary.org/transport/trends-in-the-transport-sector_19991223'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Passenger Transport activity',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['PKM'],
        'dimensioning': 'Inland passenger transport by Rail'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_418(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'loading capacity - Rail freight loading capacity',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1995-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'UIC', 'url': 'https://uic.org/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'loading capacity',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['#/1000 inhabitants','#/1 Mio. units of current USD GDP'],
        'dimensioning': 'Rail freight loading capacity'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_419(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Density rail lines - Density of road and rail lines',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2000-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'UIC', 'url': 'https://uic.org/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Density rail lines',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['km / 100 sq. Km'],
        'dimensioning': 'Density of road and rail lines'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_420(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Share of electrified/high-speed rail ines in total rail network',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2000-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'UIC', 'url': 'https://uic.org/'}
        ],
        'language': 'en',
        'sectors': ['rail'],
        'modes': ['heavy-rail','high-speed-rail','transit-rail'],
        'services': ['passenger'],
        'frequency': 'as_needed',
        'indicators': 'Share of electrified/high-speed rail ines in total rail network',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'Share of electrified/high-speed rail ines in total rail network'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_421(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Freight transport activity - tkm for Coastal Shipping Containers transport, inland waterways freight transport',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1970-01-01',
        'temporal_coverage_end': '2021-01-01',
        'geographies': ['eur'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ITF transport statistics based on transport ministries, statistical offices', 'url': 'https://www.itf-oecd.org/transport-data-and-statistics'}
        ],
        'language': 'en',
        'sectors': ['water'],
        'modes': ['coastal-shipping','inland-shipping','international-maritime'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'Freight transport activity',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['TKM','TEU (twenty foot equivalent unit)','TKM per 1000 units of current USD GDP'],
        'dimensioning': 'tkm for Coastal Shipping Containers transport, inland waterways freight transport'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_422(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'seat capacity - Available seat capacity for scheduled flight',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1995-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'UIC', 'url': 'https://uic.org/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['freight'],
        'frequency': 'as_needed',
        'indicators': 'seat capacity',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['#/1000 inhabitants','#/1 Mio. units of current USD GDP','seats-km / 1000 units of current USD GDP'],
        'dimensioning': 'Available seat capacity for scheduled flight'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_423(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Share of set capacity - share of international seats-km in total seats-km',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '1995-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'ICAO', 'url': 'https://www.icao.int/Pages/default.aspx'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Share of set capacity',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['%'],
        'dimensioning': 'share of international seats-km in total seats-km'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
def dataset_424(org_id, dataset_title):
    
    data = {
        'title': dataset_title,
        'name': dataset_title.lower().replace(' - ', '-').replace(' ', '-').replace(',','').replace('(','').replace(')','').replace('/','').replace('&','').replace('%',''),
        'notes': 'Airport density',
        'license_id': 'CC-BY-4.0',
        'owner_org': org_id,
        'temporal_coverage_start': '2000-01-01',
        'temporal_coverage_end': '2020-01-01',
        'geographies': ['aus', 'aut', 'bel', 'can', 'chl', 'col', 'cze', 'dnk', 'est', 'fin', 'fra', 'deu', 'grc', 'hun', 'isl', 'irl', 'isr', 'ita', 'jpn', 'kor', 'lva', 'ltu', 'lux', 'mex', 'nld', 'nzl', 'nor', 'pol', 'prt', 'svk', 'svn', 'esp', 'swe', 'che', 'tur', 'gbr', 'usa'],
        'tdc_category': 'public',
        'sources': [
            {'title': 'World Bank', 'url': 'https://data.worldbank.org/'},
            {'title': 'Flightglobal', 'url': 'https://www.flightglobal.com/'}
        ],
        'language': 'en',
        'sectors': ['aviation'],
        'modes': ['domestic-aviation','international-aviation'],
        'services': ['passenger','freight'],
        'frequency': 'as_needed',
        'indicators': 'Airport density',
        'data_provider': 'ITF-OECD',
        'url': 'https://stats.oecd.org/index.aspx?lang=en',
        'data_access': 'publicly available',
        'units': ['# / 1 Mio. inhabitants','# / 100.000 sq. KM'],
        'dimensioning': 'Airport'
    }

    try:
        response = requests.post(
            urljoin(CKAN_URL, '/api/3/action/package_create'),
            json=data,
            headers={'Authorization': API_KEY, 'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raises an error for HTTP errors
        print('Dataset created successfully:', response.json())
        data_dict = {
            'OECD.Stat': 'https://stats.oecd.org/index.aspx?lang=en'
        }
        for key, value in data_dict.items():
            resource_name = key
            resource = value
            resource_format='webpage'
            create_resource_remote_url_with_format(data['name'], resource, resource_name, resource_format)
    except Exception as e:
        print('Error creating dataset:', str(e))
if __name__ == '__main__':
    #dataset_1('our-world-in-data', 'New passenger vehicle registrations by type Norway', 'Our World in Data/new-vehicles-type-area.csv')
    #dataset_2('our-world-in-data', 'Share of new passenger vehicles that are battery electric 2019', 'Our World in Data/share-vehicle-electric.csv')
    #dataset_3('our-world-in-data', 'Average carbon intensity of new passenger vehicles 2019', 'Our World in Data/carbon-new-passenger-vehicles.csv')
    #dataset_4('our-world-in-data', 'Fuel economy of new passenger vehicles 2019', 'Our World in Data/fuel-efficiency-new-vehicles.csv')
    #dataset_5('our-world-in-data', 'Global airline passenger capacity and traffic', 'Our World in Data/airline-capacity-and-traffic.csv')
    #dataset_6('our-world-in-data', 'Share of airline seats filled by passengers', 'Our World in Data/airline-passenger-load-factor.csv')
    #dataset_7('our-world-in-data', 'Per capita CO₂ emissions from domestic aviation 2018', 'Our World in Data/per-capita-co2-domestic-aviation.csv')
    #dataset_8('our-world-in-data', 'CO₂ emissions from domestic air travel 2018', 'Our World in Data/co2-emissions-domestic-aviation.csv')
    #dataset_9('our-world-in-data', 'Share of global CO₂ emissions from domestic air travel 2018', 'Our World in Data/share-global-co2-domestic-aviation.csv')
    #dataset_10('our-world-in-data', 'Per capita CO₂ emissions from international aviation 2018', 'Our World in Data/per-capita-co2-international-aviation.csv')
    #dataset_11('our-world-in-data', 'CO₂ emissions from international aviation 2018', 'Our World in Data/co2-international-aviation.csv')
    #dataset_12('our-world-in-data', 'Share of global CO₂ emissions from international aviation, 2018', 'Our World in Data/share-co2-international-aviation.csv')
    #dataset_13('our-world-in-data', 'Per capita CO₂ emissions from international passenger flights, tourism-adjusted, 2018', 'Our World in Data/per-capita-co2-international-flights-adjusted.csv')
    #dataset_14('our-world-in-data', 'Per capita CO₂ emissions from commercial aviation, tourism-adjusted, 2018', 'Our World in Data/per-capita-co2-aviation-adjusted.csv')
    #dataset_15('our-world-in-data', 'Per capita CO₂ emissions from aviation, 2018', 'Our World in Data/per-capita-co2-aviation.csv')
    #dataset_16('our-world-in-data', 'CO₂ emissions from aviation, 2018', 'Our World in Data/co2-emissions-aviation.csv')
    #dataset_17('our-world-in-data', 'Share of global CO₂ emissions from aviation, 2018', 'Our World in Data/share-co2-emissions-aviation.csv')
    #dataset_18('our-world-in-data', 'Per capita domestic aviation passenger kilometers, 2018', 'Our World in Data/per-capita-domestic-aviation-km.csv')
    #dataset_19('our-world-in-data', 'Share of global domestic aviation passenger kilometers, 2018', 'Our World in Data/share-global-domestic-aviation-km.csv')
    #dataset_20('our-world-in-data', 'Total domestic aviation passenger kilometers, 2018', 'Our World in Data/total-domestic-aviation-km.csv')
    #dataset_21('our-world-in-data', 'Per capita international aviation passenger kilometers, 2018', 'Our World in Data/per-capita-international-aviation-km.csv')
    #dataset_22('our-world-in-data', 'Share of global passenger kilometers from international aviation, 2018', 'Our World in Data/share-international-aviation-km.csv')
    #dataset_23('our-world-in-data', 'Total passenger kilometers from international aviation, 2018', 'Our World in Data/passenger-km-international-aviation.csv')
    #dataset_24('our-world-in-data', 'Per capita passenger kilometers from air travel, 2018', 'Our World in Data/per-capita-km-aviation.csv')
    #dataset_25('our-world-in-data', 'Share of global passenger kilometers from air travel, 2018', 'Our World in Data/share-km-aviation.csv')
    #dataset_26('our-world-in-data', 'Total passenger kilometers from air travel, 2018', 'Our World in Data/total-aviation-km.csv')
    #dataset_27('our-world-in-data', 'Tonne-kilometers of air freight, 2021', 'Our World in Data/air-transport-freight-ton-km.csv')
    #dataset_28('our-world-in-data', 'Passenger-kilometers by rail, 2021', 'Our World in Data/railways-passengers-carried-passenger-km.csv')
    #dataset_29('our-world-in-data', 'Energy intensity of transport per passenger-kilometer, 2018', 'Our World in Data/energy-intensity-transport.csv')
    #dataset_30('our-world-in-data', 'Per capita CO₂ emissions from transport, 2020', 'Our World in Data/per-capita-co2-transport.csv')
    #dataset_31('our-world-in-data', 'CO₂ emissions from transport, 2020', 'Our World in Data/co2-emissions-transport.csv')
    #dataset_32('climate-trace', 'Domestic aviation country emissions', 'Climatetrace/domestic-aviation_country_emissions.csv')
    #dataset_33('climate-trace', 'International aviation country emissions', 'Climatetrace/international-aviation_country_emissions.csv')
    #dataset_34('climate-trace', 'Other transport country emissions', 'Climatetrace/other-transport_country_emissions.csv')
    #dataset_35('climate-trace', 'Railways country emissions', 'Climatetrace/railways_country_emissions.csv')
    #dataset_36('climate-trace', 'Road transportation country emissions', 'Climatetrace/road-transportation_country_emissions.csv')
    #dataset_37('climate-trace', 'Domestic shipping country emissions', 'Climatetrace/domestic-shipping_country_emissions.csv')
    #dataset_38('climate-trace', 'International shipping country emissions', 'Climatetrace/international-shipping_country_emissions.csv')
    #dataset_39('world-bank', 'Air transport, registered carrier departures worldwide', 'World Bank/API_IS_AIR_DPRT_DS2_en_csv_v2_3415031.csv')
    #dataset_40('world-bank', 'Air transport, freight (million ton-km)', 'World Bank/API_IS_AIR_GOOD_MT_K1_DS2_en_csv_v2_3401747.csv')
    #dataset_41('world-bank', 'Air transport, passengers carried', 'World Bank/API_IS_AIR_PSGR_DS2_en_csv_v2_3401550.csv')
    #dataset_42('world-bank', 'Rail lines (total route-km)', 'World Bank/API_IS_RRS_TOTL_KM_DS2_en_csv_v2_3434344.csv')
    #dataset_43('world-bank', 'Railways, goods transported (million ton-km)', 'World Bank/API_IS_RRS_GOOD_MT_K6_DS2_en_csv_v2_3434337.csv')
    #dataset_44('world-bank', 'Railways, passengers carried (million passenger-km)', 'World Bank/API_IS_RRS_PASG_KM_DS2_en_csv_v2_3434340.csv')
    #dataset_45('world-bank', 'Container port traffic (TEU: 20 foot equivalent units)', 'World Bank/API_IS_SHP_GOOD_TU_DS2_en_csv_v2_3434242.csv')
    #dataset_46('oica', 'Global Sales Statistics 2019-2023', 'https://www.oica.net/wp-content/uploads/total_sales_2023.xlsx')
    #dataset_47('oica', 'Motorization rate 2020 - WORLDWIDE', 'https://www.oica.net/wp-content/uploads/Total-World-vehicles-in-use-2020.xlsx')
    #dataset_48('oica', '2023 production statistics')
    #dataset_49('acea', 'VEHICLES IN USE EUROPE 2022', 'https://www.acea.auto/files/ACEA-report-vehicles-in-use-europe-2022.pdf')
    #dataset_50('acea', 'NEW CAR REGISTRATIONS, EUROPEAN UNION IN JULY 2024', 'https://www.acea.auto/files/Press_release_car_registrations_July_2024.pdf')
    #dataset_51('acea', 'NEW COMMERCIAL VEHICLE REGISTRATIONS, EUROPEAN UNION H1 2024', 'https://www.acea.auto/files/Press_release_commercial_vehicle_registrations_H1-2024.pdf')
    #dataset_52('acea', 'NEW CAR REGISTRATIONS BY FUEL TYPE, EUROPEAN UNION IN Q4 2022', 'https://www.acea.auto/files/20230201_PRPC-fuel_Q4-2022_FINAL-1.pdf')
    #dataset_53('acea', 'NEW BUS, TRUCK AND VAN REGISTRATIONS BY FUEL TYPE, EUROPEAN UNION 2022')
    #dataset_54('acea', 'CO2 emissions from car production in the EU', 'https://www.acea.auto/figure/co2-emissions-from-car-production-in-eu')
    #dataset_55('acea', 'Energy consumption during car production in the EU', 'https://www.acea.auto/figure/energy-consumption-during-car-production-in-eu')
    #dataset_56('acea', 'Water used in car production in the EU', 'https://www.acea.auto/figure/water-used-in-car-production-in-eu')
    #dataset_57('acea', 'Waste from car production in the EU', 'https://www.acea.auto/figure/waste-from-car-production-in-eu')
    #dataset_58('ccg', 'Transport Starter Data Kit - PKM', 'https://zenodo.org/records/10406893/files/TSDK_ALL.xlsx')
    #dataset_59('ccg', 'Transport Starter Data Kit - TKM', 'https://zenodo.org/records/10406893/files/TSDK_ALL.xlsx')
    #dataset_60('ccg', 'Transport Starter Data Kit - Quantity', 'https://zenodo.org/records/10406893/files/TSDK_ALL.xlsx')
    #dataset_194('kapsarc', 'Vehicle Fuel Economy Data & CO2 emissions - road - kapsarc')
    #dataset_195('kapsarc', 'CO2 emissions from passenger cars - road - kapsarc')
    #dataset_196('kapsarc', 'Number of vehicles in use - road - kapsarc')
    #dataset_197('kapsarc', 'Vehicles registerd on the road - road - kapsarc')
    #dataset_198('kapsarc', 'Road Network - road - kapsarc')
    #dataset_199('kapsarc', 'Distance between main cities - road - kapsarc')
    #dataset_200('kapsarc', 'New passenger car registrations - road - kapsarc')
    #dataset_201('kapsarc', 'New road vehicle registrations - road - kapsarc')
    #dataset_202('kapsarc', 'Road vehicle fleet - road - kapsarc')
    #dataset_203('kapsarc', 'Passenger vehicle fleet - road - kapsarc')
    #dataset_204('kapsarc', 'Share of road transport - road - kapsarc')
    #dataset_205('kapsarc', 'Lenght of roads inside cities - road - kapsarc')
    #dataset_206('kapsarc', 'Registered motor vehicles - road - kapsarc')
    #dataset_207('kapsarc', 'Total road length - road - kapsarc')
    #dataset_208('kapsarc', 'Vehicle fleet - road - kapsarc')
    #dataset_209('kapsarc', 'Registered vehicles  - road - kapsarc')
    #dataset_210('kapsarc', 'Length of paved road - road - kapsarc')
    #dataset_211('kapsarc', 'Passenger transport activity - rail - kapsarc')
    #dataset_212('kapsarc', 'Freight transport activity - rail - kapsarc')
    #dataset_213('kapsarc', 'Freight transport activity - eurostat - rail - kapsarc')
    #dataset_214('kapsarc', 'Passenger transport activity - eurostat - rail - kapsarc')
    #dataset_215('kapsarc', 'Rolling Stock - rail - kapsarc')
    #dataset_216('kapsarc', 'Passenger transport activity - passengers carried - rail - kapsarc')
    #dataset_217('kapsarc', 'Distance between railway stations - rail - kapsarc')
    #dataset_218('kapsarc', 'Number of locomotives and cars - rail - kapsarc')
    #dataset_219('kapsarc', 'Passenger & Cargo Traffic - air - kapsarc')
    #dataset_220('kapsarc', 'Passenger activity - air - kapsarc')
    #dataset_221('kapsarc', 'Freight activity - air - kapsarc')
    #dataset_222('kapsarc', 'Air traffic - air - kapsarc')
    #dataset_223('kapsarc', 'Number of airplanes - air - kapsarc')
    #dataset_224('kapsarc', 'Cargo loaded/unloaded - water - kapsarc')
    #dataset_225('kapsarc', 'Volume of seaports exports - water - kapsarc')
    #dataset_226('kapsarc', 'Merchant fleet - water - kapsarc')
    #dataset_227('kapsarc', 'Freight transport activity - water - kapsarc')
    #dataset_228('kapsarc', 'Freight transport activity - tankers - water - kapsarc')
    #dataset_229('kapsarc', 'Modal split of freight transport - intermodal - kapsarc')
    #dataset_230('kapsarc', 'Passenger transport - intermodal - kapsarc')
    #dataset_231('kapsarc', 'Passenger, Freight and container transport - intermodal - kapsarc')
    #dataset_232('oak-ridge-national-laboratory', 'Petroleum production and consumption - intermodal - ornl')
    #dataset_233('oak-ridge-national-laboratory', 'Transportation petroleum consumption - intermodal - ornl')
    #dataset_234('oak-ridge-national-laboratory', 'Energy consumption - intermodal - ornl')
    #dataset_235('oak-ridge-national-laboratory', 'Fuel production, import, consumption - intermodal - ornl')
    #dataset_236('oak-ridge-national-laboratory', 'Transport energy/fuel consumption - intermodal - ornl')
    #dataset_237('oak-ridge-national-laboratory', 'Passenger travel activity - intermodal - ornl')
    #dataset_238('oak-ridge-national-laboratory', 'Energy intensity - intermodal - ornl')
    #dataset_239('oak-ridge-national-laboratory', 'Carbon content - intermodal - ornl')
    #dataset_240('oak-ridge-national-laboratory', 'CO2 emissions - intermodal - ornl')
    #dataset_241('oak-ridge-national-laboratory', 'Carbon coefficients - intermodal - ornl')
    #dataset_242('oak-ridge-national-laboratory', 'Freight transport activity - intermodal - ornl')
    #dataset_243('oak-ridge-national-laboratory', 'Average mile per freight trip - intermodal - ornl')
    #dataset_244('oak-ridge-national-laboratory', 'Average trip length - intermodal - ornl')
    #dataset_245('oak-ridge-national-laboratory', 'Emission of air pollutants - intermodal - ornl')
    #dataset_246('oak-ridge-national-laboratory', 'Vehicle Fleet (also intermodal) - road - ornl')
    #dataset_247('oak-ridge-national-laboratory', 'Modal split - road - ornl')
    #dataset_248('oak-ridge-national-laboratory', 'Travel activity (also intermodal) - road - ornl')
    #dataset_249('oak-ridge-national-laboratory', 'Fuel use & fuel economy (also intermodal) - road - ornl')
    #dataset_250('oak-ridge-national-laboratory', 'Fuel economy comparison - road - ornl')
    #dataset_251('oak-ridge-national-laboratory', 'Production shares - road - ornl')
    #dataset_252('oak-ridge-national-laboratory', 'Technology penetration - road - ornl')
    #dataset_253('oak-ridge-national-laboratory', 'Average material consumption - road - ornl')
    #dataset_254('oak-ridge-national-laboratory', 'Refueling stations - road - ornl')
    #dataset_255('oak-ridge-national-laboratory', 'Emission standards - road - ornl')
    #dataset_256('oak-ridge-national-laboratory', 'Driving cycle attributes - road - ornl')
    #dataset_257('oak-ridge-national-laboratory', 'Diesel share - road - ornl')
    #dataset_258('oak-ridge-national-laboratory', 'Carshare members - road - ornl')
    #dataset_259('oak-ridge-national-laboratory', 'Car operating costs - road - ornl')
    #dataset_260('oak-ridge-national-laboratory', 'Fuel costs - road - ornl')
    #dataset_261('oak-ridge-national-laboratory', 'Production weighted Carbon footprint - road - ornl')
    #dataset_262('oak-ridge-national-laboratory', 'Load factor - road - ornl')
    #dataset_263('oak-ridge-national-laboratory', 'Fleet - rail - ornl')
    #dataset_264('oak-ridge-national-laboratory', 'Average trip length - rail - ornl')
    #dataset_265('oak-ridge-national-laboratory', 'Traffic activity - rail - ornl')
    #dataset_266('oak-ridge-national-laboratory', 'Energy intensity - rail - ornl')
    #dataset_267('oak-ridge-national-laboratory', 'Fuel use - rail - ornl')
    #dataset_268('oak-ridge-national-laboratory', 'Fleet - water - ornl')
    #dataset_269('oak-ridge-national-laboratory', 'Energy use - water - ornl')
    #dataset_270('oak-ridge-national-laboratory', 'Freight activity - water - ornl')
    #dataset_271('oak-ridge-national-laboratory', 'Fuel use - water - ornl')
    #dataset_272('oak-ridge-national-laboratory', 'Fleet - air - ornl')
    #dataset_273('oak-ridge-national-laboratory', 'Travel activity - air - ornl')
    #dataset_274('oak-ridge-national-laboratory', 'Energy use - air - ornl')
    #dataset_275('oak-ridge-national-laboratory', 'Fuel use - air - ornl')
    #dataset_278('unece', 'Infrastructre length - road - unece')
    #dataset_279('unece', 'Vehicle fleet and new registrations - road - unece')
    #dataset_280('unece', 'Traffic motor vehicle movements - road - unece')
    #dataset_281('unece', 'Freight transport - road - unece')
    #dataset_282('unece', 'Passenger transport - road - unece')
    #dataset_283('unece', 'Safety, accidents, fatalities, and injuries - road - unece')
    #dataset_284('unece', 'Infrastructure length - rail - unece')
    #dataset_285('unece', 'Transport equipment - rail - unece')
    #dataset_286('unece', 'Traffic train movements - rail - unece')
    #dataset_287('unece', 'Freight transport - rail - unece')
    #dataset_288('unece', 'Passenger transport- rail - unece')
    #dataset_289('unece', 'Safety, accidents, fatalities, and injuries - rail - unece')
    #dataset_290('unece', 'Infrastructure navigable river length - water - unece')
    #dataset_291('unece', 'Vessels - water - unece')
    #dataset_292('unece', 'Freight transport - water - unece')
    #dataset_293('unece', 'Passenger transport - rail - unece')
    #dataset_294('caf-urban-mobility-observatory', 'Number of vehicles registered - road - caf')
    #dataset_295('caf-urban-mobility-observatory', 'Number of vehicles registered 2nd - road - caf')
    #dataset_296('caf-urban-mobility-observatory', 'Number of vehicles per inhabitant - road - caf')
    #dataset_297('caf-urban-mobility-observatory', 'Number of vehicles per inhabitant 2nd - road - caf')
    #dataset_298('caf-urban-mobility-observatory', 'Number of public transit vehicles registered - road - caf')
    #dataset_299('caf-urban-mobility-observatory', 'Number of trips per person per day - road - caf')
    #dataset_300('caf-urban-mobility-observatory', 'Modal Split - road - caf')
    #dataset_301('international-union-of-railways', 'CO2 emissions - rail - uic')
    #dataset_302('international-union-of-railways', 'Total emissions - rail - uic')
    #dataset_303('international-union-of-railways', 'Energy consumption - rail - uic')
    #dataset_304('international-union-of-railways', 'Air pollutants emissions - rail - uic')
    #dataset_305('slocat', 'Transport Knowledge Base - all - slocat')
    #dataset_306('un-sdg-indicator-database', 'Death rate due to road traffic injuries - road - sdg')
    #dataset_307('un-sdg-indicator-database', 'Freight volume - all - sdg')
    #dataset_308('un-sdg-indicator-database', 'Passenger volume - all - sdg')
    #dataset_309('un-sdg-indicator-database', 'Freight loaded and uloaded - water - sdg')
    #dataset_310('un-sdg-indicator-database', 'Proportion of population that has convenient access to public transport - all - sdg')
    #dataset_311('international-road-federation', 'Road Network length - road - irf')
    #dataset_312('international-road-federation', 'Road vehicle mileage - road - irf')
    #dataset_313('international-road-federation', 'Freight ton-kilometer - road - irf')
    #dataset_314('international-road-federation', 'Passenger Person-kilometer - road - irf')
    #dataset_315('international-road-federation', 'Vehicle fleet - road - irf')
    #dataset_316('international-road-federation', 'Fuel Prices - road - irf')
    #dataset_317('international-road-federation', 'Energy consumption - road - irf')
    #dataset_318('international-road-federation', 'Road Accidents on roads - road - irf')
    #dataset_319('international-road-federation', 'Number of vehicles produced - road - irf')
    #dataset_320('international-road-federation', 'Vehicle Fleet new - road - irf')
    #dataset_321('international-road-federation', 'Number of vehicles exported - road - irf')
    #dataset_322('international-road-federation', 'Road expenditures and revenues - road - irf')
    #dataset_323('international-road-federation', 'CO2 emissions transport sector - all - irf')
    #dataset_324('asian-transport-outlook', 'Passengers Kilometer Travel - rail - ato')
    #dataset_325('asian-transport-outlook', 'Freight Transport - rail - ato')
    #dataset_326('asian-transport-outlook', 'Efficiency of Train Services - rail - ato')
    #dataset_327('asian-transport-outlook', 'Land Transport Passenger Kilometers Travel - rail - ato')
    #dataset_328('asian-transport-outlook', 'Land Transport Freight Kilometers Travel - rail - ato')
    #dataset_329('asian-transport-outlook', 'Passengers Kilometer Travel - HSR - rail - ato')
    #dataset_330('asian-transport-outlook', 'Passengers Kilometer Travel - Domestic Aviation - air - ato')
    #dataset_331('asian-transport-outlook', 'Air transport carrier departures - air - ato')
    #dataset_332('asian-transport-outlook', 'Aviation International Passenger Kilometers - air - ato')
    #dataset_333('asian-transport-outlook', 'Aviation Trips per capita - air - ato')
    #dataset_334('asian-transport-outlook', 'Aviation Trips per capita -2030 Forecast (BAU) - air - ato')
    #dataset_335('asian-transport-outlook', 'Aviation Total Passenger Kilometers - air - ato')
    #dataset_336('asian-transport-outlook', 'Freight Transport - Tonne-km for Aviation - air - ato')
    #dataset_337('asian-transport-outlook', 'Freight Transport - Tonne-km for Aviation international - air - ato')
    #dataset_338('asian-transport-outlook', 'Efficiency of air transport services - air - ato')
    #dataset_339('asian-transport-outlook', 'Passengers Kilometer Travel - Bus - road - ato')
    #dataset_340('asian-transport-outlook', 'Passengers Kilometer Travel - Roads - road - ato')
    #dataset_341('asian-transport-outlook', 'Motorised Two Wheeler Sales - road - ato')
    #dataset_342('asian-transport-outlook', 'Motorised Three Wheeler Sales - road - ato')
    #dataset_343('asian-transport-outlook', 'LDV Sales - road - ato')
    #dataset_344('asian-transport-outlook', 'Total Vehicle sales (motorised) - road - ato')
    #dataset_345('asian-transport-outlook', 'Commercial Vehicle Sales (motorised) - road - ato')
    #dataset_346('asian-transport-outlook', 'Vehicle registration (Motorised 2W) - road - ato')
    #dataset_347('asian-transport-outlook', 'Vehicle registration (Motorised 3W) - road - ato')
    #dataset_348('asian-transport-outlook', 'Vehicle registration (LDV) - road - ato')
    #dataset_349('asian-transport-outlook', 'Vehicle registration (Bus) - road - ato')
    #dataset_350('asian-transport-outlook', 'Vehicle registration (Others) - road - ato')
    #dataset_351('asian-transport-outlook', 'Freight Vehicle registration - road - ato')
    #dataset_352('asian-transport-outlook', 'Total Vehicle Registration - road - ato')
    #dataset_353('asian-transport-outlook', 'Motorisation Index - road - ato')
    #dataset_354('asian-transport-outlook', 'LDV Motorisation Index - road - ato')
    #dataset_355('asian-transport-outlook', 'Two and Three Wheelers Motorisation Index - road - ato')
    #dataset_356('asian-transport-outlook', 'Bus Motorisation Index - road - ato')
    #dataset_357('asian-transport-outlook', 'Freight Vehicles Motorisation Index - road - ato')
    #dataset_358('asian-transport-outlook', 'Freight Transport - Tonne-km for Roads - road - ato')
    #dataset_359('asian-transport-outlook', 'Passengers Kilometer Travel - water - ato')
    #dataset_360('asian-transport-outlook', 'Freight Transport - Domestic - water - ato')
    #dataset_361('asian-transport-outlook', 'Freight Transport - International - water - ato')
    #dataset_362('asian-transport-outlook', 'Port call and performance statistics - water - ato')
    #dataset_363('asian-transport-outlook', 'Container port traffic (TEU) - water - ato')
    #dataset_364('asian-transport-outlook', 'Merchant fleet by country of beneficial ownership, annual - water - ato')
    #dataset_365('asian-transport-outlook', 'Efficiency of seaport services - water - ato')
    #dataset_366('asian-transport-outlook', 'Total Passenger Kilometer Travel - all - ato')
    #dataset_367('asian-transport-outlook', 'Total Passenger Kilometer Travel/Capita - all - ato')
    #dataset_368('asian-transport-outlook', 'Total Passenger Kilometer Travel/GDP - all - ato')
    #dataset_369('asian-transport-outlook', 'Total Passenger Kilometer Travel Mode Share - all - ato')
    #dataset_370('asian-transport-outlook', 'Freight Transport - Tonne-km (Total) - all - ato')
    #dataset_371('asian-transport-outlook', 'Freight tonne-km/GDP - all - ato')
    #dataset_372('asian-transport-outlook', 'Freight tonne-km/capita - all - ato')
    #dataset_373('asian-transport-outlook', 'Total Freight Kilometer Travel Mode Share - all - ato')
    #dataset_374('asian-transport-outlook', 'Internet shoppers as a share of Population - all - ato')
    #dataset_375('asian-transport-outlook', 'Internet shoppers as a share of Population (Female) - all - ato')
    #dataset_376('asian-transport-outlook', 'UNCTAD B2C E-commerce index - all - ato')
    #dataset_377('asian-transport-outlook', 'Logistics Performance Index - all - ato')
    #dataset_378('asian-transport-outlook', 'Domestic LPI - all - ato')
    #dataset_379('asian-transport-outlook', 'Percent Of Firms Identifying Transportation As A Major Constraint - Services - all - ato')
    #dataset_380('asian-transport-outlook', 'Percent of firms choosing transportation as their biggest obstacle - Manufacturing - all - ato')
    #dataset_381('asian-transport-outlook', 'Transport services (% of service imports, BoP) - all - ato')
    #dataset_382('asian-transport-outlook', 'Transport services (% of service exports, BoP) - all - ato')
    #dataset_383('asian-transport-outlook', 'Import of Transport Services - all - ato')
    #dataset_384('asian-transport-outlook', 'Export of Transport Services - all - ato')
    #dataset_385('itf-oecd', 'Transport Infrastructure Expenditures (capital value, investment, maintenance) - all - itf-oecd')
    #dataset_386('itf-oecd', 'Infrastructure investment - all - itf-oecd')
    #dataset_387('itf-oecd', 'Freight Transport activity share - all - itf-oecd')
    #dataset_388('itf-oecd', 'Passenger Transport activity share - all - itf-oecd')
    #dataset_389('itf-oecd', 'Transport household expenditure - all - itf-oecd')
    #dataset_390('itf-oecd', 'Transport GHG emissions - all - itf-oecd')
    #dataset_391('itf-oecd', 'Share of CO2 emissions from road/domestic aviation/rail in total CO2 emission - all - itf-oecd')
    #dataset_392('itf-oecd', 'Share of CO2 emissions from transport in total CO2 emissions - all - itf-oecd')
    #dataset_393('itf-oecd', 'Modal Split - all - itf-oecd')
    #dataset_394('itf-oecd', 'Passenger transport activiity - IND - all - itf-oecd')
    #dataset_395('itf-oecd', 'Freight transport activity - all - itf-oecd')
    #dataset_396('itf-oecd', 'Fuel consumption - all - itf-oecd')
    #dataset_397('itf-oecd', 'CO2 emission transport - all - itf-oecd')
    #dataset_398('itf-oecd', 'Public transport access - all - itf-oecd')
    #dataset_399('itf-oecd', 'Air pollutants emissions - all - itf-oecd')
    #dataset_400('itf-oecd', 'Freight transport activity - road - itf-oecd')
    #dataset_401('itf-oecd', 'Road injuries/ casualties - road - itf-oecd')
    #dataset_402('itf-oecd', 'New vehicle registration - road - itf-oecd')
    #dataset_403('itf-oecd', 'Passenger Transport activity - road - itf-oecd')
    #dataset_404('itf-oecd', 'Vehicle fleet - road - itf-oecd')
    #dataset_405('itf-oecd', 'Density of road - road - itf-oecd')
    #dataset_406('itf-oecd', 'Share of motorways/urban roads in total road network - road - itf-oecd')
    #dataset_407('itf-oecd', 'Mileage - road - itf-oecd')
    #dataset_408('itf-oecd', 'Fuel demand - road - itf-oecd')
    #dataset_409('itf-oecd', 'Vehicle fleet - vehicles by type  - road - itf-oecd')
    #dataset_410('itf-oecd', 'Length of road infrastructure - road - itf-oecd')
    #dataset_411('itf-oecd', 'Road density - road - itf-oecd')
    #dataset_412('itf-oecd', 'Passenger vehicle load Factor - road - itf-oecd')
    #dataset_413('itf-oecd', 'Number of passenger trips - road - itf-oecd')
    #dataset_414('itf-oecd', 'Average trip length - road - itf-oecd')
    #dataset_415('itf-oecd', 'Vehicle fleet - vehicle and fuel type - road - itf-oecd')
    #dataset_416('itf-oecd', 'Freight transport activity - rail - itf-oecd')
    #dataset_417('itf-oecd', 'Passenger Transport activity - rail - itf-oecd')
    #dataset_418('itf-oecd', 'Loading capacity - rail - itf-oecd')
    #dataset_419('itf-oecd', 'Density rail lines - rail - itf-oecd')
    #dataset_420('itf-oecd', 'Share of electrified/high-speed rail ines in total rail network - rail - itf-oecd')
    #dataset_421('itf-oecd', 'Freight transport activity - water - itf-oecd')
    #dataset_422('itf-oecd', 'Seat capacity - avia - itf-oecd')
    #dataset_423('itf-oecd', 'Share of set capacity - avia - itf-oecd')
    #dataset_424('itf-oecd', 'Airport density - avia - itf-oecd')