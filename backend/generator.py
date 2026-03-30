import random

def generate_dataset(schema, size=5):
    data = []
    for _ in range(size):
        data.append({
            "name": random.choice(["Alice", "Bob", "Charlie"]),
            "value": random.randint(1, 100)
        })
    return data
