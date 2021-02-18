DROP SCHEMA public CASCADE;
CREATE SCHEMA public;


CREATE TABLE users
       (
        id SERIAL PRIMARY KEY,
        name VARCHAR (50) UNIQUE NOT NULL,
        email VARCHAR (255),
        registration_time TIMESTAMP
       );


CREATE TABLE cart
       (
        id SERIAL PRIMARY KEY,
        creation_time TIMESTAMP,
        user_id INT,
        CONSTRAINT fk_user
             FOREIGN KEY(user_id)
                  REFERENCES users(id)
       );

CREATE TABLE cart_details
(
        id SERIAL PRIMARY KEY,
        cart_id INT,
        price INT,
        product VARCHAR(255),
        CONSTRAINT fk_cart_id
             FOREIGN KEY(cart_id)
                  REFERENCES cart(id)

);

--- Just example data


INSERT INTO users
(name, email, registration_time)
VALUES
('Illia', 'illia.sukonnik@gmail.com', '2020-01-01 11:45:00'),
('Alex', 'alex@example.com', '2020-03-08 15:10:00'),
('Bohdan', 'bohdan@example.com', '2020-01-01 00:00:00');

INSERT INTO cart
(creation_time, user_id)
VALUES
('2020-01-01 00:15:00', 3),
('2020-03-08 16:00:00', 2),
('2020-10-11 4:00:00', 1),
('2020-11-15 19:00:00', 1);


INSERT INTO cart_details
(cart_id, price, product)
VALUES
(1, 200, 'mandarin'),
(1, 1500, 'fireworks'),
(1, 1000000, 'happiness');

INSERT INTO cart_details
(cart_id, price, product)
VALUES
(2, 500, 'flowers'),
(2, 10, 'stripe');

INSERT INTO cart_details
(cart_id, price, product)
VALUES
(3, 2500, 'keyboard'),
(3, 500, 'Book: how to stop be boring');

INSERT INTO cart_details
(cart_id, price, product)
VALUES
(4, 1500, 'fireworks'),
(4, 42, 'Book: OOP for dummies');


-- INSERT INTO cart_details
-- (cart_id, price, product)
-- VALUES
-- (5, 2000, 'Book: How to cure from MacOs'),
-- (5, 3000, 'Book: Another wise book name');