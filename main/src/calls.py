import json
from xmlrpc.client import ServerProxy
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
        self.proxy = ServerProxy(f"http://localhost:{self.port}")

    def get_gem5_data(self):
        self.parse_data(json.loads(self.proxy.get_config_options()))
        return self.data

    def parse_data(self, data):
        for key, value in data.items():
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

    def configure_simulation(self, usr_config, resource, id):
        printdebug("[calls] Configuration sent to gem5")
        messages = []

        messages.append(json.loads(self.proxy.add_config(id)))

        messages.append(json.loads(self.proxy.set_board(
            id, 
            usr_config['board']['type'], 
            usr_config['board']['clk']
        )))

        messages.append(json.loads(self.proxy.set_processor(
            id, 
            usr_config['processor']['isa'], 
            usr_config['processor']['type'],
            usr_config['processor']['cpu'],
            usr_config['processor']['ncores']
        )))

        messages.append(json.loads(self.proxy.set_memory(
            id, 
            usr_config['memory']['type'], 
            usr_config['memory']['size']
        )))

        messages.append(json.loads(self.proxy.set_cache(
            id,
            usr_config['cache']['type'],
            usr_config['cache']['l1d_size'], 
            usr_config['cache']['l1i_size'], 
            usr_config['cache']['l2_size'], 
            usr_config['cache']['l1d_assoc'], 
            usr_config['cache']['l1i_assoc'], 
            usr_config['cache']['l2_assoc']
        )))

        messages.append(json.loads(self.proxy.set_resource(
            id, 
            resource[1]
        )))
        print(messages)
    

    def shutdown(self):
        printdebug("[calls] shutting down backend")
        response = json.loads(self.proxy.shutdown())
        return response

    def view_saved(self, render_box):
        printdebug("[calls] viewing saved configs.")
        saved = json.loads(self.proxy.get_configs())
        render_box.configure(state="normal")
        render_box.delete("1.0", "end")
        render_box.insert("1.0", json.dumps(saved))
        render_box.configure(state="disabled")

    def run_simulation(self, id):
        printdebug("[calls] running the simulation!")
        output = json.loads(self.proxy.run_simulation(id))
        print(output)

        sim = json.loads(self.proxy.get_sims())
        self.stats.update_path(sim[-1]['path'])

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


if __name__ == "__main__":
    myobj = SimScholarCalls(stats_handler=None, port=8080, path='/home/a599m019/Projects/Current/SimScholar/gem5')
    myobj.get_gem5_data()

    print(myobj.data)
