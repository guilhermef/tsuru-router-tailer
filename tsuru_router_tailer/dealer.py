import re


class Dealer(object):
    def __init__(self, logstash=None):
        self.logstash = logstash

    def connection_made(self, *args):
        pass

    def pipe_data_received(self, line, data=None):
        if line.startswith('tail: '):
            return
        result = self.do_line(line.rstrip())
        self.send_to_logstash(result)

    def send_to_logstash(self, log_json):
        pass

    def connection_lost(self, *args):
        pass

    def pipe_connection_lost(self, *args):
        pass

    def process_exited(self, *args):
        pass

    def do_line(self, line):
        tsuru_app = line.split(" ")[-3].replace('"', '').split('.')[0]
        value = line.split(" ")[-2]
        r = r'.* "(?P<method>\w+) (?P<path>.*) HTTP.*" (?P<status_code>\d{3}).*'
        info = re.search(r, line)
        return {
            "metric": "response_time",
            "client": "tsuru",
            "app": tsuru_app,
            "value": float(value),
            "path": info.groupdict()['path'],
            "method": info.groupdict()['method'],
            "status_code": info.groupdict()['status_code']
        }
