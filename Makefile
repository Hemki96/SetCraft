SHELL := /bin/bash

SCRIPT_DIR := infra/scripts

.PHONY: bootstrap dev test test-unit test-int lint format typecheck seed clean

bootstrap:
	@$(SCRIPT_DIR)/bootstrap.sh

dev:
	@$(SCRIPT_DIR)/dev.sh

test:
	@$(SCRIPT_DIR)/test.sh

test-unit:
	@$(SCRIPT_DIR)/test-unit.sh

test-int:
	@$(SCRIPT_DIR)/test-int.sh

lint:
	@$(SCRIPT_DIR)/lint.sh

format:
	@$(SCRIPT_DIR)/format.sh

typecheck:
	@$(SCRIPT_DIR)/typecheck.sh

seed:
	@$(SCRIPT_DIR)/seed.sh

clean:
	@$(SCRIPT_DIR)/clean.sh
