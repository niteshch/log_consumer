"""
send_email example implementation. feel free to replace this with your own
"""

from datetime import datetime
GLOBAL_TOTAL = 0

def send_email(msg):

    """
    stand-in for an emailer, this one just prints to console
    with some info about when the message was made public
    """

    global GLOBAL_TOTAL
    GLOBAL_TOTAL += 1

    print("""\
#####################################################
##                 SERVER ALERT                    ##
##                                                 ##
## received: {date:%Y-%m-%d %H:%M:%S.%f}            ##
## total_alerts: {total:7d}                           ##
#####################################################
{msg}

""".format(
        date=datetime.now(),
        total=GLOBAL_TOTAL,
        msg=msg))