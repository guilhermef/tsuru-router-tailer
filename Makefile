setup:
	@pip install -e .[tests]

unit:
	@coverage run --branch `which nosetests` -v --with-yanc -s tests/

static flake8:
	@flake8 tsuru_router_tailer/
	@flake8 tests/

focus:
	@coverage run --branch `which nosetests` -vv --with-yanc --logging-level=WARNING --with-focus -i -s tests/
