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

from gem5.components.processors.cpu_types import *
from gem5.components.memory import *

from http.server import BaseHTTPRequestHandler, HTTPServer
import inspect, json

MemTypes = {name:obj for name,obj in inspect.getmembers(dram_interfaces, inspect.ismodule)}
newline_str = '\n'
newline_bytes = newline_str.encode('utf-8')

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

#=============================================================#

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__m5_main__':
    run_server()