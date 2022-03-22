import pandas as pd
df = pd.read_csv('youshu_edges.csv')
df1 = df.sample(frac =.01)
print(len(df1))
print(df1)
#here I sampled for hin2vec and it did help.
df1.to_csv("youshu_edges_sample.csv", index=False, sep=',')