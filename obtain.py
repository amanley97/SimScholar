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

import inspect

MemTypes = {name:obj for name,obj in inspect.getmembers(dram_interfaces, inspect.ismodule)}

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
    return mem_types

def get_cpu_types():
    return get_cpu_types_str_set()

# print("CPU TYPES: ", get_cpu_types())
# print("MEM TYPES: ", get_mem_types())
