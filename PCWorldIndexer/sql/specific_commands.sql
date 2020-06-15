/*
 * Copyright © 2020 NeuroByte Tech. All rights reserved.
 *
 * NeuroByte Tech is the Developer Company of Rohan Mathew.
 *
 * Project: PriceTracker
 * File Name: specific_commands.sql
 * Last Modified: 11/05/2020, 19:59
 */

SELECT COUNT(*)
FROM ppt_products
WHERE id = 298473;

SELECT COUNT(*)
FROM ppt_prices
WHERE date = ''
  AND product_id = 6734;

SELECT COUNT(*)
FROM (
         SELECT *
         FROM lzx36405.ppt_prices p
         WHERE p.product_id = '245055'
           AND p.price = 907.2
           AND p.available = true
         ORDER BY date DESC
         LIMIT 1
     );

SELECT COUNT(*)
FROM lzx36405.ppt_prices p
WHERE p.date = '2020-05-11'
  AND p.product_id = 245055
  AND
