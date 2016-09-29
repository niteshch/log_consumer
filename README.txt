In this project, I have leveraged an existing utility - Logster by Etsy

The source of logster can be found at https://github.com/etsy/logster

Logster is a utility for reading log files and generating metrics to
configurable outputs. It is ideal for visualizing trends of events that
are occurring in your application/system/error logs. For example, you might use
logster to graph the number of occurrences of HTTP response code that appears in
your web server logs.

Logster maintains a cursor, via a tailer, on each log file that it reads so that
each successive execution only inspects new log entries.

This tool is made up of parsing classes that are written to accommodate your specific
log format. The parser classes essentially read a log file line by line, apply a regular
expression to extract useful data from the lines you are interested in, and then
aggregate that data into metrics that will be submitted to the configured output.

I have added a bunch of utilities to the program to accomodate the requirements of the
problem statement. I added a new parser - ParameterizedLogParser which takes in a regular
expression as a parameter to process the log file in any input format. You can modify the
number of lines of logs to be received in mail by supplying -m option to the parser. Default is 100.

I added SendMailOutput class to call send mail using the send_mail utility provided at the root.
Additional flags were added and changes were made to the code in monitor.py file as per
the requirements.

## Pre-requisites

Logster supports two methods for gathering data from a logfile:

1. By default, Logster uses the "logtail" utility that can be obtained from the
   logcheck package, either from a Debian package manager or from source:

       http://packages.debian.org/source/sid/logcheck

   RPMs for logcheck can be found here:

       http://rpmfind.net/linux/rpm2html/search.php?query=logcheck

2. Optionally, Logster can use the "Pygtail" Python module instead of logtail.
   You can install Pygtail using pip

   ```
   $ pip install pygtail
   ```

   To use Pygtail, supply the ```--tailer=pygtail``` option on the Logster
   commandline.


## Usage

You can test monitor.py from the command line.

    $ python monitor.py --output=sendmail ParameterizedLogParser -l logster_log/ -s logster_state/ -t pygtail /var/log/test_log.log --parser-options "-l WARNING,ERROR,FATAL,INFO,DEBUG -r \[(?P<date>[0-9-_\-\.]+)\s(?P<time>[0-9-_:\.]+,\d{3})\]\[(?P<module>.*)\]\[(?P<log_level>WARNING|ERROR|FATAL|INFO|DEBUG)\]"

Additional usage details can be found with the -h option:

    $ python monitor.py -h
    Usage: monitor [options] parser logfile

    Tail a log file and filter each line to generate metrics that can be sent to
    common monitoring packages.

    Options:
      -h, --help            show this help message and exit
      -t TAILER, --tailer=TAILER
                            Specify which tailer to use. Options are logtail and
                            pygtail. Default is "logtail".
      --logtail=LOGTAIL     Specify location of logtail. Default
                            "/usr/sbin/logtail2"
      -p METRIC_PREFIX, --metric-prefix=METRIC_PREFIX
                            Add prefix to all published metrics. This is for
                            people that may multiple instances of same service on
                            same host.
      -x METRIC_SUFFIX, --metric-suffix=METRIC_SUFFIX
                            Add suffix to all published metrics. This is for
                            people that may add suffix at the end of their
                            metrics.
      --parser-help         Print usage and options for the selected parser
      --parser-options=PARSER_OPTIONS
                            Options to pass to the logster parser such as "-o
                            VALUE --option2 VALUE". These are parser-specific and
                            passed directly to the parser.
      -s STATE_DIR, --state-dir=STATE_DIR
                            Where to store the tailer state file.  Default
                            location /var/run
      -l LOG_DIR, --log-dir=LOG_DIR
                            Where to store the logster logfile.  Default location
                            /var/log/logster
      --log-conf=LOG_CONF   Logging configuration file. None by default
      -o OUTPUT, --output=OUTPUT
                            Where to send metrics (can specify multiple times).
                            Choices are statsd, stdout, cloudwatch, graphite,
                            ganglia, nsca or a fully qualified Python class name
      -d, --dry-run         Parse the log file but send stats to standard output.
      -D, --debug           Provide more verbose logging for debugging.
      -e EVENT, --log-event-string=EVENT
                        Event on which we call output (Print stdout or send
                        mail). Default is "ERROR"


ParameterizedLogParser
    Options:
      -m LINES_COUNT, --max-length=LINES_COUNT
                             Number of historic lines to keep track of when tailing the log
      -l LEVELS, --log-levels=LEVELS
                             Comma-separated list of log levels to track: (default: "WARNING,ERROR,FATAL")
      -r REGEX,  --log-regex=REGEX
                             RegEx for reading log file events:
                             (default: "\[(?P<date>[0-9-_\-\.]+) (?P<time>[0-9-_:\.]+,\d{3})\]\[(?P<module>.*)\]\[(?P<log_level>WARNING|ERROR|FATAL)\]")




