# =========================
# Variabel
# =========================
WEB_DB_NAME = office
DOCKER = docker
DOCKER_COMPOSE = ${DOCKER} compose
CONTAINER_ODOO = odoo-17a
CONTAINER_DB = odoo17a-postgres
USER = odoo
PASSWORD = odoo
include .env
export

# =========================
# Bantuan
# =========================
help:
	@echo "Available targets:"
	@echo "   start               - Start the containers"
	@echo "   stop                - Stop the containers"
	@echo "   restart             - Restart the containers"
	@echo "   console             - Odoo interactive shell"
	@echo "   psql                - PostgreSQL interactive shell"
	@echo "   logs odoo           - Show logs from Odoo container"
	@echo "   logs db             - Show logs from PostgreSQL container"
	@echo "   addon <addon_name>  - Restart instance and upgrade addon"

# =========================
# Perintah dasar
# =========================
start:
	$(DOCKER_COMPOSE) up -d

stop:
	$(DOCKER_COMPOSE) down

restart:
	$(DOCKER_COMPOSE) restart

console:
	$(DOCKER) exec -it $(CONTAINER_ODOO) odoo shell \
		--db_host=$(CONTAINER_DB) -d $(WEB_DB_NAME) -r $(USER) -w $(PASSWORD)

psql:
	$(DOCKER) exec -it $(CONTAINER_DB) psql -U $(USER) -d $(WEB_DB_NAME)

# =========================
# Logs
# =========================
define log_target
	@if [ "$(1)" = "odoo" ]; then \
		$(DOCKER_COMPOSE) logs -f $(CONTAINER_ODOO); \
	elif [ "$(1)" = "db" ]; then \
		$(DOCKER_COMPOSE) logs -f $(CONTAINER_DB); \
	else \
		echo "Invalid logs target. Use 'make logs odoo' or 'make logs db'."; \
	fi
endef

logs:
	$(call log_target,$(word 2,$(MAKECMDGOALS)))

# =========================
# Upgrade addon
# =========================
define upgrade_addon
	$(DOCKER) exec -it $(CONTAINER_ODOO) odoo \
		--db_host=$(CONTAINER_DB) \
		-d $(WEB_DB_NAME) \
		-r $(USER) \
		-w $(PASSWORD) \
		-u $(1)
endef

addon: restart
	$(call upgrade_addon,$(word 2,$(MAKECMDGOALS)))

# =========================
# Target umum supaya argumen tambahan tidak error
# =========================
%:
	@:

.PHONY: start stop restart console psql logs addon