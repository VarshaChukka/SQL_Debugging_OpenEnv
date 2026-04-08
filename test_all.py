import requests

BASE = "http://127.0.0.1:8000"

def check(name, condition):
    print(f"{name}: {'PASS' if condition else 'FAIL'}")

# 1. tasks
res = requests.get(f"{BASE}/tasks").json()
check("Tasks endpoint", len(res["tasks"]) == 3)

# 2. reset
res = requests.get(f"{BASE}/reset?task_id=0").json()
check("Reset endpoint", "problem" in res and "db_schema" in res)

# 3. step correct
res = requests.post(f"{BASE}/step", json={"sql_query": "SELECT * FROM users"}).json()
check("Correct query", res[1]["score"] == 1.0)

# 4. step wrong
res = requests.post(f"{BASE}/step", json={"sql_query": "SELECT name FROM users"}).json()
check("Wrong query scoring", res[1]["score"] < 1.0)

# 5. state
res = requests.get(f"{BASE}/state").json()
check("State endpoint", isinstance(res, dict))

# 6. invalid task
try:
    requests.get(f"{BASE}/reset?task_id=10").json()
    print("Invalid task handling: PASS")
except:
    print("Invalid task handling: FAIL")

print("\n✅ AUTO TEST COMPLETED")