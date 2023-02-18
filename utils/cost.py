import requests
import json
from presets import presets

# TODO: standardize with SKUs

def get_cost_from_torpedo_product(vendor_name="gcp",product='DemoSession'):
    if vendor_name == 'gcp':
        return get_cost(vendor_name=vendor_name,service='Compute Engine', region = 'us-west1', productFamily ='Compute Instance',machine_type=presets['gcp'][product])
    elif vendor_name == 'aws':
        # undefined, need to find good AWS instances first
        return get_cost(machine_type=presets['aws'][product])
def get_cost(vendor_name = "aws", service = 'AmazonEC2', region = 'us-east-1', productFamily=None, machine_type = 'm3.large'):
    headers = {
        'X-Api-Key': 'ico-ZhdTlKXsD4kUtB4ZuGOSl4L2adtD2u5f',
        'Content-Type': 'application/json',
    }
    if vendor_name=='gcp':
        
        query_string = "{products(filter:{vendorName:\"%s\",service:\"%s\", productFamily: \"%s\" region:\"%s\",attributeFilters:[{key:\"machineType\",value:\"%s\"}]}) {prices(filter:{purchaseOption:\"on_demand\"}) {USD}}}" % (vendor_name,service, productFamily, region, machine_type)
    elif vendor_name=='aws': 
        productFamily='EC2 THING'
        query_string = "{products(filter:{vendorName:\"%s\",service:\"%s\", productFamily: \"%s\" region:\"%s\",attributeFilters:[{key:\"instanceType\",value:\"%s\"}]}) {prices(filter:{purchaseOption:\"on_demand\"}) {USD}}}" % (vendor_name,service, productFamily, region, machine_type)
    json_string = {"query": query_string}


    response = requests.post('https://pricing.api.infracost.io/graphql', headers=headers, json=json_string)

    return (response.json())


#for key in presets['gcp'].keys():
#    print(get_cost_from_torpedo_product(vendor_name="gcp",product=key))
