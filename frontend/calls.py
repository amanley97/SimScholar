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

import requests, json    

opt = {
    'boards' : {
        'type' : [],
        'clk' : 0
    },
    'processor' : {
        'isa' : ['ISA.X86', 'ISA.ARM'], # TODO
        'type' : [],
        'ncores' : 0
    },
    'memory' : {
        'type' : [],
        'size' : 0
    },
    'cache' : {
        'type' : [],
        # 'l1d' : 0,
        # 'l1i' : 0
    }
}

def get_gem5_data():

    board_req = http_request("get-board-types", "GET")
    board_types = board_req.json() if board_req.status_code == 200 else ["NULL"]
    for key,value in board_types.items():
        opt['boards']['type'].append(key)
        for k_t, v_t in value.items():
            if isinstance(v_t, dict):
                for k_t2, v_t2 in v_t.items():
                    if k_t2 not in opt['cache']['type']:
                        opt['cache']['type'].append(k_t2)
                    # TODO for Alex
                        for i in v_t2:
                            if i.endswith('_size'):
                                opt['cache'][i] = 0
    cpu_req = http_request("get-cpu-types", "GET")
    cpu_types = cpu_req.json() if cpu_req.status_code == 200 else ["NULL"]
    for items in cpu_types:
        opt['processor']['type'].append(items)

    cache_req = http_request("get-cache-types", "GET")
    cache_types = cache_req.json() if cache_req.status_code == 200 else ["NULL"]

    mem_req = http_request("get-mem-types", "GET")
    mem_types_o = mem_req.json() if mem_req.status_code == 200 else ["NULL"]
    # mem_types = []
    # for mem_type, mem_configs in mem_types_o.items():
    #     for type in mem_configs:
    #       mem_types.append(type)
    opt['memory']['type'] = mem_types_o
    # return [board_types, cpu_types]
    return [opt]

def http_request(api_endpoint, request_type, data=None):
    """
    Handles HTTP requests based on the provided endpoint and request type.

    Parameters:
    - api_endpoint (str): The API endpoint URL.
    - request_type (str): The HTTP request type (e.g., 'GET', 'PUT', 'POST').
    - data (dict, optional): Data to be included in the request body (for 'PUT' or 'POST').

    Returns:
    - response (requests.Response): The response object from the HTTP request.
    """
    headers = {"Content-Type": "application/json"}
    full_url = f"http://localhost:5000/{api_endpoint}"

    try:
        if request_type.upper() == 'GET':
            response = requests.get(full_url, headers=headers)
        elif request_type.upper() == 'PUT':
            response = requests.put(full_url, data=json.dumps(data), headers=headers)
        elif request_type.upper() == 'POST':
            response = requests.post(full_url, data=json.dumps(data), headers=headers)
        else:
            raise ValueError("Invalid request type. Supported types are 'GET', 'PUT', and 'POST'.")
        print(f"Request {request_type} for {api_endpoint} successful.")
        return response
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return response

def run_simulation(output_location):
    output = http_request("run-simulation", "PUT")
    output_location.config(text=str(output.text))

def exit(root, debug=None):
    http_request("shutdown", "PUT")
    root.destroy()
    if debug != None:
        debug.destroy()

def print_selected(list, label):
    result_dict = {}
    for label, stringvar in zip(label, list):
        value = stringvar.get()
        result_dict[label] = value
    data_test = http_request("user-data", "PUT", result_dict)
    print(data_test.text)