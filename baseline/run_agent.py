import requests

BASE_URL = "http://127.0.0.1:8000"


def generate_sql(problem, schema):
    problem = problem.lower()

    if "all users" in problem:
        return "SELECT * FROM users"

    if "id > 1" in problem:
        return "SELECT * FROM users WHERE id > 1"

    if "join" in problem:
        return """
        SELECT users.id, users.name, orders.amount
        FROM users
        JOIN orders ON users.id = orders.user_id
        """

    return "SELECT * FROM users"


def run():
    total_score = 0
    num_tasks = 3

    for task_id in range(num_tasks):
        print(f"\n--- Running Task {task_id} ---")

        res = requests.get(f"{BASE_URL}/reset?task_id={task_id}").json()

        problem = res["problem"]
        schema = res["db_schema"]

        print("Problem:", problem)

        sql_query = generate_sql(problem, schema)
        print("SQL:", sql_query)

        step_res = requests.post(
            f"{BASE_URL}/step",
            json={"sql_query": sql_query}
        ).json()

        reward = step_res[1]["score"]
        feedback = step_res[1]["feedback"]

        print("Score:", reward, "| Feedback:", feedback)

        total_score += reward

    final_score = total_score / num_tasks
    print("\n🎯 FINAL SCORE:", final_score)


if __name__ == "__main__":
    run()