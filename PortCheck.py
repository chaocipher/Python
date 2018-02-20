import socket
import argparse


# Parser structure
varArgParser = argparse.ArgumentParser()
varArgParser.add_argument("--T", help="Target IP address.")
varArgParser.add_argument("--P", help="Target Port to check")
varArgParser.add_argument("--PRange", help="Target range of ports to check. Ex. '20-443'")
varArgs = varArgParser.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


if varArgs.PRange:
    # Grab the starting port number in the range.
    varPRTRangeStart = int(varArgs.PRange[:varArgs.PRange.find('-')])

    # Ending range: +1 inside the find to clear the '-' character and +1 outside to make it inclusive for the user.
    varPRTRangeStop = int(varArgs.PRange[varArgs.PRange.find('-')+1:]) + 1

    for varPRT in range(varPRTRangeStart, varPRTRangeStop):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket.setdefaulttimeout(.1)
        result = sock.connect_ex((varArgs.T, int(varPRT)))

        if result == 0:
            print(f'{int(varPRT)} Port is open.')
            sock.shutdown(.1)
        else:
            print(f'{int(varPRT)} Port is not open.')


else:
    result = sock.connect_ex((varArgs.T, int(varArgs.P)))
    if result == 0:
        print(f'{int(varArgs.P)} Port is open.')
    else:
        print(f'{int(varArgs.P)} Port is not open.')




