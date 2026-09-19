import csv
import os
import random

random.seed(42)
os.makedirs("shards", exist_ok=True)

for shard_id in range(8):
    filepath = f"shards/shard_{shard_id}.csv"
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "name", "email"])
        for row_id in range(100):
            uid = f"user_{shard_id}_{row_id}"
            is_invalid = random.random() < (0.10 + shard_id * 0.02)
            if is_invalid:
                invalid_type = random.choice(["bad_email", "missing_name"])
                if invalid_type == "bad_email":
                    writer.writerow([uid, f"User_{row_id}", f"broken_email_{row_id}.com"])
                else:
                    writer.writerow([uid, "", f"user_{row_id}@example.com"])
            else:
                writer.writerow([uid, f"User_{row_id}", f"user_{row_id}@example.com"])
    print(f"Generated {filepath}")
