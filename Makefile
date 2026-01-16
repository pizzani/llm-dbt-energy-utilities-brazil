up:
	docker compose up -d --build
py:
	docker compose run --rm python python $(ARGS)
sh:
	docker compose exec python bash