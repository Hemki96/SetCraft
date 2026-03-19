SHELL := /bin/bash

SCRIPT_DIR := infra/scripts

.PHONY: bootstrap dev test test-unit test-int lint format typecheck seed clean verify-foundation db-smoke

bootstrap:
	@bash $(SCRIPT_DIR)/bootstrap.sh

dev:
	@bash $(SCRIPT_DIR)/dev.sh

test:
	@bash $(SCRIPT_DIR)/test.sh

test-unit:
	@bash $(SCRIPT_DIR)/test-unit.sh

test-int:
	@bash $(SCRIPT_DIR)/test-int.sh

lint:
	@bash $(SCRIPT_DIR)/lint.sh

format:
	@bash $(SCRIPT_DIR)/format.sh

typecheck:
	@bash $(SCRIPT_DIR)/typecheck.sh

seed:
	@bash $(SCRIPT_DIR)/seed.sh

clean:
	@bash $(SCRIPT_DIR)/clean.sh

verify-foundation:
	@$(SCRIPT_DIR)/verify-foundation.sh

db-smoke:
	@bash $(SCRIPT_DIR)/db-smoke.sh
