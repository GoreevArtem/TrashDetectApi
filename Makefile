build:
	docker compose -f docker-compose.yml build

up:
	docker compose -f docker-compose.yml up -d

debug:
	docker compose -f docker-compose.yml up --build

stop:
	docker compose -f docker-compose.yml down

down:
	docker compose -f docker-compose.yml down -v