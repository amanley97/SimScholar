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

import threading, os, signal
from gem5.components.processors.cpu_types import *
from gem5.components.memory import *
from gem5.components import *
from gem5.simulate.simulator import Simulator

# Test using simple ARM
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.processors.simple_processor import SimpleProcessor


from http.server import BaseHTTPRequestHandler, HTTPServer
import inspect, json

MemTypes = {name:obj for name,obj in inspect.getmembers(dram_interfaces, inspect.ismodule)}
# Global flag to control server shutdown
shutdown_flag = False

def get_cls(file, mask):
    cls = []
    for name, obj in inspect.getmembers(file):
        if inspect.isclass(obj) and name != mask:
            cls.append(name)
    return cls

def get_mem_types():
    mem_types = {}
    for name, idx in MemTypes.items():
        mem_types.update({name : get_cls(idx, 'DRAMInterface')})
    mem_types_b = json.dumps(mem_types, indent=2).encode('utf-8')
    return mem_types_b

def get_cpu_types():
    cpu_types = list(get_cpu_types_str_set())
    cpu_types_b = json.dumps(cpu_types, indent=2).encode('utf-8')
    return cpu_types_b

#=============================================================#

class SimpleHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/get-mem-types':
            self.handle_mem_types()
        elif self.path == '/get-cpu-types':
            self.handle_cpu_types()
        else:
            self.send_error(404, 'Not Found')

    def do_PUT(self):
        if self.path == '/run-simulation':
            self.handle_run_simulator()
        elif self.path == '/shutdown':
            self.handle_shutdown()
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

    def handle_run_simulator(self):
        simulator_thread = threading.Thread(target=run_gem5_simulator())
        simulator_thread.start()

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Simulator started in a separate thread\n")

    def handle_shutdown(self):
        global shutdown_flag
        shutdown_flag = True  # Set the global flag to initiate shutdown

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Shutting down server\n")

#=============================================================#

def run_server(port=5000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHandler)

    # Run the server in a separate thread
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()

    print(f'Starting server on port {port}...')

    # Keep the main thread busy (e.g., waiting for user input)
    while not shutdown_flag:
        pass

    # Close the server's socket explicitly before initiating shutdown
    print("Closing server socket...")
    httpd.server_close()

    # Initiate graceful shutdown
    print("Shutting down server...")
    httpd.shutdown()
    server_thread.join()  # Wait for the server thread to finish

def run_gem5_simulator():
        simulator = Simulator(board=board)
        simulator.run()

board = SimpleBoard(
    clk_freq="3GHz",
    processor=SimpleProcessor(cpu_type=CPUTypes.TIMING, isa=ISA.ARM, num_cores=1),
    memory=SingleChannelDDR3_1600(size="32MB"),
    cache_hierarchy=NoCache()
)
board.set_se_binary_workload(
    obtain_resource("arm-hello64-static")
)

if __name__ == '__m5_main__':
    run_server()
    