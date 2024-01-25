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

#!/bin/bash

GEM5_PATH=$(pwd)/../../../../build/ARM/gem5.opt
GEM5_API_PATH=$(pwd)/api/obtain-api.py
FRONTEND_PATH=$(pwd)/frontend/frontend.py

$GEM5_PATH $GEM5_API_PATH &
sleep 2
python3 $FRONTEND_PATH