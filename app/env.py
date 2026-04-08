import sqlite3
from app.tasks import get_task
from app.grader import grade

class SQLEnv:
    def __init__(self):
        self.conn = None
        self.current_task = None

    def reset(self, task_id=0):
        self.conn = sqlite3.connect(":memory:")
        self.current_task = get_task(task_id)

        for stmt in self.current_task["setup"]:
            self.conn.execute(stmt)

        observation = {
            "problem": self.current_task["problem"],
            "db_schema": self.current_task["schema"],
            "last_error": None,
            "query_result": None
        }

        return observation

    def step(self, action):
        try:
            cursor = self.conn.execute(action.sql_query)
            result = cursor.fetchall()

            score, feedback = grade(result, self.current_task)

            observation = {
                "problem": self.current_task["problem"],
                "db_schema": self.current_task["schema"],
                "last_error": None,
                "query_result": str(result)
            }

            reward = {
                "score": float(score),
                "feedback": feedback
            }

            done = score == 1.0
            info = {}

            return observation, reward, done, info

        except Exception as e:
            observation = {
                "problem": self.current_task["problem"],
                "db_schema": self.current_task["schema"],
                "last_error": str(e),
                "query_result": None
            }

            reward = {
                "score": 0.0,   # ⚠️ FIXED (no negative)
                "feedback": "SQL Error"
            }

            return observation, reward, False, {}

    def state(self):
        return {
            "problem": self.current_task["problem"],
            "db_schema": self.current_task["schema"]
        }