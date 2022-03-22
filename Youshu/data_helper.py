"""
@author: Branco François and Louis Lanckriet
"""

import pandas as pd

# Making link.dat
bundle_item = pd.read_csv('bundle_item.txt', sep="\t", header=None)
user_bundle = pd.read_csv('user_bundle.txt', sep="\t", header=None)
user_item = pd.read_csv('user_item.txt', sep="\t", header=None)

link_list = []
for index, row in bundle_item.iterrows():
    link_list.append([1000000 + row[0], 2000000 + row[1]])

for index, row in user_bundle.iterrows():
    link_list.append([3000000 + row[0], 1000000 + row[1]])

for index, row in user_item.iterrows():
    link_list.append([3000000 + row[0], 2000000 + row[1]])

df = pd.DataFrame(link_list)

#Here we sampled the data, but it did not affect the memory issue
df = df.sample(frac =.01)
df.to_csv("link.dat", index=False, header=False, sep=' ')

#making node.dat
node_list = []
for index, row in df.iterrows():
    # For column 1
    # type 1 is a bundle
    if row[0] < 2000000:
        node_list.append([row[0], 'some-bundle-name', 1])
    # type 2 is an item
    elif (row[0] >= 2000000) and (row[0] <= 3000000):
        node_list.append([row[0], 'some-item-name', 2])
    # type 3 is a user
    else:
        node_list.append([row[0], 'some-user-name', 0])

    # For column 2
    # type 1 is a bundle
    if row[1] < 2000000:
        node_list.append([row[1], 'some-bundle-name', 1])
    # type 2 is an item
    elif (row[1] >= 2000000) and (row[1] < 3000000):
        node_list.append([row[1], 'some-item-name', 2])
    # type 3 is a user
    else:
        node_list.append([row[1], 'some-user-name', 0])

df2 = pd.DataFrame(node_list)
df2 = df2.drop_duplicates()
df2.columns = ['number', 'info', 'type']
df2 = df2.sort_values(by=['number'])
df2.to_csv("node.dat", index=False, header=False, sep=' ')

#making youshu_edges.csv
edges_list = []
for index, row in df.iterrows():
    #edge of type bundle-item
    if (row[0] < 2000000) and ((row[1] >= 2000000) and (row[1] < 3000000)):
        edges_list.append([row[0], row[1], 1, 1, 2, '1-2'])
    #edge of type user-bundle
    elif (row[0] <= 3000000) and (row[1] < 2000000):
        edges_list.append([row[0], row[1], 1, 3, 1, '0-1'])
    # edge of type user-item
    else:
        edges_list.append([row[0], row[1], 1, 3, 2, '0-2'])

df3 = pd.DataFrame(edges_list)
df3.columns = ['dest_node', 'source_node', 'weight', 'source_class', 'dest_class', 'edge_class']
df3.to_csv("youshu_edges.csv", index=False, sep=',')

print("IT'S DONE")
