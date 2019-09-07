.PHONY: generate
build:
	mkdir -p protos
	# Points to the latest tested proto
	wget https://raw.githubusercontent.com/liftbridge-io/liftbridge-grpc/0877a0cacb7a721e2e19280cff126dc2ed51912d/api.proto -O protos/api.proto
	python -m grpc_tools.protoc -I. --python_out=python_liftbridge/ --grpc_python_out=python_liftbridge/ protos/api.proto
	mv python_liftbridge/protos/* python_liftbridge/.
	rmdir python_liftbridge/protos

.PHONY: clean
clean:
	find -name '*.pyc' -delete
	find -name '__pycache__' -delete

.PHONY: install-hooks
install-hooks:
	tox -e pre-commit -- install -f --install-hooks

.PHONY: publish
publish:
	rm -fr build dist .egg python_liftbridge.egg-info
	pip install wheel twine
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg python_liftbridge.egg-info

.PHONY: super-clean
super-clean:
	rm -rf .tox
	rm -rf venv
	pyenv local --unset

.PHONY: run-liftbridge
run-liftbridge:
	docker pull dgzlopes/liftbridge-docker
	docker run -d --name=liftbridge-main -p 4222:4222 -p 9292:9292 -p 8222:8222 -p 6222:6222 dgzlopes/liftbridge-docker

.PHONY: pub
pub:
	python examples/lift-pub.py $(RUN_ARGS) -d

.PHONY: sub
sub:
	python examples/lift-sub.py $(RUN_ARGS) -c -d

# If the first argument is "pub"...
ifeq (pub,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "pub"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

# If the first argument is "sub"...
ifeq (sub,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "sub"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
