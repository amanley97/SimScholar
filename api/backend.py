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
import copy
import os, multiprocessing, sys
from gem5.components.processors.cpu_types import *
from gem5.components.memory import *
from gem5.components import *
from gem5.simulate.simulator import Simulator

from m5.stats import *
# Test using simple ARM
from gem5.isas import ISA
from gem5.resources.resource import *
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.memory import single_channel
from gem5.components.memory import multi_channel
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.cachehierarchies.classic.caches.l1icache import L1ICache
from gem5.components.cachehierarchies.classic.caches.l1dcache import L1DCache
from gem5.components.cachehierarchies.classic.caches.l2cache import L2Cache
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import PrivateL1SharedL2CacheHierarchy
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import PrivateL1PrivateL2CacheHierarchy
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import PrivateL1CacheHierarchy

from gem5.components.processors.simple_processor import SimpleProcessor
#
from http.server import BaseHTTPRequestHandler, HTTPServer
import inspect, json

MemTypes = {name:obj for name,obj in inspect.getmembers(dram_interfaces, inspect.ismodule)}
#MemTypes = {name:obj for name,obj in inspect.getmembers(dram_interfaces, inspect.ismodule)}
def collect_memory_functions(module):
    function_names = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            function_names.append(name)
    return function_names

# Collecting functions from both modules
single_channel_memory = collect_memory_functions(single_channel)
multi_channel_memory = collect_memory_functions(multi_channel)
def get_init_parameters(*classes):
    class_params_dict = {}
    for cls in classes:
        init_signature = inspect.signature(cls.__init__)
        parameters = list(init_signature.parameters.keys())
        # Filter out 'self' and any other non-attribute parameters you don't want
        filtered_parameters = [param for param in parameters if param not in ['self', 'cls', '*args', '**kwargs']]
        class_params_dict[cls.__name__] = filtered_parameters
    return class_params_dict

def get_cls(file, mask):
    cls = []
    for name, obj in inspect.getmembers(file):
        if inspect.isclass(obj) and name != mask:
            cls.append(name)
    return cls

def get_board_types():
    cache_types = ['NoCache', 'PrivateL1SharedL2CacheHierarchy','PrivateL1PrivateL2CacheHierarchy', 'PrivateL1CacheHierarchy'] # TODO - get from gem5 automatically
    cache_class_objects = [globals()[class_name] for class_name in cache_types]
    # List of the classes we want to inspect
    classes_to_inspect = [SimpleBoard, X86Board, SimpleProcessor, *cache_class_objects]
    # Get the dictionary of class names and their init parameters
    board_info = get_init_parameters(*classes_to_inspect)
    for board in ['SimpleBoard', 'X86Board']:
        processor_info = board_info['SimpleProcessor']
        cache_hierarchy_info = {k: board_info[k] for k in cache_types}
        board_info[board] = {
            'clk_freq': [board_info[board][0]],  # Assuming clk_freq is a string and not another key
            'Memory': [board_info[board][2], "size"],  # Assuming memory is a string and not another key
            'Processor': processor_info,
            'Cache Hierarchy': cache_hierarchy_info
        }
    # Remove extra items from the dictionary
    for key in ['SimpleProcessor', *cache_types]:
        board_info.pop(key, None)

    board_types = {}
    for name, idx in board_info.items():
        # print(name, idx)
        board_types.update({name : idx})
    board_types_b = json.dumps(board_types, indent=2).encode('utf-8')
    return board_types_b

def get_mem_types():
    # mem_types = {}
    # for name, idx in MemTypes.items():
    #     mem_types.update({name : get_cls(idx, 'DRAMInterface')})
    mem_types = single_channel_memory + multi_channel_memory
    mem_types_b = json.dumps(mem_types, indent=2).encode('utf-8')
    # print("MTB", mem_types_b)
    return mem_types_b

def get_cpu_types():
    cpu_types = list(get_cpu_types_str_set())
    cpu_types_b = json.dumps(cpu_types, indent=2).encode('utf-8')
    return cpu_types_b
boardd = None
#=============================================================#
class SimpleHandler(BaseHTTPRequestHandler):
    user_data_storage = {}

    def do_GET(self):
        if self.path == '/get-mem-types':
            self.handle_mem_types()
        elif self.path == '/get-cpu-types':
            self.handle_cpu_types()
        elif self.path == '/get-board-types':
            self.handle_board_types()
        else:
            self.send_error(404, 'Not Found')

    def do_PUT(self):
        if self.path == '/run-simulation':
            self.handle_run_simulator()
        elif self.path == '/shutdown':
            self.handle_shutdown()
        elif self.path == '/user-data':
            self.handle_user_data()
        else:
            self.send_error(404, 'Not Found')

    def handle_mem_types(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(get_mem_types())

    def handle_cpu_types(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(get_cpu_types())

    def handle_board_types(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(get_board_types())

    def handle_run_simulator(self):
        process = multiprocessing.Process(target=run_gem5_simulator)
        # process = multiprocessing.Process(target=run_gem5_simulator, args=(boardd,))
        process.start()
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Simulator started in a separate thread\n")
        # process.terminate()
        process.join()

        self.wfile.write(b"Simulation Complete\n")
    def handle_parse_simulation_output(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write()

    def handle_shutdown(self):
        # TODO: Ensure the backend server and port are closed

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Shutting down server\n")

    def get_user_data(cls, user_id):
        # Method to retrieve data for a given user
        return cls.user_data_storage.get(user_id)
    def handle_user_data(self):
        try:
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            received_data = json.loads(data.decode('utf-8'))

            user_id = 'default'
            SimpleHandler.user_data_storage[user_id] = received_data
            # print("RESPONSE => ", SimpleHandler.user_data_storage.get(user_id))
            self.send_response(200)

        except Exception as e:
            # Handle any exceptions that might occur during processing
            print(f"Error processing PUT request: {e}")
            self.send_response(500, {"error": "Internal Server Error"})

        self.end_headers()
        self.wfile.write(b"Successfully configured gem5. Ready to Simulate!")

#=============================================================#

def run_server(port=5000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHandler)

    print(f'Starting server on port {port}...')
    httpd.serve_forever()

def run_gem5_simulator():
    with open("./m5out/stats.txt", 'r+') as file:
        file.seek(0)
        file.truncate()

    with open('m5out/output.txt', "w") as f:
        sys.stdout = f
        sys.stderr = f
        print("Simulation PID: ", os.getpid())
        user_id = 'default'
        data = SimpleHandler.user_data_storage.get(user_id)
        global boardd
        if boardd is None:
            boardd = generate_config(data)
        else:
            del boardd
            boardd = generate_config(data)
        simulator = Simulator(board=boardd)
        simulator.run()
        print(
        "Exiting @ tick {} because {}.".format(
            simulator.get_current_tick(), simulator.get_last_exit_event_cause()
            )
        )
        sys.stdout.flush()
        sys.stderr.flush()

    dump()
    reset()
    m5.statsreset()

def generate_config(board_info):
    brd = str(board_info['Board Configuration']['type'])
    clk = str(board_info['Board Configuration']['clk']) + "GHz"
    cpu = eval("CPUTypes." + str(board_info['Processor Configuration']['type']).upper())
    isa = eval(board_info['Processor Configuration']['isa'])
    ncores = int(board_info['Processor Configuration']['ncores'])
    mem = eval(board_info['Memory Configuration']['type'])
    msize = str(board_info['Memory Configuration']['size']) + "MB"
    cache_type = board_info['Cache Configuration']['type']
    cache = None
    cache_for_display = ""
    if cache_type == "NoCache":
        cache = eval(board_info['Cache Configuration']['type'] + "()")
        cache_for_display = board_info['Cache Configuration']['type']
    elif cache_type == "PrivateL1CacheHierarchy":
        cache = PrivateL1CacheHierarchy(
            l1d_size = str(board_info['Cache Configuration']['l1d_size']) + "KiB",
            l1i_size = str(board_info['Cache Configuration']['l1i_size']) + "KiB"
        )
        cache_for_display = str(board_info['Cache Configuration']['type']) + "\nL1d: " +str(board_info['Cache Configuration']['l1d_size']) + "KiB" + "\nL1i: " +str(board_info['Cache Configuration']['l1i_size']).replace(",","") + "KiB"
    elif cache_type == "PrivateL1SharedL2CacheHierarchy":
        cache = PrivateL1SharedL2CacheHierarchy(
            l1d_size=str(board_info['Cache Configuration']['l1d_size']) + "KiB",
            l1i_size=str(board_info['Cache Configuration']['l1i_size']) + "KiB",
            l2_size=str(board_info['Cache Configuration']['l2_size']) + "KiB",
            l1d_assoc = board_info['Cache Configuration']['l1d_assoc'],
            l1i_assoc = board_info['Cache Configuration']['l1i_assoc'],
            l2_assoc = board_info['Cache Configuration']['l2_assoc']
        )
        cache_for_display = str(board_info['Cache Configuration']['type']) + "\nL1d: " +str(board_info['Cache Configuration']['l1d_size']) + "KiB" + "\nL1i: " +str(board_info['Cache Configuration']['l1i_size']) + "KiB" + "\nL2: " +str(board_info['Cache Configuration']['l2_size']) + "KiB" + "\nL1d_assoc: " +str(board_info['Cache Configuration']['l1d_assoc']) + "\nL1i_assoc: " +str(board_info['Cache Configuration']['l1i_assoc']) + "\nL2_assoc: " +str(board_info['Cache Configuration']['l2_assoc']).replace(",","")
    elif cache_type == "PrivateL1PrivateL2CacheHierarchy":
        cache = PrivateL1PrivateL2CacheHierarchy(
            l1d_size = str(board_info['Cache Configuration']['l1d_size']) + "KiB",
            l1i_size = str(board_info['Cache Configuration']['l1i_size']) + "KiB",
            l2_size = str(board_info['Cache Configuration']['l2_size']) + "KiB"
        )
        cache_for_display = str(board_info['Cache Configuration']['type']) + "\nL1d: " +str(board_info['Cache Configuration']['l1d_size']) + "KiB" + "\nL1i: " +str(board_info['Cache Configuration']['l1i_size']) + "KiB" +  "\nL2: " +str(board_info['Cache Configuration']['l2_size']).replace(",","") + "KiB"

    rtype = board_info['resource'][0]
    resource = str(board_info['resource'][1])
    print("\n======CONFIGURATION======")

    print(f"Board: {brd}, \nClock Frequency: {clk}, \nCPU Type: {cpu}, \nISA: {isa}, \nNumber of Cores: {ncores}, \nMemory Type: {mem}, \nMemory Size: {msize}, \nCache Type: {cache_for_display}, \nUsing Resource: {resource}\n")

    #TODO: Add support for other board types

    configuration = SimpleBoard(
        clk_freq=clk,
        processor=SimpleProcessor(cpu_type=cpu, isa=isa, num_cores=ncores),
        memory=mem(size=msize),
        cache_hierarchy=cache
    )

    if rtype == 'default':
        configuration.set_se_binary_workload(
            obtain_resource(resource)
        )
    elif rtype == 'custom':
        configuration.set_se_binary_workload(
            BinaryResource(resource)
        )
    else:
        print("invalid resource")
    return configuration


if __name__ == '__m5_main__':
    run_server()
    