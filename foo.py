import uuid
from typing import List


def generate_uuid() -> str:
    return str(uuid.uuid4())


def generate_10_uuid() -> List[str]:
    return [generate_uuid() for _ in range(10)]


if __name__ == "__main__":
    print(generate_10_uuid())
