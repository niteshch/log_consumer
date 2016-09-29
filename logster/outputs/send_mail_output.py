from logster.logster_helper import LogsterOutput
from send_mail import send_email


class SendMailOutput(LogsterOutput):
    shortname = 'sendmail'

    def __init__(self, parser, options, logger):
        super(SendMailOutput, self).__init__(parser, options, logger)

    def submit(self, msg):
        send_email(msg)