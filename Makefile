.PHONY: help
help:
	@echo "Call one of the available targets:"
	@sed -n 's/\(^[^.#[:space:]A-Z]*\):.*$$/\1/p' Makefile | uniq

.PHONY: init
init:
	uv sync

# Override to use uv, e.g. PYTHON_RUN="uv run"
PYTHON_RUN ?=

.PHONY: test
test:
	$(PYTHON_RUN) py.test -s --cov-report=term --cov=baremetal_support tests/

.PHONY: tidy
tidy: ## Format code and fix linting issues
	ruff format
	ruff check --fix

.PHONY: check-types-ty
check-types-ty: ## Run ty type checker
	ty check
