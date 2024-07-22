insert INTO ingredient (id, name) VALUES (1, 'Сахар'), (2, 'Пакетик чая');

insert Into recipe (id, name, nocase_name, description, image_id) values (1, 'Черный чай с бергамотом', 'черный чай с бергамотом', 'Вкусный чай', 'AgACAgIAAxkBAAPLZpJheY1Vm8Rw_4jPED_iKM7a7AQAAn3dMRuu0pFIgXK6A8W3QGUBAAMCAAN5AAM1BA');

insert Into recipe (id, name, nocase_name, description, image_id) values (2, 'Зеленый чай с малиной', 'зеленый чай с малиной', 'Вкусный зеленый чай', 'AgACAgIAAxkBAAPIZpJg8HeAGVH_4-e0Jggs9GN6kXoAAnvdMRuu0pFIf6XFFz7sg5ABAAMCAAN5AAM1BA');

insert into tag (id, name) values (1, 'Десерт'), (2, 'Напиток'), (3, 'Низко калорийный');

insert Into recipe_tag (recipe_id, tag_id) values (1, 1), (1, 2), (2, 3), (2, 2);

insert into recipe_ingredient (id, ingredient_id, recipe_id, amount, amount_type) values (1, 2, 1, 1, 'PIECE'), (2, 1, 1, 2, 'SMALL_SPOON');

insert into recipe_step (id, sequence_number, recipe_id, description, image_id) values 
    (1, 1, 1, 'Положить чайный пакетик в кружку', 'AgACAgIAAxkBAAIDgmaTnhsV4eHaKYZIyRDbWTUowD_EAAIV2jEb9KChSAiucVz1L99AAQADAgADeQADNQQ'), 
    (2, 2, 1, 'Залить кипятком', 'AgACAgIAAxkBAAIDhGaTnna5L0eZhExv4infujGi0nkFAAIa2jEb9KChSCdPobW2hTeHAQADAgADeQADNQQ'), 
    (3, 3, 1, 'Подождать 2 минуты', 'AgACAgIAAxkBAAIBZGaSt1IhzQ_4VFv6XJ47sk-cqSOVAAJ53zEbrtKRSKbJksRnkqr3AQADAgADeQADNQQ'),
    (4, 4, 1, 'Вытащить пакетик', 'AgACAgIAAxkBAAIDhmaTnrKG5YATEQUVfuFmdVsnOF7SAAIb2jEb9KChSGto_ogdQh6zAQADAgADeQADNQQ'),
    (5, 5, 1, 'Насыпать 2 маленькие ложки сахара в кружку', 'AgACAgIAAxkBAAIDiGaTnuLJfSvYVkOpNsMx07x0r8tnAAIc2jEb9KChSCDtntvYiAtbAQADAgADeQADNQQ'),
    (6, 6, 1, 'Перемешать сахар ложкой', 'AgACAgIAAxkBAAIBZGaSt1IhzQ_4VFv6XJ47sk-cqSOVAAJ53zEbrtKRSKbJksRnkqr3AQADAgADeQADNQQ');