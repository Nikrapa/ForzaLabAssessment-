import sqlite3
import pandas as pd
import json

def create_database(conn):
    """Create database schema."""
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS pokemon (
        id INTEGER PRIMARY KEY,
        name TEXT,
        weight INTEGER,
        height INTEGER,
        base_experience INTEGER
    );
    CREATE TABLE IF NOT EXISTS pokemon_types (
        pokemon_id INTEGER,
        type_name TEXT,
        FOREIGN KEY (pokemon_id) REFERENCES pokemon (id)
    );
    CREATE TABLE IF NOT EXISTS pokemon_abilities (
        pokemon_id INTEGER,
        ability_name TEXT,
        FOREIGN KEY (pokemon_id) REFERENCES pokemon (id)
    );
    CREATE TABLE IF NOT EXISTS damage_relations (
        type_name TEXT,
        relation_type TEXT,
        related_type_name TEXT,
        FOREIGN KEY (type_name) REFERENCES types (name)
    );
    """)
    conn.commit()
    print("Database schema created.")

def load_damage_relations_data(conn):
    """Load damage relations data into the database."""
    with open("data/damage_relations.json") as f:
        damage_relations_data = json.load(f)

    # Convert JSON to DataFrame
    df = pd.DataFrame(damage_relations_data)
    df.to_sql("damage_relations", conn, if_exists="replace", index=False)
    print("Damage relations data loaded into database.")

def load_other_data(conn):
    """Load other data into the database."""
    # Example: Load Pokémon data
    pokemon_df = pd.read_csv("data/transformed/pokemon.csv")
    pokemon_types_df = pd.read_csv("data/transformed/pokemon_types.csv")
    pokemon_abilities_df = pd.read_csv("data/transformed/pokemon_abilities.csv")

    # Load data into tables
    pokemon_df.to_sql("pokemon", conn, if_exists="replace", index=False)
    pokemon_types_df.to_sql("pokemon_types", conn, if_exists="replace", index=False)
    pokemon_abilities_df.to_sql("pokemon_abilities", conn, if_exists="replace", index=False)
    print("Other data loaded into database.")

if __name__ == "__main__":
    # Connect to SQLite database
    conn = sqlite3.connect("data/pokemon.db")
    print("Connected to database.")

    create_database(conn)

    load_other_data(conn)        
    load_damage_relations_data(conn)   

    conn.close()
    print("Database connection closed.")
