#build:
#	docker compose -f docker-compose.yml build

up:
	docker compose -f docker-compose.yml up --build

down:
	docker compose -f docker-compose.yml down -v