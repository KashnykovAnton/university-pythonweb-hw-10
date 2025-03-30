# university-pythonweb-hw-10

docker: docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres

Lesson 9: https://www.youtube.com/watch?v=w-xbSutnP0Q&t=1s
Lesson 10: https://www.youtube.com/watch?v=r3xDHqpTOSo&t=1s

Commands:

init async alembic: - alembic init -t async migrations

poetry add black -G dev

alembic revision --autogenerate -m "Init"
alembic upgrade head

For pagination: https://uriyyo-fastapi-pagination.netlify.app/

run script - fastapi dev ./main.py

Work with redis:
brew update
brew install redis
brew services start redis
Run "fastapi dev ./main.py" only after running redis!

docker-compose
to run: docker-compose up -d

If after registration ocurs the next error:
"Exception raised Error connecting to smtp.meta.ua on port 465: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (\_ssl.c:1020), check your credentials or email service configuration"
follow - https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate
