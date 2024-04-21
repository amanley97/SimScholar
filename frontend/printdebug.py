import re
from colorama import Fore, init
init(autoreset=True)

def printdebug(message, color='cyan'):
    if color == 'green':
        pcolor= Fore.LIGHTGREEN_EX
    elif color == 'red':
        pcolor = Fore.LIGHTRED_EX
    else:
        pcolor = Fore.LIGHTCYAN_EX

    pattern = r'\[(.*?)\]'
    last_end = 0
    for match in re.finditer(pattern, message):
        print(Fore.LIGHTWHITE_EX + message[last_end:match.start()], end='')
        print(pcolor + match.group(0), end='')
        last_end = match.end()
    
    print(Fore.LIGHTWHITE_EX + message[last_end:])

# Example usage
# printdebug("[in cyan] white text", color='cyan')
