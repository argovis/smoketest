import requests, time, os

# Define the API endpoint
#APIX = "https://argovis-apix-atoc-argovis-dev.apps.containers02.colorado.edu"
APIX = "https://admt-experimental.colorado.edu"  # repurposed the admt-api public route to explore if going through officially public CU routers matters; might want to change the service this route points to back to admt-api if it ever matter.
API = "https://argovis-api.colorado.edu"
TOKEN = os.getenv('TOKEN')

def smoke_test(API, APIX, TOKEN, route):
    print("Testing", route)    

    print("    Testing", API)
    start_time = time.time()
    try:
        response_api = requests.get(API + route, headers={'x-argokey': TOKEN})
    except requests.exceptions.RequestException as e:
        print("        Request failed:", e)
        return
    elapsed_time_api = time.time() - start_time
    print(f"        Request took {elapsed_time_api:.2f} seconds")
    print(f"        Request returned status code {response_api.status_code}")
    try:
        response_api_json = response_api.json()
        if '_id' in response_api_json[0]:
            response_api_json.sort(key=lambda x: x['_id'])
    except ValueError:
        print("        Response is not valid JSON.")

    print("    Testing", APIX)
    start_time = time.time()
    try:
        response_apix = requests.get(APIX + route, headers={'x-argokey': TOKEN})
    except requests.exceptions.RequestException as e:
        print("        Request failed:", e)
        return
    elapsed_time_apix = time.time() - start_time
    print(f"        Request took {elapsed_time_apix:.2f} seconds")
    print(f"        Request returned status code {response_apix.status_code}")
    try:
        response_apix_json = response_apix.json()
        if '_id' in response_apix_json[0]:
            response_apix_json.sort(key=lambda x: x['_id'])
    except ValueError:
        print("        Response is not valid JSON.")

    print("        Responses are identical:", response_api_json == response_apix_json)

    return [elapsed_time_api, elapsed_time_apix, response_api_json, response_apix_json]

# routes_to_check = [
#    '/argone?forecastOrigin=-178,-44',
#    '/argone?forecastOrigin=-178,-44&data=all',
#    '/argone?forecastOrigin=-178,-44&data=90,180',
#    '/argone?forecastOrigin=-178,-44&compression=minimal'
# ] 


routes_to_check = [
   '/argo?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]',
   '/argo?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&startDate=2010-01-01T00:00:00Z&endDate=2011-01-01T00:00:00Z',
   '/argo?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&startDate=2010-01-01T00:00:00Z&endDate=2011-01-01T00:00:00Z&data=all',
   '/argo?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&startDate=2010-01-01T00:00:00Z&endDate=2011-01-01T00:00:00Z&data=all&verticalRange=0,100.12345', # recall we started excluding the lower vertical bound, so for these purposes let's check bounds that probably dont exactly appear in the dataset.
   '/argo?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&startDate=2010-01-01T00:00:00Z&endDate=2011-01-01T00:00:00Z&data=temperature,pressure',
   '/argo?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&startDate=2010-01-01T00:00:00Z&endDate=2011-01-01T00:00:00Z&data=temperature,1,pressure',
   '/argo?platform=4902354',
   '/argo?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&batchmeta=true', # json mismatch, prod api is wrong, see batchmeta_argo_mismatch.py
   '/argo?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&compression=minimal',
   '/argo?startDate=2021-01-01T00:00:00Z&endDate=2021-01-11T00:00:00Z&compression=minimal'
]

# routes_to_check = [
#    '/argotrajectories?polygon=[[-27,4],[-29,4],[-29,6],[-27,6],[-27,4]]',
#    '/argotrajectories?polygon=[[-27,4],[-29,4],[-29,6],[-27,6],[-27,4]]&data=all',
#    '/argotrajectories?polygon=[[-27,4],[-29,4],[-29,6],[-27,6],[-27,4]]&data=velocity_zonal',
#    '/argotrajectories?platform=13857',
#    '/argotrajectories?polygon=[[-27,4],[-29,4],[-29,6],[-27,6],[-27,4]]&batchmeta=true',
#    '/argotrajectories?polygon=[[-27,4],[-29,4],[-29,6],[-27,6],[-27,4]]&compression=minimal',
# ]

# routes_to_check = [
#    '/cchdo?startDate=2010-01-01T00:00:00Z&endDate=2010-02-01T00:00:00Z',
#    '/cchdo?startDate=2010-01-01T00:00:00Z&endDate=2010-02-01T00:00:00Z&data=all',
#    '/cchdo?startDate=2010-01-01T00:00:00Z&endDate=2010-02-01T00:00:00Z&data=all&verticalRange=0,100.12345', 
#    '/cchdo?startDate=2010-01-01T00:00:00Z&endDate=2010-02-01T00:00:00Z&data=temperature,pressure',
#    '/cchdo?startDate=2010-01-01T00:00:00Z&endDate=2010-02-01T00:00:00Z&data=temperature,0,pressure',
#    '/cchdo?woceline=A10',
#    '/cchdo?startDate=2010-01-01T00:00:00Z&endDate=2010-02-01T00:00:00Z&batchmeta=true',
#    '/cchdo?startDate=2010-01-01T00:00:00Z&endDate=2010-02-01T00:00:00Z&compression=minimal',
# ]

# routes_to_check = [
#    '/easyocean?startDate=2010-01-01T00:00:00Z&endDate=2010-02-01T00:00:00Z',
#    '/easyocean?startDate=2010-01-01T00:00:00Z&endDate=2010-02-01T00:00:00Z&data=all',
#    '/easyocean?startDate=2010-01-01T00:00:00Z&endDate=2010-02-01T00:00:00Z&data=all&verticalRange=0,100.12345',
#    '/easyocean?startDate=2010-01-01T00:00:00Z&endDate=2010-02-01T00:00:00Z&data=pressure,ctd_temperature',
#    '/easyocean?startDate=2010-01-01T00:00:00Z&endDate=2010-02-01T00:00:00Z&data=all&batchmeta=true',
#    '/easyocean?startDate=2010-01-01T00:00:00Z&endDate=2010-02-01T00:00:00Z&data=all&compression=minimal',
# ]

# routes_to_check = [
#     '/extended/ar?box=[[-35,-55],[-34,-54]]&startDate=2020-01-01T00:00:00Z&endDate=2021-01-01T00:00:00Z',
#     '/extended/ar?box=[[-35,-55],[-34,-54]]&startDate=2020-01-01T00:00:00Z&endDate=2021-01-01T00:00:00Z&data=all',
#     '/extended/ar?box=[[-35,-55],[-34,-54]]&startDate=2020-01-01T00:00:00Z&endDate=2021-01-01T00:00:00Z&batchmeta=true',
#     '/extended/ar?box=[[-35,-55],[-34,-54]]&startDate=2020-01-01T00:00:00Z&endDate=2021-01-01T00:00:00Z&compression=minimal',
# ]

# routes_to_check = [
#    '/grids/rg09?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]',
#    '/grids/rg09?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&startDate=2010-01-01T00:00:00Z&endDate=2011-01-01T00:00:00Z',
#    '/grids/rg09?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&startDate=2010-01-01T00:00:00Z&endDate=2011-01-01T00:00:00Z&data=all',
#    '/grids/rg09?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&startDate=2010-01-01T00:00:00Z&endDate=2011-01-01T00:00:00Z&data=all&verticalRange=0,100.12345',
#    '/grids/rg09?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&startDate=2010-01-01T00:00:00Z&endDate=2011-01-01T00:00:00Z&data=rg09_temperature',
#    '/grids/rg09?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&batchmeta=true',
#    '/grids/rg09?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&compression=minimal',
# ]

# routes_to_check = [
#    '/grids/kg21?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]',
#    '/grids/kg21?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&startDate=2010-01-01T00:00:00Z&endDate=2011-01-01T00:00:00Z',
#    '/grids/kg21?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&startDate=2010-01-01T00:00:00Z&endDate=2011-01-01T00:00:00Z&data=all',
#    '/grids/kg21?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&startDate=2010-01-01T00:00:00Z&endDate=2011-01-01T00:00:00Z&data=kg21_ohc15to300',
#    '/grids/kg21?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&batchmeta=true',
#    '/grids/kg21?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&compression=minimal',
# ]

# routes_to_check = [
#    '/grids/glodap?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]',
#    '/grids/glodap?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&data=all',
#    '/grids/glodap?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&data=all&verticalRange=0,100.12345', 
#    '/grids/glodap?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&data=NO3,OmegaA',
#    '/grids/glodap?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&batchmeta=true',
#    '/grids/glodap?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]&compression=minimal',
# ]

# routes_to_check = [
#    '/tc?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]',
#    '/tc?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&startDate=2010-01-01T00:00:00Z&endDate=2020-01-01T00:00:00Z',
#    '/tc?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&startDate=2010-01-01T00:00:00Z&endDate=2020-01-01T00:00:00Z&data=all',
#    '/tc?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&startDate=2010-01-01T00:00:00Z&endDate=2020-01-01T00:00:00Z&data=wind',
#    '/tc?name=MARIA',
#    '/tc?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&batchmeta=true',
#    '/tc?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&compression=minimal',
# ]

# routes_to_check = [
#    '/timeseries/noaasst?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]',
#    '/timeseries/noaasst?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&startDate=2010-01-01T00:00:00Z&endDate=2020-01-01T00:00:00Z',
#    '/timeseries/noaasst?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&startDate=2010-01-01T00:00:00Z&endDate=2020-01-01T00:00:00Z&data=all',
#    '/timeseries/noaasst?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&startDate=2010-01-01T00:00:00Z&endDate=2020-01-01T00:00:00Z&data=sst',
#    '/timeseries/noaasst?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&batchmeta=true',
#    '/timeseries/noaasst?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&compression=minimal',
# ]

# routes_to_check = [
#    '/timeseries/copernicussla?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]',
#    '/timeseries/copernicussla?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&startDate=2010-01-01T00:00:00Z&endDate=2020-01-01T00:00:00Z',
#    '/timeseries/copernicussla?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&startDate=2010-01-01T00:00:00Z&endDate=2020-01-01T00:00:00Z&data=all',
#    '/timeseries/copernicussla?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&startDate=2010-01-01T00:00:00Z&endDate=2020-01-01T00:00:00Z&data=sla,adt',
#    '/timeseries/copernicussla?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&batchmeta=true',
#    '/timeseries/copernicussla?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&compression=minimal',
# ]

# routes_to_check = [
#    '/timeseries/ccmpwind?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]',
#    '/timeseries/ccmpwind?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&startDate=2010-01-01T00:00:00Z&endDate=2020-01-01T00:00:00Z',
#    '/timeseries/ccmpwind?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&startDate=2010-01-01T00:00:00Z&endDate=2020-01-01T00:00:00Z&data=all',
#    '/timeseries/ccmpwind?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&startDate=2010-01-01T00:00:00Z&endDate=2020-01-01T00:00:00Z&data=uwnd,vwnd',
#    '/timeseries/ccmpwind?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&batchmeta=true',
#    '/timeseries/ccmpwind?polygon=[[-92,27],[-92,22],[-87,22],[-87,27],[-92,27]]&compression=minimal',
# ]

for route in routes_to_check:
    blob = smoke_test(API, APIX, TOKEN, route)

