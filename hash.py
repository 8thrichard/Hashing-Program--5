# Richard Boamah | Lab 5 - Hashing Program | Fall 2023
from tabulate import tabulate
import hashlib

# Step 1: Open the text file, remove duplicates, and create a clean data file

# Create a set to store unique passwords
unique_passwords = set()

# Open the input text file and remove duplicates
with open("passwords.txt", "r") as file:
    for line in file:
        password = line.strip()  # Remove leading/trailing whitespace
        unique_passwords.add(password)

# Create a clean data file with unique passwords
with open("clean_passwords.txt", "w") as clean_file:
    for password in unique_passwords:
        clean_file.write(password + '\n')

# Step 2: Implement a hash function using SHA-256
# Utilized CHATGPT AI
def sha256_hash(password, hash_table):
    # Hash the password using SHA-256 and return the digest
    sha256 = hashlib.sha256()
    sha256.update(password.encode("utf-8"))
    hashed_password = int(sha256.hexdigest(), 16)

    index = hashed_password % len(hash_table)
    collisions = 0

    while hash_table[index] is not None:
        if hash_table[index] == password:
            # Password is already in the hash table, no collision
            break
        index = (index + 1) % len(hash_table)
        collisions += 1

    if collisions > 0:
        return collisions

    hash_table[index] = password
    return collisions

# Initialize a hash table as a list for the SHA-256 hash function
hash_table_sha256 = [None] * len(unique_passwords)

# Initialize collisions counters
collisions_sha256 = 0

# Insert passwords into the SHA-256 hash table and count collisions
for password in unique_passwords:
    collisions = sha256_hash(password, hash_table_sha256)
    collisions_sha256 += collisions

# Step 3: Create second and third hash functions, track collisions for both

# Define a second hash function (e.g., a different approach)
def second_hash(password, hash_table):
    seed = 314  # Some arbitrary value
    combined_input = f"{password}{seed}"
    hashed_password = int(hashlib.sha256(combined_input.encode("utf-8")).hexdigest(), 16)

    index = hashed_password % len(hash_table)
    collisions = 0

    while hash_table[index] is not None:
        if hash_table[index] == password:
            # Password is already in the hash table, no collision
            break
        index = (index + 1) % len(hash_table)
        collisions += 1

    if collisions > 0:
        return collisions

    hash_table[index] = password
    return collisions

# Initialize a hash table as a list for the second hash function
hash_table_second = [None] * len(unique_passwords)

# Initialize collisions counters
collisions_second = 0

# Insert passwords using the second hash function and count collisions
for password in unique_passwords:
    collisions = second_hash(password, hash_table_second)
    collisions_second += collisions

# Define a third hash function (e.g., another approach)
def third_hash(password, hash_table):
    hashed_password = ord(password[0])  # Use the ASCII value of the first character

    index = hashed_password % len(hash_table)
    collisions = 0

    while hash_table[index] is not None:
        if hash_table[index] == password:
            # Password is already in the hash table, no collision
            break
        index = (index + 1) % len(hash_table)
        collisions += 1

    if collisions > 0:
        return collisions

    hash_table[index] = password
    return collisions

# Initialize a hash table as a list for the third hash function
hash_table_third = [None] * len(unique_passwords)

# Initialize collisions counters
collisions_third = 0

# Insert passwords using the third hash function and count collisions
for password in unique_passwords:
    collisions = third_hash(password, hash_table_third)
    collisions_third += collisions

# Step 4: Determine which hash function provides the least collisions

def count_total_collisions():
    return collisions_sha256 + collisions_second + collisions_third

best_hash_function = "SHA-256 Hash Function"
total_collisions = count_total_collisions()

if collisions_second < total_collisions and collisions_second < collisions_third:
    best_hash_function = "Second Hash Function"
elif collisions_third < total_collisions and collisions_third < collisions_second:
    best_hash_function = "Third Hash Function"

# Step 5: Create a text file explaining hash function collision results

with open("hash_function_results.txt", "w") as results_file:
    results_file.write("Hash Function Collision Results:\n")
    results_file.write(f"- SHA-256 Hash Function Collisions: {collisions_sha256} collisions\n")
    results_file.write(f"- Second Hash Function Collisions: {collisions_second} collisions\n")
    results_file.write(f"- Third Hash Function Collisions: {collisions_third} collisions\n")
    results_file.write(f"The best hash function is {best_hash_function}\n")
    results_file.write(f"Total Collisions: {total_collisions}\n")

collision_data = [
    ["SHA-256 Hash Function", collisions_sha256],
    ["Second Hash Function", collisions_second],
    ["Third Hash Function", collisions_third],
    ["The Best Hash Function is", best_hash_function],
    ["Total Collisions", total_collisions]
]

collision_table = tabulate(collision_data, headers=["Hash Function", "Collisions"], tablefmt="fancy_grid")

# Print the collision results table
print("Collision Results:")
print(collision_table)

# Save the collision results to a text file
with open("collision_results.txt", "w") as results_file:
    results_file.write("Collision Results:\n")
    results_file.write(collision_table)

# References:
# - GeeksforGeeks - Introduction to Hashing (https://www.geeksforgeeks.org/introduction-to-hashing-data-structure-and-algorithm-tutorials/)
# -  https://www.simplilearn.com/tutorials/cyber-security-tutorial/sha-256-algorithm
# - ChatGPT AI - to Understand more and write some of the functions effectively

