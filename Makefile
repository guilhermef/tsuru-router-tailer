setup:
	@pip install -e .[tests]

coverage:
	@coverage report -m --fail-under=10

unit:
	@coverage run --branch `which nosetests` -v --with-yanc -s tests/
	@$(MAKE) coverage

static flake8:
	@flake8 tsuru_router_tailer/
	@flake8 tests/

focus:
	@coverage run --branch `which nosetests` -vv --with-yanc --logging-level=WARNING --with-focus -i -s tests/

test: redis unit static

run:
	@tsuru-router-tailer --logstash 'localhost:420' 'some_file.log'

kill_redis:
	@-redis-cli 'SHUTDOWN'

redis: kill_redis
	@redis-server redis.conf; sleep 1
