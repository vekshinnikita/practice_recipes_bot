SELECT count(recipe.id) AS total_count 
FROM recipe JOIN recipe_tag ON recipe.id = recipe_tag.recipe_id JOIN tag ON tag.id = recipe_tag.tag_id 
WHERE recipe.nocase_name like '%черный%'