/*
 * Copyright © 2020 NeuroByte Tech. All rights reserved.
 *
 * NeuroByte Tech is the Developer Company of Rohan Mathew.
 *
 * Project: PriceTracker
 * File Name: general.sql
 * Last Modified: 11/05/2020, 19:59
 */

CREATE TABLE ppt_products
(
    id    INT           NOT NULL PRIMARY KEY,
    brand VARCHAR(50)   NOT NULL,
    model VARCHAR(150)  NOT NULL UNIQUE,
    url   VARCHAR(1000) NOT NULL UNIQUE
);
SELECT *
FROM ppt_products;

CREATE TABLE ppt_prices
(
    date       DATE    NOT NULL,
    product_id INT     NOT NULL REFERENCES ppt_products,
    price      DOUBLE,
    available  BOOLEAN NOT NULL
);
SELECT *
FROM ppt_prices;

DROP TABLE ppt_products;
DROP TABLE ppt_prices;

INSERT INTO ppt_products (id, brand, model, url)
VALUES (9382038, 'hasdif', 'rsdflajsdfhdsg', 'hgsdfg');
INSERT INTO ppt_prices (date, product_id, price, available)
VALUES (2020 - 5 - 28, 245066, 907.2, true);