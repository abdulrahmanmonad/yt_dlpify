.PHONY: help

build-components = build-domain build-usecases build-gateways build-external-systems 

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
		
build-domain: ## Buidling the domain layer
	@cd domain && make build

build-usecases: ## Buidling the usecases layer
	@cd usecases && make build

build-gateways: ## Buidling the gateways layer
	@cd gateways && make build

build-external-systems: ## Buidling the external-systems layer
	@cd external_systems && make build

build-all: $(build-components) ## Buidling the project layers
	@echo "Building the project !"