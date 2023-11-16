--# create table --


CREATE TABLE person
(
    p_name               text,
    p_surname            text,
    sex                  text,
    age                  numeric,
    country              text
);


-- # data load --

COPY person
FROM '/docker-entrypoint-initdb.d/data/person.csv'
DELIMITER ','
ENCODING 'UTF8'
CSV HEADER;
