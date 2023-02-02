import json

from datasets import load_dataset
from pyflowchart import Flowchart

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    ds = load_dataset("codeparrot/apps", split="train")
    sample = next(iter(ds))
    # non-empty solutions and input_output features can be parsed from text format this way:
    sample["solutions"] = json.loads(sample["solutions"])
    sample["input_output"] = json.loads(sample["input_output"])

    solutions = sample["solutions"]
    for solution in solutions:
        print("========Solution:==========")
        fc = Flowchart.from_code(solution)
        print(fc.flowchart())
