.PHONY: build run clean stop

IMAGE_NAME := obsidian-mcp
# Default vault path if not specified
VAULT_PATH ?= $(HOME)/Documents/vault
CONTAINER_NAME := obsidian-mcp-api

# Allow overriding OBSIDIAN_VAULT_PATH via environment variable
OBSIDIAN_VAULT_PATH ?= $(VAULT_PATH)

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d \
		-p 8010:8000 \
		-v "$(OBSIDIAN_VAULT_PATH):/vault" \
		-e OBSIDIAN_VAULT_PATH=/vault \
		--name $(CONTAINER_NAME) \
		$(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME) && \
	docker rm $(CONTAINER_NAME)

clean:
	docker rmi $(IMAGE_NAME)
	docker system prune -f
