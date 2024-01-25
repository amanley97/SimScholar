# ----------------------------------------------------------------------------
# NOTICE: This code is the exclusive property of University of Kansas
#         Architecture Research and is strictly confidential.
#
#         Unauthorized distribution, reproduction, or use of this code, in
#         whole or in part, is strictly prohibited. This includes, but is
#         not limited to, any form of public or private distribution,
#         publication, or replication.
#
# For inquiries or access requests, please contact:
#         Alex Manley (amanley97@ku.edu)
#         Mahmudul Hasan (m.hasan@ku.edu)
# ----------------------------------------------------------------------------

import requests

def simulate_action():
    try:
        response = requests.put('http://127.0.0.1:5000/run-simulation')

    # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Request successful")
            return (response)
        else:
            return (f"Request failed with status code: {response.status_code}")

    except requests.RequestException as e:
        # Handle exceptions related to the request (e.g., connection error, timeout)
        print(f"Request failed: {e}")
        return (f"Request failed: {e}")
    except Exception as e:
        # Handle other unexpected exceptions
        print(f"An unexpected error occurred: {e}")
        return (f"An unexpected error occurred: {e}")
    

def get_gem5_data():

    # response0 = requests.get('http://127.0.0.1:5000/get-board-types')
    # board_types = response0.json() if response0.status_code == 200 else None
    board_types = ['simple']

    response1 = requests.get('http://127.0.0.1:5000/get-cpu-types')
    cpu_types = response1.json() if response1.status_code == 200 else None

    # response2 = requests.get('http://127.0.0.1:5000/get-cache-types')
    # cache_types = response2.json() if response2.status_code == 200 else None
    cache_types = ['No Cache']

    response3 = requests.get('http://127.0.0.1:5000/get-mem-types')
    mem_types_o = response3.json() if response3.status_code == 200 else None
    mem_types = []
    for mem_type, mem_configs in mem_types_o.items():
        for type in mem_configs:
          mem_types.append(mem_type+": "+type)

    return [board_types, cpu_types, cache_types, mem_types]

def exit_server():
    try:
        response = requests.put('http://127.0.0.1:5000/shutdown')

    # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Request successful")
            return (response)
        else:
            return (f"Request failed with status code: {response.status_code}")
    except requests.RequestException as e:
        # Handle exceptions related to the request (e.g., connection error, timeout)
        print(f"Request failed: {e}")
        return (f"Request failed: {e}")
    except Exception as e:
        # Handle other unexpected exceptions
        print(f"An unexpected error occurred: {e}")
        return (f"An unexpected error occurred: {e}")