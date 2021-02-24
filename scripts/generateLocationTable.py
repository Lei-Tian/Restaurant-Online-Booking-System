import json
from geopy.geocoders import Nominatim
results = set()
with open("yelp_academic_dataset_restaurant.json") as f:
    for record in f:
        data = json.loads(record)
        results.add((data['city'], data['state']))
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
        if state in canada_states:
            country = "Canada"
        elif state in us_states:
            country = "USA"
        else:
            #geolocator = Nominatim(user_agent="geoapiExercises")
            #location = geolocator.reverse(str(latitude) + "," + str(longitude))
            #address = location.raw['address']
            #country = address.get('country', '')
            #print(city, state, latitude, longitude, country)
            # there are only 2 such records, both are in Canada: 
            # 1) Leeds XWY 43.6528212 -79.3763454 Canada
            # 2) Hartlepool HPL 43.7429401909 -79.220507741 Canada
            country = "Canada"
        h.write(str(id_) + "," + city + ',' + state + ',' + country + '\n')
        id_ += 1
