def get_task(task_id):

    tasks = [
        # EASY
        {
            "problem": "Get all users",
            "schema": "users(id, name)",
            "setup": [
                "CREATE TABLE users(id INT, name TEXT)",
                "INSERT INTO users VALUES (1,'A'), (2,'B')"
            ],
            "expected": [(1,'A'), (2,'B')]
        },

        # MEDIUM
        {
            "problem": "Get users with id > 1",
            "schema": "users(id, name)",
            "setup": [
                "CREATE TABLE users(id INT, name TEXT)",
                "INSERT INTO users VALUES (1,'A'), (2,'B'), (3,'C')"
            ],
            "expected": [(2,'B'), (3,'C')]
        },

        # HARD
        {
            "problem": "Join users and orders",
            "schema": "users(id, name), orders(user_id, amount)",
            "setup": [
                "CREATE TABLE users(id INT, name TEXT)",
                "CREATE TABLE orders(user_id INT, amount INT)",
                "INSERT INTO users VALUES (1,'A'), (2,'B')",
                "INSERT INTO orders VALUES (1,100), (2,200)"
            ],
            "expected": [(1,'A',100), (2,'B',200)]
        }
    ]

    # ✅ SAFETY CHECK (IMPORTANT)
    if task_id < 0 or task_id >= len(tasks):
        raise ValueError("Invalid task_id")

    return tasks[task_id]