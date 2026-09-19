import os
import csv
import re
import time

pod_index = os.getenv("JOB_COMPLETION_INDEX", "0")
pod_name = os.getenv("POD_NAME", "unknown-pod")
node_name = os.getenv("NODE_NAME", "unknown-node")

shard_path = f"shards/shard_{pod_index}.csv"
email_regex = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

invalid_count = 0
total_rows = 0

if not os.path.exists(shard_path):
    print(f"[ERROR] Shard file not found: {shard_path}")
    exit(1)

# Hold pod in Running state for 12 seconds so kubectl get pods -o wide captures concurrency
time.sleep(12)

with open(shard_path, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_rows += 1
        name = row.get("name", "").strip()
        email = row.get("email", "").strip()
        if not name or not email_regex.match(email):
            invalid_count += 1

print(f"REPORT: shard_id={pod_index} pod={pod_name} node={node_name} total={total_rows} invalid_rows={invalid_count}")
