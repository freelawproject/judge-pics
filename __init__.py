import json
import os

judge_root = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(judge_root, 'judges.json')) as f:
    judge_pics = json.load(f)

