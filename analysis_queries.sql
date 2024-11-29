-- Query 1: Top 5 heaviest Pokémon per type
SELECT 
    t.type_name,
    p.name AS pokemon_name,
    p.weight
FROM 
    pokemon p
JOIN 
    pokemon_types t ON p.id = t.pokemon_id
ORDER BY 
    t.type_name, p.weight DESC
LIMIT 5;

-- Query 2: Pokémon with the most abilities
SELECT 
    p.name AS pokemon_name,
    COUNT(a.ability_name) AS ability_count
FROM 
    pokemon p
JOIN 
    pokemon_abilities a ON p.id = a.pokemon_id
GROUP BY 
    p.name
ORDER BY 
    ability_count DESC
LIMIT 1;

-- Query 3: Average base experience by type
SELECT 
    t.type_name,
    AVG(p.base_experience) AS avg_base_experience
FROM 
    pokemon p
JOIN 
    pokemon_types t ON p.id = t.pokemon_id
GROUP BY 
    t.type_name;

-- Query 4: Types with the strongest and weakest damage relations
SELECT 
    type_name,
    relation_type,
    COUNT(related_type_name) AS relation_count
FROM 
    damage_relations
GROUP BY 
    type_name, relation_type
ORDER BY 
    relation_count DESC;

