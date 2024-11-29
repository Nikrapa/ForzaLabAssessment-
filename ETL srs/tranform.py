import pandas as pd
import json
import os

# Normalize the Pokémon data
def normalize_pokemon_data():
    """Transform Pokémon data into separate CSV files and clean the data."""
    with open("data/pokemon.json") as f:
        pokemon = json.load(f)

    # Create Pokémon DataFrame
    pokemon_df = pd.DataFrame(pokemon)

    # Remove duplicates: drop rows with duplicate Pokémon IDs or names
    pokemon_df = pokemon_df.drop_duplicates(subset=["id", "name"])

    # - Fill missing weights, heights, base_experience with 0 or NaN 
    pokemon_df['weight'] = pokemon_df['weight'].fillna(0)
    pokemon_df['height'] = pokemon_df['height'].fillna(0)
    pokemon_df['base_experience'] = pokemon_df['base_experience'].fillna(0)

    # Create types and abilities DataFrames 
    types_df = pokemon_df.explode("types")[["id", "types"]].rename(columns={"id": "pokemon_id", "types": "type_name"})
    abilities_df = pokemon_df.explode("abilities")[["id", "abilities"]].rename(columns={"id": "pokemon_id", "abilities": "ability_name"})

    # Drop the original lists of types and abilities from the Pokémon DataFrame
    pokemon_df = pokemon_df.drop(columns=["types", "abilities"])

    # Save transformed and cleaned data
    os.makedirs("data/transformed", exist_ok=True)
    pokemon_df.to_csv("data/transformed/pokemon.csv", index=False)
    types_df.to_csv("data/transformed/pokemon_types.csv", index=False)
    abilities_df.to_csv("data/transformed/pokemon_abilities.csv", index=False)
    
    print("Transformed and cleaned Pokémon data saved to data/transformed/")

# Transform damage relations data
def transform_damage_relations():
    """Transform damage relations data into a CSV file."""
    # Ensure the transformed data directory exists
    os.makedirs("data/transformed", exist_ok=True)

    # Load damage_relations.json
    with open("data/damage_relations.json") as f:
        damage_relations_data = json.load(f)

    # Convert JSON to a DataFrame
    df = pd.DataFrame(damage_relations_data)

    # Check for missing data and handle it (e.g., fill with "Unknown" or remove rows with missing relations)
    df['type_name'] = df['type_name'].fillna("Unknown")
    df['relation_type'] = df['relation_type'].fillna("Unknown")
    df['related_type_name'] = df['related_type_name'].fillna("Unknown")

    # Save the DataFrame to a CSV file
    output_file = "data/transformed/damage_relations.csv"
    df.to_csv(output_file, index=False)
    print(f"Damage relations data transformed and saved to {output_file}")

if __name__ == "__main__":
    # Transform Pokémon and damage relations data
    normalize_pokemon_data()
    transform_damage_relations()
