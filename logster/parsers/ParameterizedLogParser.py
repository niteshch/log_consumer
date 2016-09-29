#  Author: Nitesh Chauhan <nc2663@columbia.edu>
#
#  A sample logster parser file that can be used to parse the
#  logs with a specific format. The format can be provided to
#  the parser as a parameter in form of RegEx.
#
#  Example:
#  python logster.py --output=stdout ParameterizedLogParser /var/log/example_app/app.log --parser-options "-l WARN,ERROR,FATAL -r \[(?P<date>[0-9-_\-\.]+)\s(?P<time>[0-9-_:\.]+,\d{3})\]\[(?P<module>.*)\]\[(?P<log_level>WARN|ERROR|FATAL)\]"
#
# Note:
#     - WARN,ERROR,FATAL is default log level tracked
#     - \[(?P<date>[0-9-_\-\.]+)\s(?P<time>[0-9-_:\.]+,\d{3})\]\[(?P<module>.*)\]\[(?P<log_level>WARNING|ERROR|FATAL)\]
#        is the default regular expression
#

import time
import re
import optparse

import collections

from logster.logster_helper import MetricObject, LogsterParser
from logster.logster_helper import LogsterParsingException

class ParameterizedLogParser(LogsterParser):
    
    def __init__(self, option_string=None):
        '''Initialize any data structures or variables needed for keeping track
        of the tasty bits we find in the log we are parsing.'''
        
        if option_string:
            options = option_string.split(' ')
        else:
            options = []
        
        optparser = optparse.OptionParser()
        optparser.add_option('--max-length', '-m', dest='history_maxlen', type="int", default=100,
                             help='Number of historic lines to keep track of when tailing the log')
        optparser.add_option('--log-levels', '-l', dest='levels', default='WARNING,ERROR,FATAL',
                            help='Comma-separated list of log levels to track: (default: "ERROR")')
        optparser.add_option('--log-regex', '-r', dest='regex', action="store", default='\[(?P<date>[0-9-_\-\.]+) (?P<time>[0-9-_:\.]+,\d{3})\]\[(?P<module>.*)\]\[(?P<log_level>%s)\]' % ('|'.join(['WARN', 'ERROR', 'FATAL'])),
                            help='RegEx for reading log file events: (default: "\[(?P<date>[0-9-_\-\.]+) (?P<time>[0-9-_:\.]+,\d{3})\]\[(?P<module>.*)\]\[(?P<log_level>WARNING|ERROR|FATAL)\]")')
        
        opts, args = optparser.parse_args(args=options)

        self.levels = opts.levels.split(',')
        self.regex = opts.regex
        self.log_history = collections.deque(maxlen=opts.history_maxlen)
        self.is_event = False

        for level in self.levels:
            # Track counts from 0 for each log level
            setattr(self, level, 0)
        
        # Regular expression for matching lines we are interested in, and capturing
        # fields from the line (in this case, a log level such as WARN, ERROR, or FATAL).
        self.reg = re.compile(self.regex)

    def parse_line(self, line):
        '''This function should digest the contents of one line at a time, updating
        object's state variables. Takes a single argument, the line to be parsed.'''
        self.log_history.append(line)
        try:
            # Apply regular expression to each line and extract interesting bits.
            regMatch = self.reg.match(line)
            if regMatch:
                linebits = regMatch.groupdict()
                log_level = linebits['log_level']
                if 'ERROR' in log_level:
                    self.is_event = True
                if log_level in self.levels:
                    current_val = getattr(self, log_level)
                    setattr(self, log_level, current_val+1)
            else:
                raise LogsterParsingException("regmatch failed to match")
                
        except Exception as e:
            raise LogsterParsingException("regmatch or contents failed with %s" % e)
            
            
    def get_state(self, duration):
        '''Run any necessary calculations on the data collected from the logs
        and return a list of metric objects.'''
        self.duration = float(duration)
        
        metrics = [MetricObject(level, (getattr(self, level))) for level in self.levels]
        return metrics

    def get_log_history(self):
        return self.log_history
