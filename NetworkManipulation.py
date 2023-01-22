# --------------------------------------------------------------------------
#
# This script performs fundamental social network analysis tasks
# on the temporal  network graph for the StackOverflow-related dataset.
# On each execution, a dedicated folder is created containing all result files.
#
# Author: Aggelos Stamatiou, November 2020
#
# --------------------------------------------------------------------------

import sys
import os
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import operator as op
from datetime import datetime
from math import log

# Util printing function.
def printf(format, *args):
    sys.stdout.write(format % args)

# Creates a figure file containing the distribution histogram of a given degrees array.
def PlotCentralityDistribution(Index, Type, Degrees):
    plt.hist(Degrees.values());
    plt.xlabel('Degrees');
    plt.ylabel('Absolute Frequency');
    plt.savefig('Period_{0}_Sub_Network_{1}_Centrality_Distribution.png'.format(Index, Type));
    printf('\t%s Centrality Distribution file Period_%d_Sub_Network_%s_Centrality_Distribution.png created.\n', Type, Index, Type);

# Computes Graph Distance metric: S_GD=[S_GD (u,v)]=-Length of Shortest Path Between u and v
def graph_distances(G):
    Sgd = dict();
    for source in G.nodes():
        Sgd[source] = dict();
        for target in G.nodes():
            Sgd[source][target] = 0;
            if nx.has_path(G, source, target):
                Sgd[source][target] = nx.shortest_path_length(G, source, target);
    return Sgd;

# Computes Common Neighbors metric: S_CN=[S_CN (u,v)]=|Γ(u)∩Γ(v)|
def common_neighbors(G):
    Scn = dict();
    cn = dict();
    for source in G.nodes():
        Scn[source] = dict();
        cn[source] = dict();
        for target in G.nodes():
            if (target != source):
                target_neighborhood = list(G.successors(target)) + list(G.predecessors(target));
                if (source in target_neighborhood):
                    for neighbor in target_neighborhood:
                        if ((neighbor != source) & (neighbor != target)):
                            if (neighbor not in Scn[source]):
                                Scn[source][neighbor] = 0;
                            if (neighbor not in cn[source]):
                                cn[source][neighbor] = [];
                            Scn[source][neighbor] += 1;
                            cn[source][neighbor].append(target);
    return Scn, cn;

# Computes Jaccard's Coefficient metric: S_JC=[S_JC (u,v)]=(|Γ(u)∩Γ(v)|)/(|Γ(u)UΓ(v)|)
def jaccards_coefficient(G, Scn):
    Sjc = dict();
    for source in G.nodes():
        Sjc[source] = dict();
        for target in G.nodes():
            source_neighborhood = list(G.successors(source)) + list(G.predecessors(source));
            target_neighborhood = list(G.successors(target)) + list(G.predecessors(target));
            union_len = len(list(set().union(source_neighborhood, target_neighborhood)));
            Sjc[source][target] = 0; # <-- 0 h 1????
            if ((union_len > 0) & (Scn[source] is not None) & (target in Scn[source].keys())):
                Sjc[source][target] = Scn[source][target]/union_len;
    return Sjc;

# Computes Adamic/Adar metric: S_A=[S_A (u,v)]=∑_(z∈Γ(u)∩Γ(v))▒1/(log⁡(|Γ(z)|))
def adamic_adar(G, common_neighbors):
    Sa = dict();
    for source in G.nodes():
        Sa[source] = dict();
        for target in G.nodes():
            if (target not in common_neighbors[source]):
                Sa[source][target] = 0;
            else:
                Sa[source][target] = sum(1 / log(G.degree(neighbor)) for neighbor in common_neighbors[source][target]);
    return Sa;

# Computes Preferiential Attachment metric: S_PA=[S_PA (u,v)]=|Γ(u)|*|Γ(v)|
def preferential_attachment(G):
    Spa = dict();
    for source in G.nodes():
        Spa[source] = dict();
        for target in G.nodes():
            Spa[source][target] = G.degree(source) * G.degree(target);
    return Spa;

# For a given similarity metric table:
#   1. Extract table max value.
#   2. Find which pairs of nodes have the max value.
#   3. Predict next period edges: If S(x) >= Prediction_Weight * max for two nodes, edge is created.
#   4. Compute prediction success rate.
#   4. Write results in a file.
def similiraty_metric_predictions(file, Type, Similarity_Table, Prediction_Weight, Previous_Period_Edges, Next_Period_Edges):
    Sx_max = 0;
    for k in Similarity_Table:
        if (len(Similarity_Table[k].items()) > 0):
            dict_max = max(Similarity_Table[k].items(), key=op.itemgetter(1))[1];
            if (dict_max > Sx_max):
                Sx_max = dict_max;
    Prediction_Limit = Prediction_Weight * Sx_max;
    max_items_list = [];
    predicted_items = [];
    for k in Similarity_Table:
        for key, value in Similarity_Table[k].items():
            if (value == Sx_max):
                max_items_list.append((k, key));
            elif ((value >= Prediction_Limit) & ((k, key) not in Previous_Period_Edges)):
                predicted_items.append((k, key));
    counter = 0;
    for predicted_item in predicted_items:
        if (predicted_item in Next_Period_Edges):
            counter += 1;
    percentage = (counter/len(predicted_items)) * 100 if (len(predicted_items) > 0) else 0;
    with open(file, 'w') as f:
        f.write('S{0} max = {1}\n'.format(Type, Sx_max));
        f.write('Nodes:');
        for item in max_items_list:
            f.write(' {0}'.format(item));
        f.write('\n');
        f.write('Next period predicted edges:');
        for item in predicted_items:
            f.write(' {0}'.format(item));
        f.write('\n');
        f.write('SP{0}% = {1}\n'.format(Type, percentage));

# Writes given Dictionary to a CSV file.
def write_dictionary_to_csv(File, Dict):
    with open(File, 'w') as f:
        for key in Dict.keys():
            f.write(',{0}'.format(key));
        f.write('\n');
        for key in Dict.keys():
            f.write('{0}'.format(key));
            for value in Dict[key].values():
                f.write(',{0}'.format(value));
            f.write('\n');

#####################################################

# Retrieving required execution parameters.
network_file = input('Welcome to Network Analysis application.\nPlease provide the network file path: ');
N = int(input('Please provide N (int) for splitting the network to time periods: '));
# Metric weights.
Pgd = float(input('Please provide the following metric weights in 0.xx format (e.g 50% -> 0.50):\nPgd ->'));
Pcn = float(input('Pcn -> '));
Pjc = float(input('Pjc -> '));
Pa = float(input('Pa -> '));
Ppa = float(input('Ppa -> '));
print('\nExecution starting...');

# Load network from file.
printf('\nReading network file %s...\n', network_file);
Network = pd.read_csv(network_file, sep=" ", header=None);
Network.columns = ['user0', 'user1', 'timestamp']
print('Network loaded.');
NetworkGraph=nx.from_pandas_edgelist(Network, 'user0', 'user1', create_using=nx.DiGraph());

# Create outputs folder.
print('\nCreating outputs folder...');
output_folder = datetime.now().strftime("%Y_%m_%d_%H_%M_%S");
os.mkdir(output_folder);
os.chdir(output_folder);
printf('Outputs folder %s created.\n', output_folder);

# Visualize network graph in file.
print('\nCreating Network Graph figure file...');
nx.draw(NetworkGraph, with_labels=True);
plt.savefig('Network_Graph.png');
print('Network Graph figure file Network_Graph.png created.');

# Find min and max node creation timestamps and display network information. (1)
printf('\nNetwork information:\n\tNodes: %d\n\tEdges: %d\n', len(NetworkGraph.nodes()), len(NetworkGraph.edges()));
min_idx = Network['timestamp'].idxmin();
user1 = Network.iloc[min_idx].iloc[0];
user2 = Network.iloc[min_idx].iloc[1];
min_timestamp = Network.iloc[min_idx].iloc[2];
date = datetime.fromtimestamp(min_timestamp);
printf('\tEarliest Network node: User %d connected with user %d on %s.\n', user1, user2, date);
max_idx = Network['timestamp'].idxmax();
user1 = Network.iloc[max_idx].iloc[0];
user2 = Network.iloc[max_idx].iloc[1];
max_timestamp = Network.iloc[max_idx].iloc[2];
date = datetime.fromtimestamp(max_timestamp);
printf('\tLatest Network node: User %d connected with user %d on %s.\n', user1, user2, date);

# N time periods computation and Sub-Networks creation. (2)
DT = max_timestamp - min_timestamp;
dT = DT/N;

# Compute boundaries.
TJs = [];
for j in range(N):
    TJs.append(min_timestamp + j*dT);

# Sub-networks creation.
printf('\nCreating %d sub-networks...\n', N);
Sub_Networks = [];
for j in range(N-1):
    period_start = datetime.fromtimestamp(TJs[j]);
    period_end = datetime.fromtimestamp(TJs[j+1]);
    printf('\tPeriod %d: [%s, %s)\n', j, period_start,period_end);
    Sub_Networks.append(Network.loc[(Network['timestamp'] >= TJs[j]) & (Network['timestamp'] < TJs[j+1])]);

period_start = datetime.fromtimestamp(TJs[N-1]);
period_end = datetime.fromtimestamp(max_timestamp);
printf('\tPeriod %d: [%s, %s]\n', N-1, period_start, period_end);
Sub_Networks.append(Network[Network['timestamp'] >= TJs[N-1]]);
print('Sub-networks created.\n');

# Sub-networks graph figure and adjacency matrix files creation. (3)
Sub_Networks_Graphs = [];
print('Creating Sub-Networks files...');
for j in range(N):
    period_folder = 'Period_{0}_Sub_Network'.format(j);
    os.mkdir(period_folder);
    os.chdir(period_folder);
    plt.clf();
    G=nx.from_pandas_edgelist(Sub_Networks[j], 'user0', 'user1', create_using=nx.DiGraph());
    nx.draw(G, with_labels=True);
    plt.savefig('Graph.png');
    Sub_Networks_Graphs.append(G);
    printf('\tGraph figure file Period_%d_Sub_Network_Graph.png created.\n', j);
    nx.to_pandas_adjacency(G).to_csv('Period_{0}_Sub_Network_Adjacency_Matrix.csv'.format(j));
    printf('\tAdjacency matrix file Period_%d_Sub_Network_Adjacency_Matrix.csv created.\n', j);
    os.chdir('../');
print('Sub-Networks files created.\n');

# Sub-networks centralities files creation. (4)
print('Creating Sub-Networks Centrality Distribution files...');
for j in range(N):
    period_folder = 'Period_{0}_Sub_Network'.format(j);
    os.chdir(period_folder);
    plt.clf();
    PlotCentralityDistribution(j, 'Degree', nx.degree_centrality(Sub_Networks_Graphs[j]));
    plt.clf();
    PlotCentralityDistribution(j, 'InDegree', nx.in_degree_centrality(Sub_Networks_Graphs[j]));
    plt.clf();
    PlotCentralityDistribution(j, 'OutDegree', nx.out_degree_centrality(Sub_Networks_Graphs[j]));
    plt.clf();
    PlotCentralityDistribution(j, 'Closeness', nx.closeness_centrality(Sub_Networks_Graphs[j]));
    plt.clf();
    PlotCentralityDistribution(j, 'Betweenness', nx.betweenness_centrality(Sub_Networks_Graphs[j]));
    plt.clf();
    PlotCentralityDistribution(j, 'Eigenvector', nx.eigenvector_centrality_numpy(Sub_Networks_Graphs[j]));
    plt.clf();
    PlotCentralityDistribution(j, 'Katz', nx.katz_centrality_numpy(Sub_Networks_Graphs[j]));
    os.chdir('../');
print('Sub-Networks Centrality Distribution files created.\n');

# V*[tj-1,tj+1], E*[tj-1,tj] and E*[tj,tj+1] computation of consecutive sub-networks. (5)
print('Creating consecutive sub-networks files...');
Consecutive_Sub_Networks_Graphs = [];
Consecutive_Sub_Networks_Graphs_G1_Edges = [];
for j in range(1,N):
    consecutive_sub_networks_folder = 'Consecutive_Sub_Networks_{0}_and_{1}'.format(j-1, j);
    os.mkdir(consecutive_sub_networks_folder);
    os.chdir(consecutive_sub_networks_folder);
    G = nx.DiGraph()
    common_nodes = set(Sub_Networks_Graphs[j-1].nodes()).intersection(set(Sub_Networks_Graphs[j].nodes()));
    with open('V[t{0},t{1}].txt'.format(j-1, j+1), 'w') as f:
        f.writelines('%s\n' % common_node for common_node in common_nodes);
    printf('\tFile V[t%d,t%d].txt created.\n', j-1, j+1);
    G.add_nodes_from(common_nodes);
    # Retrieving all in and out edges of common nodes
    G0Edges = list(Sub_Networks_Graphs[j-1].out_edges(common_nodes)) + list(Sub_Networks_Graphs[j-1].in_edges(common_nodes));
    # Filtering list to contain edges that both nodes are in common nodes list. Also duplicates are removed.
    G0Edges = list(dict.fromkeys([(u,v) for u,v in G0Edges if (u in common_nodes) & (v in common_nodes)]));
    with open('E[t{0},t{1}].txt'.format(j-1, j), 'w') as f:
        f.writelines('%s\n' % str(G0Edge) for G0Edge in G0Edges);
    printf('\tFile E[t%d,t%d].txt created.\n', j-1, j);
    G.add_edges_from(G0Edges);
    G1Edges = list(Sub_Networks_Graphs[j].out_edges(common_nodes)) + list(Sub_Networks_Graphs[j].in_edges(common_nodes));
    G1Edges = list(dict.fromkeys([(u,v) for u,v in G1Edges if (u in common_nodes) & (v in common_nodes)]));
    with open('E[t{0},t{1}].txt'.format(j, j+1), 'w') as f:
        f.writelines('%s\n' % str(G1Edge) for G1Edge in G1Edges);
    printf('\tFile E[t%d,t%d].txt created.\n', j, j+1);
    Consecutive_Sub_Networks_Graphs_G1_Edges.append(G1Edges);
    Consecutive_Sub_Networks_Graphs.append(G);
    os.chdir('../');
print('Consecutive sub-networks files created.\n');

# Computation of similarity tables of consecutive sub-networks. (6)
print('Creating consecutive sub-networks similarity tables files...');
Sgd_List = [];
Scn_List = [];
Sjc_List = [];
Sa_List = [];
Spa_List = [];
for j in range(N-1):
    consecutive_sub_networks_folder = 'Consecutive_Sub_Networks_{0}_and_{1}'.format(j, j+1);
    os.chdir(consecutive_sub_networks_folder);
    Sgd = graph_distances(Consecutive_Sub_Networks_Graphs[j]);
    write_dictionary_to_csv('Consecutive_Sub_Networks_{0}_and_{1}_Graph_Distances.csv'.format(j, j+1), Sgd);
    printf('\tFile Consecutive_Sub_Networks_%d_and_%d_Graph_Distances.csv created.\n', j, j+1);
    Sgd_List.append(Sgd);
    [Scn,cn] = common_neighbors(Consecutive_Sub_Networks_Graphs[j]);
    write_dictionary_to_csv('Consecutive_Sub_Networks_{0}_and_{1}_Common_Neighbors.csv'.format(j, j+1), Scn);
    printf('\tFile Consecutive_Sub_Networks_%d_and_%d_Common_Neighbors.csv created.\n', j, j+1);
    Scn_List.append(Scn);
    Sjc = jaccards_coefficient(Consecutive_Sub_Networks_Graphs[j], Scn);
    write_dictionary_to_csv('Consecutive_Sub_Networks_{0}_and_{1}_Jaccards_Coefficient.csv'.format(j, j+1), Sjc);
    printf('\tFile Consecutive_Sub_Networks_%d_and_%d_Jaccards_Coefficient.csv created.\n', j, j+1);
    Sjc_List.append(Sjc);
    Sa = adamic_adar(Consecutive_Sub_Networks_Graphs[j], cn);
    write_dictionary_to_csv('Consecutive_Sub_Networks_{0}_and_{1}_Adamic_Adar.csv'.format(j, j+1), Sa);
    printf('\tFile Consecutive_Sub_Networks_%d_and_%d_Adamic_Adar.csv created.\n', j, j+1);
    Sa_List.append(Sa);
    Spa = preferential_attachment(Consecutive_Sub_Networks_Graphs[j]);
    write_dictionary_to_csv('Consecutive_Sub_Networks_{0}_and_{1}_Preferential_Attachment.csv'.format(j, j+1), Spa);
    printf('\tFile Consecutive_Sub_Networks_%d_and_%d_Preferential_Attachment.csv created.\n', j, j+1);
    Spa_List.append(Spa);
    os.chdir('../');
print('Consecutive sub-networks similarity tables files created.\n');

# Computation of similarity metrics predictions of consecutive sub-networks. (7)
print('Creating consecutive sub-networks similarity metrics predictions files...');
printf('\tPrediction metrics weights: Pgd = %0.2f, Pcn = %0.2f, Pjc = %0.2f, Pa = %0.2f, Ppa = %0.2f\n', Pgd, Pcn, Pjc, Pa, Ppa);
for j in range(N-1):
    consecutive_sub_networks_folder = 'Consecutive_Sub_Networks_{0}_and_{1}'.format(j, j+1);
    os.chdir(consecutive_sub_networks_folder);
    file='Consecutive_Sub_Networks_{0}_and_{1}_Graph_Distances_Predictions.txt'.format(j, j+1);
    similiraty_metric_predictions(file, 'gd', Sgd_List[j], Pgd, Consecutive_Sub_Networks_Graphs[j].edges(), Consecutive_Sub_Networks_Graphs_G1_Edges[j]);
    printf('\tFile %s created.\n', file);
    file='Consecutive_Sub_Networks_{0}_and_{1}_Common_Neighbors_Predictions.txt'.format(j, j+1);
    similiraty_metric_predictions(file, 'cn', Scn_List[j], Pcn, Consecutive_Sub_Networks_Graphs[j].edges(), Consecutive_Sub_Networks_Graphs_G1_Edges[j]);
    printf('\tFile %s created.\n', file);
    file='Consecutive_Sub_Networks_{0}_and_{1}_Jaccards_Coefficient_Predictions.txt'.format(j, j+1);
    similiraty_metric_predictions(file, 'jc', Sjc_List[j], Pjc, Consecutive_Sub_Networks_Graphs[j].edges(), Consecutive_Sub_Networks_Graphs_G1_Edges[j]);
    printf('\tFile %s created.\n', file);
    file='Consecutive_Sub_Networks_{0}_and_{1}_Adamic_Adar_Predictions.txt'.format(j, j+1);
    similiraty_metric_predictions(file, 'a', Sa_List[j], Pa, Consecutive_Sub_Networks_Graphs[j].edges(), Consecutive_Sub_Networks_Graphs_G1_Edges[j]);
    printf('\tFile %s created.\n', file);
    file='Consecutive_Sub_Networks_{0}_and_{1}_Preferential_Attachment_Predictions.txt'.format(j, j+1);
    similiraty_metric_predictions(file, 'pa', Spa_List[j], Ppa, Consecutive_Sub_Networks_Graphs[j].edges(), Consecutive_Sub_Networks_Graphs_G1_Edges[j]);
    printf('\tFile %s created.\n', file);
    os.chdir('../');
print('Consecutive sub-networks similarity metrics predictions files created.\n\nExecution finished!');
