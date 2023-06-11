from datasets import load_dataset

if __name__ == "__main__":
    mbpp_ds = load_dataset("mbpp", "sanitized")

    for i in range(1):
        print(mbpp_ds["train"][i]["code"])

    he_test_dds = load_dataset("openai_humaneval")["test"]

    for i in range(1):
        print("task_id: ", he_test_dds[i]["task_id"])
        print("prompt: ", he_test_dds[i]["prompt"])
        print("canonical_solution: ", he_test_dds[i]["canonical_solution"])
        print("test: ", he_test_dds[i]["test"])
        print("entry_point: ", he_test_dds[i]["entry_point"])
