import time
import requests

url = "http://127.0.0.1:8000/predict"
payload = {"text": "WIN a FREE cash prize now! Click here: bit.ly/xyz123"}

print("=== Request 1: Expecting Cache MISS ===")
t0 = time.perf_counter()
res1 = requests.post(url, json=payload)
dur1 = (time.perf_counter() - t0) * 1000.0
print(f"Status Code: {res1.status_code}")
print(f"Response:    {res1.json()}")
print(f"Latency:     {dur1:.2f} ms\n")

print("=== Request 2: Expecting Cache HIT ===")
t1 = time.perf_counter()
res2 = requests.post(url, json=payload)
dur2 = (time.perf_counter() - t1) * 1000.0
print(f"Status Code: {res2.status_code}")
print(f"Response:    {res2.json()}")
print(f"Latency:     {dur2:.2f} ms\n")

speedup = dur1 / dur2 if dur2 > 0 else 0
print(f"Speedup Factor: {speedup:.2f}x faster on Cache Hit")
