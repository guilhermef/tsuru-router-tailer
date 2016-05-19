import asyncio
import shlex

import tsuru_router_tailer.dealer


class Runner(object):
    def __init__(self, log_path, logstash):
        self.log_path = log_path
        self.logstash = logstash

    def run(self):
        @asyncio.coroutine
        def setup():
            loop = asyncio.get_event_loop()
            transport, protocol = yield from loop.subprocess_shell(
                tsuru_router_tailer.dealer.Dealer,
                'tail -n0 -F -q {}'.format(shlex.quote(self.log_path)),
                log_path=self.log_path,
                logstash=self.logstash
            )
            yield from protocol.complete

        asyncio.get_event_loop().run_until_complete(setup())
