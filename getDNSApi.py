import requests
import json

# API Key and URL
API_KEY = 'h523hDtETbkJ3nSJL323hjYLXbCyDaRZ'
BASE_URL = 'https://api.recruitment.shq.nz'
CLIENT_ID = 100  # Given client ID

def get_domains(client_id):
    """Get list of domains for a given client ID."""
    url = f"{BASE_URL}/domains/{client_id}?api_key={API_KEY}"
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # JSON response, expecting it to be a list
    else:
        print(f"Failed to retrieve domains: {response.status_code}")
        return None

def get_dns_records(zone_id):
    """Get DNS records for a given zone ID."""
    url = f"{BASE_URL}/zones/{zone_id}?api_key={API_KEY}"
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # JSON response with DNS records
    else:
        print(f"Failed to retrieve DNS records: {response.status_code}")
        return None

def main():
    # Fetching domains for the client
    domains = get_domains(CLIENT_ID)
    
    if domains:
        print(f"Domains for client {CLIENT_ID}:")
        for domain in domains:
            print(f"\nDomain: {domain['name']}")
            
            # For each domain, get DNS records for associated zones
            for zone in domain.get('zones', []):
                print(f"  Zone: {zone['name']} (URI: {zone['uri']})")
                # Extract zone_id from URI
                zone_id = zone['uri'].split('/')[-1]
                dns_records = get_dns_records(zone_id)
                
                if dns_records and 'records' in dns_records:
                    print("  DNS Records:")
                    for record in dns_records['records']:
                        record_type = record.get('type', 'None')
                        record_name = record.get('name', 'None')
                        record_value = record.get('value', 'None')  # Handle missing 'value' field
                        print(f"    - Type: {record_type}, Name: {record_name}, Value: {record_value}")
                else:
                    print(f"    No DNS records found for zone {zone['name']}.")
    else:
        print("No domains found or API response was empty.")

if __name__ == '__main__':
    main()
