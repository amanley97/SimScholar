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

import re
from colorama import Fore, init

init(autoreset=True)


def printdebug(message, color="cyan"):
    if color == "green":
        pcolor = Fore.LIGHTGREEN_EX
    elif color == "red":
        pcolor = Fore.LIGHTRED_EX
    else:
        pcolor = Fore.LIGHTCYAN_EX

    pattern = r"\[(.*?)\]"
    last_end = 0
    for match in re.finditer(pattern, message):
        print(Fore.LIGHTWHITE_EX + message[last_end : match.start()], end="")
        print(pcolor + match.group(0), end="")
        last_end = match.end()

    print(Fore.LIGHTWHITE_EX + message[last_end:])


# Example usage
# printdebug("[in cyan] white text", color='cyan')
