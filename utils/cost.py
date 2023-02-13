import requests
import json
from presets import presets

# TODO: standardize with SKUs

def get_cost(vendor_name = "aws", service = 'AmazonEC2', region = 'us-east-1', machine_type = 'm3.large'):
    headers = {
        'X-Api-Key': 'ico-ZhdTlKXsD4kUtB4ZuGOSl4L2adtD2u5f',
        'Content-Type': 'application/json',
    }
    query_string = "{products(filter:{vendorName:\"%s\",service:\"%s\",region:\"%s\",attributeFilters:[{key:\"instanceType\",value:\"%s\"},{key:\"operatingSystem\",value:\"Linux\"},{key:\"tenancy\",value:\"Shared\"},{key:\"capacitystatus\",value:\"Used\"},{key:\"preInstalledSw\",value:\"NA\"}]}) {prices(filter:{purchaseOption:\"on_demand\"}) {USD}}}" % (vendor_name,service,region, machine_type)
    json_string = {"query": query_string}


    response = requests.post('https://pricing.api.infracost.io/graphql', headers=headers, json=json_string)

    return (response.json())

print(get_cost())
print(get_cost(vendor_name="gcp",service='Compute Engine',machine_type=presets[0]['gcp'][0]['DataAnalyticsOffering']))
