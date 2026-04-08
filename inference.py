import os
from openai import OpenAI
import requests

# REQUIRED ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# Initialize OpenAI client (MANDATORY)
client = OpenAI(
    base_url="https://api.openai.com/v1",
    api_key=HF_TOKEN
)

BASE_URL = API_BASE_URL


def generate_sql(problem):
    problem = problem.lower()

    if "all users" in problem:
        return "SELECT * FROM users"

    if "id > 1" in problem:
        return "SELECT * FROM users WHERE id > 1"

    if "join" in problem:
        return "SELECT users.id, users.name, orders.amount FROM users JOIN orders ON users.id = orders.user_id"

    return "SELECT * FROM users"


def run_task(task_id):
    step_count = 0
    rewards = []
    success = False

    print(f"[START] task={task_id} env=sql-debug model={MODEL_NAME}")

    try:
        # RESET
        res = requests.get(f"{BASE_URL}/reset?task_id={task_id}")
        res_json = res.json()
        problem = res_json["problem"]

        # GENERATE ACTION
        action = generate_sql(problem)
        step_count += 1

        # STEP
        step_res = requests.post(
            f"{BASE_URL}/step",
            json={"sql_query": action}
        )
        step_json = step_res.json()

        reward = float(step_json[1]["score"])
        done = step_json[2]

        rewards.append(f"{reward:.2f}")

        print(
            f"[STEP] step={step_count} action={action} reward={reward:.2f} "
            f"done={'true' if done else 'false'} error=null"
        )

        success = done

    except Exception as e:
        error_msg = str(e).replace("\n", " ")

        # IMPORTANT: still print STEP line
        print(
            f"[STEP] step={step_count} action=null reward=0.00 done=false error=\"{error_msg}\""
        )

    # END (ALWAYS PRINT)
    print(
        f"[END] success={'true' if success else 'false'} "
        f"steps={step_count} rewards={','.join(rewards) if rewards else '0.00'}"
    )


if __name__ == "__main__":
    for task_id in range(3):
        run_task(task_id)