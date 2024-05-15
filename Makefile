# Makefile target args
args = $(filter-out $@,$(MAKECMDGOALS))

build: ;
	make down
	docker build -f backend.dockerfile --no-cache -t events-backend .

up: ;
	docker-compose -f docker-compose/services.yml -p events-backend up -d --build

down: ;
	docker-compose -f docker-compose/services.yml -p events-backend down -t 0

enter: ;
	docker exec -it evbackend bash
