import matplotlib.pyplot as plt
import networkx as nx

import gensim, logging

m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
if m.endswith('.vec.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
elif m.endswith('.bin.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
else:
    model = gensim.models.KeyedVectors.load(m)
model.init_sims(replace=True)

words = ['мыть_VERB','полоскать_VERB','стирать_VERB','замочить_VERB','замачивать_VERB','вымочить_VERB','вымачивать_VERB','мочить_VERB','чистить_VERB','сполоснуть_VERB','омыть_VERB','обмыть_VERB','мылить_VERB','намылить_VERB','отмачивать_VERB','застирать_VERB','промыть_VERB']

G = nx.Graph()

for i in range(len(words)):
	if words[i] in model:
		G.add_node(words[i])
	else:
		print(words[i] + ' is not present in the model')

for alpha in range(len(list(G.nodes()))):
		for beta in range(len(list(G.nodes()))):
			if beta > alpha:
				try:
					if model.similarity(list(G.nodes())[beta], list(G.nodes())[alpha]) > 0.5 or model.similarity(list(G.nodes())[alpha], list(G.nodes())[beta]) > 0.5:
						G.add_edge(list(G.nodes())[alpha],list(G.nodes())[beta])
				except:
					pass

rads = [nx.radius(subgraph) for subgraph in sorted(nx.connected_component_subgraphs(G), key=len) if len(subgraph) > 1]
print("Радиус(ы):")
for radius in rads:
	print(radius)

deg = nx.degree_centrality(G)
degrees = sorted(deg, key=deg.get, reverse=True)
print("Самые центральные слова:")
for i in range(3):
	print(degrees[i])

print("Коэффициент кластеризации:",nx.average_clustering(G))

pos=nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color='blue', node_size=50)
nx.draw_networkx_edges(G, pos, edge_color='blue')
nx.draw_networkx_labels(G, pos, font_size=10, font_family='Arial')
plt.axis('off')
plt.show()