.PHONY: style code-style

style:	code-style docs-style shellcheck ## Perform all style checks

code-style: ## Check code style for all Python sources from this repository
	python3 tools/run_pycodestyle.py

ruff: ## Run Ruff linter
	ruff .

docs-style: ## Check documentation strings in all Python sources from this repository
	pydocstyle .

shellcheck: ## Run shellcheck
	./shellcheck.sh

help: ## Show this help screen
	@echo 'Usage: make <OPTIONS> ... <TARGETS>'
	@echo ''
	@echo 'Available targets are:'
	@echo ''
	@grep -E '^[ a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-35s\033[0m %s\n", $$1, $$2}'
	@echo ''
