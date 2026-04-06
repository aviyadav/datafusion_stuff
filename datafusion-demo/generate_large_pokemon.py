import csv
import random
import multiprocessing as mp
from functools import partial

def generate_pokemon_chunk(start_id, chunk_size, pokemon_data, seed):
    """Generate a chunk of pokemon rows"""
    random.seed(seed)
    rows = []
    
    for i in range(chunk_size):
        # Pick a random pokemon from the original data
        base_pokemon = random.choice(pokemon_data)
        
        # Create a new row with slight variations in stats
        new_row = base_pokemon.copy()
        
        # Vary the numeric stats slightly (columns 4-10: Total, HP, Attack, Defense, Sp. Atk, Sp. Def, Speed)
        for col_idx in [4, 5, 6, 7, 8, 9, 10]:
            try:
                original_value = int(base_pokemon[col_idx])
                # Add random variation of +/- 10%
                variation = random.randint(-original_value//10, original_value//10)
                new_row[col_idx] = str(max(1, original_value + variation))
            except (ValueError, IndexError):
                pass
        
        # Update the ID to be sequential
        new_row[0] = str(start_id + i)
        rows.append(new_row)
    
    return rows

def generate_large_pokemon_csv(input_file='pokemon.csv', output_file='pokemon_million.csv', target_rows=1000000):
    """Generate a CSV file with a million rows based on pokemon.csv using multiprocessing"""
    
    # Read the original pokemon data
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        pokemon_data = list(reader)
    
    print(f"Original pokemon data has {len(pokemon_data)} rows")
    print(f"Generating {target_rows:,} rows using multiprocessing...")
    
    # Determine number of processes and chunk size
    num_processes = mp.cpu_count()
    chunk_size = target_rows // num_processes
    
    print(f"Using {num_processes} processes with chunk size of {chunk_size:,} rows each")
    
    # Create tasks for each process
    tasks = []
    for i in range(num_processes):
        start_id = i * chunk_size + 1
        # Last process handles any remainder
        current_chunk_size = chunk_size if i < num_processes - 1 else target_rows - i * chunk_size
        seed = random.randint(0, 1000000)
        tasks.append((start_id, current_chunk_size, pokemon_data, seed))
    
    # Generate rows in parallel
    with mp.Pool(processes=num_processes) as pool:
        results = pool.starmap(generate_pokemon_chunk, tasks)
    
    print("Writing results to file...")
    
    # Write the large CSV file
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        # Write all chunks
        for chunk in results:
            writer.writerows(chunk)
    
    print(f"Successfully generated {output_file} with {target_rows:,} rows!")

if __name__ == '__main__':
    generate_large_pokemon_csv()
