import pandas as pd
import numpy as np
object = pd.read_pickle('adj_matrix.p')
print(object)
print(type(object))
print(object.shape[0])