import json
import os


judge_root = os.path.abspath(
    os.path.join(os.path.realpath(__file__), "..", "data")
)


with open(os.path.join(judge_root, "people.json")) as f:
    judge_pics = json.load(f)
