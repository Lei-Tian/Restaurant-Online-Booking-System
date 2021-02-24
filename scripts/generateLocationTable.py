import json
from geopy.geocoders import Nominatim
results = set()
with open("yelp_academic_dataset_restaurant.json") as f:
    for record in f:
        data = json.loads(record)
        city = data['city']#[0].upper() + data['city'][1:].lower()
        results.add((city, data['state']))
canada_states = set(["AB","BC","MB","NB","NL","NT","NS","NU","ON","PE","QC","SK","YT"])
us_states = set(['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL',
                 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH',
                 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 
                 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC',
                 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY'])
with open('location.csv', 'w') as h:
    h.write('id,City,State,Country\n')
    id_ = 1
    for city, state in results:
        if state in canada_states or state in us_states:
            if city.count(",") == 0 and city != "4321 w flamingo rd" and city != "Rocky view no. 44":
                if state in us_states:
                    country = "USA"
                else:
                    country = "Canada"
                h.write(str(id_) + "," + city + ',' + state + ',' + country + '\n')
                id_ += 1
        
        
