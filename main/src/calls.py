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
from main.utils.printdebug import printdebug


class SimScholarCalls:
    def __init__(self, stats_handler, port, path) -> None:
        self.port = port
        self.path = path
        self.data = None
        self.stats = stats_handler
        self.opt = {
            "boards": {"type": [], "clk": 3},
            "processor": {
                "isa": ["x86", "arm"],  # TODO
                "type": ["SimpleProcessor"],
                "cpu": [],
                "ncores": 1,
            },
            "memory": {"type": [], "size": 2048},
            "cache": {
                "type": [],
            },
        }

    def get_gem5_data(self):
        req = self.http_request("config/options", "GET")
        self.data = req.json() if req.status_code == 200 else ["NULL"]
        self.parse_data()

        return self.data

    def parse_data(self):
        for key, value in self.data.items():
            tmp_params = []
            self.opt["boards"]["type"].append(key)
            self.opt["processor"]["cpu"] = value["processor"]
            self.opt["memory"]["type"] = value["memory"]
            for cache_type, cache_val in value["cache_hierarchy"].items():
                if key == "SimpleBoard":
                    self.opt["cache"]["type"].append(cache_type)
                    if len(cache_val) > len(tmp_params):
                        tmp_params = cache_val
                    for item in tmp_params:
                        if item != "membus":
                            self.opt["cache"].update({item: 0})

    def http_request(self, api_endpoint, request_type, data=None):
        headers = {"Content-Type": "application/json"}
        full_url = f"http://localhost:{self.port}/{api_endpoint}"

        try:
            if request_type.upper() == "GET":
                response = requests.get(full_url, headers=headers)
            elif request_type.upper() == "PUT":
                response = requests.put(
                    full_url, data=json.dumps(data), headers=headers
                )
            elif request_type.upper() == "POST":
                response = requests.post(
                    full_url, data=json.dumps(data), headers=headers
                )
            else:
                raise ValueError(
                    "Invalid request type. Supported types are 'GET', 'PUT', and 'POST'."
                )
            printdebug(f"[calls] {request_type} for {api_endpoint} successful.")
            return response

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return response

    def configure_simulation(self, output_location, board_info, resource, id):
        printdebug("[calls] configuration sent to gem5")
        url = f"simulation/{id}/configure"
        board_info["resource"] = resource
        selected_opts = self.http_request(url, "PUT", board_info)
        output_location.config(text=str(selected_opts.text))

    def shutdown(self):
        printdebug("[calls] shutting down backend")
        url = f"shutdown"
        response = self.http_request(url, "PUT")
        return response

    def view_saved(self, text):
        printdebug("[calls] viewing saved configs.")
        url = f"simulation/saved"
        req = self.http_request(url, "GET")
        saved = req.json() if req.status_code == 200 else ["NULL"]
        text.configure(state="normal")
        text.delete("1.0", "end")
        text.insert("1.0", json.dumps(saved, indent=4))
        text.configure(state="disabled")

    def run_simulation(self, output_location, sim_out, stats_out, id):
        printdebug("[calls] running the simulation!")
        url = f"simulation/{id}/run"
        output = self.http_request(url, "PUT")
        out_id = str(output.text)
        output_location.config(text=out_id)
        self.display_sim_out(sim_out, stats_out, out_id)

    def display_sim_out(self, sim_out, stats_out, id):
        def parse_simulation_string(simulation_string):
            import re

            pattern = r"Starting simulation id: (\d+) using configuration id: (\d+)"
            match = re.search(pattern, simulation_string)

            if match:
                sim_id = match.group(1)
                config_id = match.group(2)
                return sim_id, config_id
            else:
                return None, None

        sim_id, cfg_id = parse_simulation_string(id)

        # UPDATE STATS
        self.stats.update_id(sim_id, cfg_id)
        # self.stats.parse_stats(stats_out)

        # UPDATE SIM OUT
        out_path = self.path + f"/m5out/config_{cfg_id}_sim_{sim_id}/output.txt"
        print(out_path)

        sim_out.configure(state="normal")
        with open(out_path, "r") as file:
            file_content = file.read()
            sim_out.delete("1.0", "end")
            sim_out.insert("1.0", file_content)
        sim_out.configure(state="disabled")
        return self.stats


# myobj = calls(8080)
# myobj.get_gem5_data()

# print(myobj.data)
