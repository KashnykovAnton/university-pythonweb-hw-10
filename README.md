# university-pythonweb-hw-10

docker: docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres

Lesson: https://www.youtube.com/watch?v=w-xbSutnP0Q&t=1s

Commands:

init async alembic: - alembic init -t async migrations

poetry add black -G dev

alembic revision --autogenerate -m "Init"
alembic upgrade head

For pagination: https://uriyyo-fastapi-pagination.netlify.app/

run script - fastapi dev ./main.py
