.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
		
test-coverage: ## Running test coverage for the project
	@poetry update
	@poetry install
	@poetry run coverage run -m pytest tests/ -vv
	@poetry run coverage report -m
	@poetry run coverage html

build: test-coverage ## Buidling the layer [gateways layer in this case]
	@poetry install
	@poetry update
	@poetry build