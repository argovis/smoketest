import requests
import time

# Define the API endpoint
#API_ROOT = "https://argovis-apix-atoc-argovis-dev.apps.containers02.colorado.edu"
API_ROOT = "https://argovis-api.colorado.edu"

def smoke_test(API_ROOT, route):
    print("Testing", API_ROOT+route)

    # Step 1: Start the timer
    start_time = time.time()

    # Step 2: Send a GET request to the API
    try:
        response = requests.get(API_ROOT + route)
    except requests.exceptions.RequestException as e:
        print("    Request failed:", e)
        return

    # Step 3: Calculate the elapsed time
    elapsed_time = time.time() - start_time
    print(f"    Request took {elapsed_time:.2f} seconds")

    # Step 4: Check the response status code
    print(f"    Request returned status code {response.status_code}")

    # Step 5: Parse the response body as JSON and check specific fields
    try:
        response_json = response.json()
        return(response_json)        
    except ValueError:
        print("    Response is not valid JSON.")


blob = smoke_test(API_ROOT, '/argo?polygon=[[0,0],[0,5],[5,5],[5,0],[0,0]]')

