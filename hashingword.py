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
def sha256_hash(password):
    # Hash the password using SHA-256 and return the digest
    sha256 = hashlib.sha256()
    sha256.update(password.encode("utf-8"))
    return int(sha256.hexdigest(), 16) % len(unique_passwords)

# Initialize a hash table as a list
hash_table = [None] * len(unique_passwords)

# Track the number of collisions
collisions = 0

# Insert passwords into the hash table
for password in unique_passwords:
    index = sha256_hash(password)

    # Handle collisions by linear probing
    while hash_table[index] is not None:
        index = (index + 1) % len(unique_passwords)
        collisions += 1

    hash_table[index] = password

# Step 3: Create second and third hash functions, track collisions for both
# (You can add additional hash functions if needed)

# Define a second hash function (e.g., a different approach)
def second_hash(password):
    # An improved hash function using Python's built-in hash() with a different seed
    seed = 314  # Some arbitrary value
    combined_input = f"{password}{seed}"
    return int(hashlib.sha256(combined_input.encode("utf-8")).hexdigest(), 16) % len(unique_passwords)

# Initialize a second hash table and track collisions
second_hash_table = [None] * len(unique_passwords)
second_collisions = 0

# Define a third hash function (e.g., another approach)
def third_hash(password):
    # An improved hash function using a different approach - the ASCII value of the first character
    return ord(password[0]) % len(unique_passwords)

# Initialize a third hash table and track collisions
third_hash_table = [None] * len(unique_passwords)
third_collisions = 0

# Insert passwords using the second and third hash functions
for password in unique_passwords:
    # Using the second hash function
    index2 = second_hash(password)
    while second_hash_table[index2] is not None:
        index2 = (index2 + 1) % len(unique_passwords)
        second_collisions += 1
    second_hash_table[index2] = password

    # Using the third hash function
    index3 = third_hash(password)
    while third_hash_table[index3] is not None:
        index3 = (index3 + 1) % len(unique_passwords)
        third_collisions += 1
    third_hash_table[index3] = password

# Step 4: Determine which hash function provides the least collisions

best_hash_function = "SHA-256 Hash Function"
if second_collisions < collisions and second_collisions < third_collisions:
    best_hash_function = "Second Hash Function"
elif third_collisions < collisions and third_collisions < second_collisions:
    best_hash_function = "Third Hash Function"

# Step 5: Create a text file explaining hash function collision results

with open("hash_function_results.txt", "w") as results_file:
    results_file.write("Hash Function Collision Results:\n")
    results_file.write(f"- SHA-256 Hash Function Collisions: {collisions} collisions\n")
    results_file.write(f"- Second Hash Function Collisions: {second_collisions} collisions\n")
    results_file.write(f"- Third Hash Function Collisions: {third_collisions} collisions\n")
    results_file.write(f"The best hash function is {best_hash_function}\n")


collision_data = [
    ["SHA-256 Hash Function", collisions],
    ["Second Hash Function", second_collisions],
    ["Third Hash Function", third_collisions],
    ["The Best Hash Function is",best_hash_function]
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