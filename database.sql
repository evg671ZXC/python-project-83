DROP TABLE IF EXISTS url_checks CASCADE;
DROP TABLE IF EXISTS urls CASCADE;

CREATE TABLE urls 
(
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at DATE
);

CREATE TABLE url_checks
(
    id          bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id      bigint,
    status_code integer,
    h1          VARCHAR(255),
    title       VARCHAR(255),
    description VARCHAR(255),
    created_at  DATE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (url_id) REFERENCES urls (id) ON DELETE CASCADE ON UPDATE CASCADE
);