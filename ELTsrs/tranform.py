import pandas as pd
import json
import os

# Normalize the Pokémon data
def normalize_pokemon_data():
    """Transform Pokémon data into separate CSV files."""
    with open("data/pokemon.json") as f:
        pokemon = json.load(f)

    # Create Pokémon DataFrame
    pokemon_df = pd.DataFrame(pokemon)

    
    types_df = pokemon_df.explode("types")[["id", "types"]].rename(columns={"id": "pokemon_id", "types": "type_name"})
    abilities_df = pokemon_df.explode("abilities")[["id", "abilities"]].rename(columns={"id": "pokemon_id", "abilities": "ability_name"})

    
    pokemon_df = pokemon_df.drop(columns=["types", "abilities"])

    # Save transformed data
    os.makedirs("data/transformed", exist_ok=True)
    pokemon_df.to_csv("data/transformed/pokemon.csv", index=False)
    types_df.to_csv("data/transformed/pokemon_types.csv", index=False)
    abilities_df.to_csv("data/transformed/pokemon_abilities.csv", index=False)
    print("Transformed Pokémon data saved to data/transformed/")

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

    # Save the DataFrame to a CSV file
    output_file = "data/transformed/damage_relations.csv"
    df.to_csv(output_file, index=False)
    print(f"Damage relations data transformed and saved to {output_file}")

if __name__ == "__main__":
    # Transform Pokémon and damage relations data
    normalize_pokemon_data()
    transform_damage_relations()
