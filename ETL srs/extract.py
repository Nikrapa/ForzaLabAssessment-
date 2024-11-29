import requests
import json
import os

# Create a data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Base URL for the PokéAPI
BASE_URL = "https://pokeapi.co/api/v2"

# Function to fetch data from a given endpoint
def fetch_data(endpoint, params=None):
    """Fetch data from the API endpoint."""
    response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch {endpoint}: {response.status_code}")
        return None

def extract_pokemon_data():
    """Fetch and save data for the first generation of Pokémon."""
    pokemon_data = []
    for i in range(1, 152):  
        data = fetch_data(f"pokemon/{i}")
        if data:
            pokemon_data.append({
                "id": data["id"],
                "name": data["name"],
                "weight": data["weight"],
                "height": data["height"],
                "base_experience": data["base_experience"],
                "types": [t["type"]["name"] for t in data["types"]],
                "abilities": [a["ability"]["name"] for a in data["abilities"]],
            })

    # Save extracted data to a JSON file
    output_file = "data/pokemon.json"
    with open(output_file, "w") as f:
        json.dump(pokemon_data, f, indent=4)
    print(f"Extracted Pokémon data saved to {output_file}")

def extract_type_data():
    """Fetch and save type-specific information, including damage relations."""
    data = fetch_data("type")
    if data:
        types_data = []
        damage_relations_data = []
        for type_info in data["results"]:
            type_details = fetch_data(type_info["url"].split(BASE_URL + "/")[-1])
            types_data.append({
                "id": type_details["id"],
                "name": type_details["name"]
            })
            for relation, types in type_details["damage_relations"].items():
                for related_type in types:
                    damage_relations_data.append({
                        "type_name": type_details["name"],
                        "relation_type": relation,
                        "related_type_name": related_type["name"]
                    })

        # Save types and damage relations data
        with open("data/types.json", "w") as f:
            json.dump(types_data, f, indent=4)
        with open("data/damage_relations.json", "w") as f:
            json.dump(damage_relations_data, f, indent=4)
        print("Extracted type data and damage relations saved.")

def extract_ability_data():
    """Fetch and save Pokémon abilities and descriptions."""
    ability_data = []
    for i in range(1, 51): 
        data = fetch_data(f"ability/{i}")
        if data:
            ability_data.append({
                "id": data["id"],
                "name": data["name"],
                "effect": data.get("effect_entries", [{}])[0].get("effect", "")
            })

    # Save ability data to a JSON file
    output_file = "data/abilities.json"
    with open(output_file, "w") as f:
        json.dump(ability_data, f, indent=4)
    print(f"Extracted ability data saved to {output_file}")

if __name__ == "__main__":
    extract_pokemon_data()
    extract_type_data()
    extract_ability_data()
