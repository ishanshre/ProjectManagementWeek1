#!make

include .env

createPostgresContainer:
	docker run --name ${db_name} -e POSTGRES_USER=${db_user} -e POSTGRES_PASSWORD=${db_password} -p 5432:5432 -d postgres
