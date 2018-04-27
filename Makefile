.DEFAULT_GOAL := help

# Generates a help message. Borrowed from https://github.com/pydanny/cookiecutter-djangopackage.
help: ## Display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@perl -nle'print $& if m{^[\.a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

stubs: ## Generate gRPC stubs
	python -m grpc.tools.protoc -I/usr/local/include -I. --python_out=./ --grpc_python_out=./ service.proto

insecure_client: ## Run client insecure
	python insecure_client.py

insecure_server: ## Run server insecure
	python insecure_server.py

secure_client: ## Run client secure
	python secure_client.py

secure_server: ## Run server secure
	python secure_server.py

secure_client_nginx: ## Run client secure with nginx (>=1.13) grpc upstreams
	python secure_client.py

gen_key: ## Generate certificate for the server. Uses openssl.
	openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt
