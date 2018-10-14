import subprocess
import shlex


def RateSentiment(sentiString):
    # open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar C:/Users/User/SentiStrength/SentiStrength.jar stdin sentidata "
                                     "C:/Users/User/SentiStrength/SentiStrength_Data/"),
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # communicate via stdin the string to be rated. Note that all spaces are replaced with +
    # can't send string in Python 3, must send bytes
    b = bytes(sentiString.replace(" ", "+"), 'utf-8')
    stdout_byte, stderr_text = p.communicate(b)

    # convert from byte
    stdout_text = stdout_byte.decode("utf-8")

    # replace the tab with a space between the positive and negative ratings. e.g. 1    -5 -> 1 -5
    stdout_text = stdout_text.rstrip().replace("\t", " ")

    # split results
    stdout_text = stdout_text.splitlines()
    for item in stdout_text:
        results = item.split(" ")
        positive = int(results[0])
        negative = int(results[1])

    return positive, negative


pos, neg = RateSentiment("niiice ")
print(pos)
print(neg)
