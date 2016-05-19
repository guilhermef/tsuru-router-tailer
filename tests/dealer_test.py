import unittest
import unittest.mock as mock
from preggy import expect

from tsuru_router_tailer.dealer import Dealer

LINE = '::ffff:10.0.0.96 - - [19/May/2016:23:26:25 +0000] "POST / HTTP/1.1" 200 13 "http://google.com" "Mozilla/5.0" ":" "app.tsuru.com" 0.012 0.012'
LOG_JSON = {
    'path': '/',
    'client': 'tsuru',
    'method': 'POST',
    'metric': 'response_time',
    'value': 0.012,
    'app': 'app',
    'status_code': '200'
}


class TestDealer(unittest.TestCase):

    def setUp(self):
        self.dealer = Dealer()

    def test_generate_json(self):
        expect(self.dealer.do_line(LINE)).\
            to_be_like(LOG_JSON)

    @mock.patch.object(Dealer, 'send_to_logstash')
    def test_send_to_logstash_on_line(self, send_to_mock):
        self.dealer.pipe_data_received(LINE)
        send_to_mock.assert_called_once_with(LOG_JSON)

    @mock.patch.object(Dealer, 'send_to_logstash')
    def test_should_ignore_tail_warning(self, send_to_mock):
        self.dealer.pipe_data_received(
            'tail: \'some_file.log.1\' has become inaccessible: No such file or directory'
        )
        send_to_mock.assert_not_called()
