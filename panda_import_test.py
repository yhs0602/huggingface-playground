import numpy as np
from numpy import random
import torch
from torch import nn
import pandas as pd
from pandas import DataFrame


def my_function():
    arr = np.array([1, 2, 3])
    tensor = torch.tensor([4, 5, 6])
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    print(random.randn(3, 3))
    print(nn.functional.relu(tensor))


if __name__ == "__main__":
    my_function()
