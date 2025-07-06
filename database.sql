CREATE TABLE urls (
id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
name VARCHAR(255) UNIQUE NOT NULL,
created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO urls (name)
VALUES ('https://ru.hexlet.io/courses/python-flask/lessons/crud/theory_unit');

INSERT INTO urls (name)
VALUES ('https://www.psycopg.org/docs/install.html#quick-install');

DROP TABLE urls;

psql -U "vitaliy333" -d "hexlet"

SELECT * FROM urls;