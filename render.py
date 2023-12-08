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

from jinja2 import Environment, FileSystemLoader
from obtain import *

board_types = ["simple"]
cpu_types = get_cpu_types()
mem_types = get_mem_types()
cache_types = ["no cache"]
template_dir = "/home/a599m019/Projects/gem5/configs/example/gem5_library/gui/templates/" # Update with your template folder absolute path

environment = Environment(loader=FileSystemLoader(template_dir))
template = environment.get_template("options.html")

filename = f"{template_dir}output.html"
content = template.render(
                            board_types=board_types,
                            cpu_types=cpu_types,
                            mem_types=mem_types,
                            cache_types=cache_types
                        )
with open(filename, mode="w", encoding="utf-8") as message:
    message.write(content)
    print("DONE")