.PHONY: style code-style

style:	code-style docs-style shellcheck ## Perform all style checks

ruff: ## Run Ruff linter
	pre-commit run --all-files ruff-check
	pre-commit run --all-files ruff-format

shellcheck: ## Run shellcheck
	pre-commit run --all-files shellcheck

help: ## Show this help screen
	@echo 'Usage: make <OPTIONS> ... <TARGETS>'
	@echo ''
	@echo 'Available targets are:'
	@echo ''
	@grep -E '^[ a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-35s\033[0m %s\n", $$1, $$2}'
	@echo ''
