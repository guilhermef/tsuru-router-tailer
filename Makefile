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

test: unit static

run:
	@tsuru-router-tailer --log 'some_file.log' --logstash 'localhost:420'
