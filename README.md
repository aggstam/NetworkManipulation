# NetworkManipulation
This python script performs fundamental social network analysis tasks on the temporal network graph for the StackOverflow-related dataset [1].
<br>
On each execution, a dedicated folder is created containing all result files.
<br>
Script calculates tmin and tmax timestamps and splits records in N sub-networks.
<br>
For each sub-network, the following are calculated:
- Various centralities (e.g. Degree, Closeness, Eigenvector, etc.)
- Similarity tables (e.g. Graph Distance, Jaccard's Coefficient, etc.)
- Metrics predictions of consecutive sub-networks

## Dependencies
- Python 3.8.5(x64)
- numpy latest
- networkx latest
- pandas latest
- matplotlib latest
- scipy latest

## Usage
Before executing any script, create a `python` virtual environment
and source it:
```shell
$ python -m venv venv
$ source venv/bin/activate
```
Install required dependencies:
```shell
$ pip install -r requirements.txt
```
A test network file(sub-set) has been provided to play with!
<br>
Execute the script:
```shell
$ python NetworkManipulation.py
```

## Execution example
```shell
$ python NetworkManipulation.py
Welcome to Network Analysis application.
Please provide the network file path: test-network.txt
Please provide N (int) for splitting the network to time periods: 5
Please provide the following metric weights in 0.xx format (e.g 50% -> 0.50):
Pgd -> 0.50
Pcn -> 0.50
Pjc -> 0.50
Pa -> 0.50
Ppa -> 0.50

Execution starting...

Reading network file test-network.txt...
Network loaded.

Creating outputs folder...
Outputs folder 2023_01_22_15_44_53 created.

Creating Network Graph figure file...
Network Graph figure file Network_Graph.png created.

Network information:
	Nodes: 434
	Edges: 448
	Earliest Network node: User 4550 connected with user 4550 on 2008-09-06 22:26:30.
	Latest Network node: User 3171 connected with user 6180 on 2008-09-16 18:27:45.

Creating 5 sub-networks...
	Period 0: [2008-09-06 22:26:30, 2008-09-08 21:38:45)
	Period 1: [2008-09-08 21:38:45, 2008-09-10 20:51:00)
	Period 2: [2008-09-10 20:51:00, 2008-09-12 20:03:15)
	Period 3: [2008-09-12 20:03:15, 2008-09-14 19:15:30)
	Period 4: [2008-09-14 19:15:30, 2008-09-16 18:27:45]
Sub-networks created.

Creating Sub-Networks files...
	Graph figure file Period_0_Sub_Network_Graph.png created.
	Adjacency matrix file Period_0_Sub_Network_Adjacency_Matrix.csv created.
	Graph figure file Period_1_Sub_Network_Graph.png created.
	Adjacency matrix file Period_1_Sub_Network_Adjacency_Matrix.csv created.
	Graph figure file Period_2_Sub_Network_Graph.png created.
	Adjacency matrix file Period_2_Sub_Network_Adjacency_Matrix.csv created.
	Graph figure file Period_3_Sub_Network_Graph.png created.
	Adjacency matrix file Period_3_Sub_Network_Adjacency_Matrix.csv created.
	Graph figure file Period_4_Sub_Network_Graph.png created.
	Adjacency matrix file Period_4_Sub_Network_Adjacency_Matrix.csv created.
Sub-Networks files created.

Creating Sub-Networks Centrality Distribution files...
	Degree Centrality Distribution file Period_0_Sub_Network_Degree_Centrality_Distribution.png created.
	InDegree Centrality Distribution file Period_0_Sub_Network_InDegree_Centrality_Distribution.png created.
	OutDegree Centrality Distribution file Period_0_Sub_Network_OutDegree_Centrality_Distribution.png created.
	Closeness Centrality Distribution file Period_0_Sub_Network_Closeness_Centrality_Distribution.png created.
	Betweenness Centrality Distribution file Period_0_Sub_Network_Betweenness_Centrality_Distribution.png created.
	Eigenvector Centrality Distribution file Period_0_Sub_Network_Eigenvector_Centrality_Distribution.png created.
	Katz Centrality Distribution file Period_0_Sub_Network_Katz_Centrality_Distribution.png created.
	Degree Centrality Distribution file Period_1_Sub_Network_Degree_Centrality_Distribution.png created.
	InDegree Centrality Distribution file Period_1_Sub_Network_InDegree_Centrality_Distribution.png created.
	OutDegree Centrality Distribution file Period_1_Sub_Network_OutDegree_Centrality_Distribution.png created.
	Closeness Centrality Distribution file Period_1_Sub_Network_Closeness_Centrality_Distribution.png created.
	Betweenness Centrality Distribution file Period_1_Sub_Network_Betweenness_Centrality_Distribution.png created.
	Eigenvector Centrality Distribution file Period_1_Sub_Network_Eigenvector_Centrality_Distribution.png created.
	Katz Centrality Distribution file Period_1_Sub_Network_Katz_Centrality_Distribution.png created.
	Degree Centrality Distribution file Period_2_Sub_Network_Degree_Centrality_Distribution.png created.
	InDegree Centrality Distribution file Period_2_Sub_Network_InDegree_Centrality_Distribution.png created.
	OutDegree Centrality Distribution file Period_2_Sub_Network_OutDegree_Centrality_Distribution.png created.
	Closeness Centrality Distribution file Period_2_Sub_Network_Closeness_Centrality_Distribution.png created.
	Betweenness Centrality Distribution file Period_2_Sub_Network_Betweenness_Centrality_Distribution.png created.
	Eigenvector Centrality Distribution file Period_2_Sub_Network_Eigenvector_Centrality_Distribution.png created.
	Katz Centrality Distribution file Period_2_Sub_Network_Katz_Centrality_Distribution.png created.
	Degree Centrality Distribution file Period_3_Sub_Network_Degree_Centrality_Distribution.png created.
	InDegree Centrality Distribution file Period_3_Sub_Network_InDegree_Centrality_Distribution.png created.
	OutDegree Centrality Distribution file Period_3_Sub_Network_OutDegree_Centrality_Distribution.png created.
	Closeness Centrality Distribution file Period_3_Sub_Network_Closeness_Centrality_Distribution.png created.
	Betweenness Centrality Distribution file Period_3_Sub_Network_Betweenness_Centrality_Distribution.png created.
	Eigenvector Centrality Distribution file Period_3_Sub_Network_Eigenvector_Centrality_Distribution.png created.
	Katz Centrality Distribution file Period_3_Sub_Network_Katz_Centrality_Distribution.png created.
	Degree Centrality Distribution file Period_4_Sub_Network_Degree_Centrality_Distribution.png created.
	InDegree Centrality Distribution file Period_4_Sub_Network_InDegree_Centrality_Distribution.png created.
	OutDegree Centrality Distribution file Period_4_Sub_Network_OutDegree_Centrality_Distribution.png created.
	Closeness Centrality Distribution file Period_4_Sub_Network_Closeness_Centrality_Distribution.png created.
	Betweenness Centrality Distribution file Period_4_Sub_Network_Betweenness_Centrality_Distribution.png created.
	Eigenvector Centrality Distribution file Period_4_Sub_Network_Eigenvector_Centrality_Distribution.png created.
	Katz Centrality Distribution file Period_4_Sub_Network_Katz_Centrality_Distribution.png created.
Sub-Networks Centrality Distribution files created.

Creating consecutive sub-networks files...
	File V[t0,t2].txt created.
	File E[t0,t1].txt created.
	File E[t1,t2].txt created.
	File V[t1,t3].txt created.
	File E[t1,t2].txt created.
	File E[t2,t3].txt created.
	File V[t2,t4].txt created.
	File E[t2,t3].txt created.
	File E[t3,t4].txt created.
	File V[t3,t5].txt created.
	File E[t3,t4].txt created.
	File E[t4,t5].txt created.
Consecutive sub-networks files created.

Creating consecutive sub-networks similarity tables files...
	File Consecutive_Sub_Networks_0_and_1_Graph_Distances.csv created.
	File Consecutive_Sub_Networks_0_and_1_Common_Neighbors.csv created.
	File Consecutive_Sub_Networks_0_and_1_Jaccards_Coefficient.csv created.
	File Consecutive_Sub_Networks_0_and_1_Adamic_Adar.csv created.
	File Consecutive_Sub_Networks_0_and_1_Preferential_Attachment.csv created.
	File Consecutive_Sub_Networks_1_and_2_Graph_Distances.csv created.
	File Consecutive_Sub_Networks_1_and_2_Common_Neighbors.csv created.
	File Consecutive_Sub_Networks_1_and_2_Jaccards_Coefficient.csv created.
	File Consecutive_Sub_Networks_1_and_2_Adamic_Adar.csv created.
	File Consecutive_Sub_Networks_1_and_2_Preferential_Attachment.csv created.
	File Consecutive_Sub_Networks_2_and_3_Graph_Distances.csv created.
	File Consecutive_Sub_Networks_2_and_3_Common_Neighbors.csv created.
	File Consecutive_Sub_Networks_2_and_3_Jaccards_Coefficient.csv created.
	File Consecutive_Sub_Networks_2_and_3_Adamic_Adar.csv created.
	File Consecutive_Sub_Networks_2_and_3_Preferential_Attachment.csv created.
	File Consecutive_Sub_Networks_3_and_4_Graph_Distances.csv created.
	File Consecutive_Sub_Networks_3_and_4_Common_Neighbors.csv created.
	File Consecutive_Sub_Networks_3_and_4_Jaccards_Coefficient.csv created.
	File Consecutive_Sub_Networks_3_and_4_Adamic_Adar.csv created.
	File Consecutive_Sub_Networks_3_and_4_Preferential_Attachment.csv created.
Consecutive sub-networks similarity tables files created.

Creating consecutive sub-networks similarity metrics predictions files...
	Prediction metrics weights: Pgd = 0.50, Pcn = 0.50, Pjc = 0.50, Pa = 0.50, Ppa = 0.50
	File Consecutive_Sub_Networks_0_and_1_Graph_Distances_Predictions.txt created.
	File Consecutive_Sub_Networks_0_and_1_Common_Neighbors_Predictions.txt created.
	File Consecutive_Sub_Networks_0_and_1_Jaccards_Coefficient_Predictions.txt created.
	File Consecutive_Sub_Networks_0_and_1_Adamic_Adar_Predictions.txt created.
	File Consecutive_Sub_Networks_0_and_1_Preferential_Attachment_Predictions.txt created.
	File Consecutive_Sub_Networks_1_and_2_Graph_Distances_Predictions.txt created.
	File Consecutive_Sub_Networks_1_and_2_Common_Neighbors_Predictions.txt created.
	File Consecutive_Sub_Networks_1_and_2_Jaccards_Coefficient_Predictions.txt created.
	File Consecutive_Sub_Networks_1_and_2_Adamic_Adar_Predictions.txt created.
	File Consecutive_Sub_Networks_1_and_2_Preferential_Attachment_Predictions.txt created.
	File Consecutive_Sub_Networks_2_and_3_Graph_Distances_Predictions.txt created.
	File Consecutive_Sub_Networks_2_and_3_Common_Neighbors_Predictions.txt created.
	File Consecutive_Sub_Networks_2_and_3_Jaccards_Coefficient_Predictions.txt created.
	File Consecutive_Sub_Networks_2_and_3_Adamic_Adar_Predictions.txt created.
	File Consecutive_Sub_Networks_2_and_3_Preferential_Attachment_Predictions.txt created.
	File Consecutive_Sub_Networks_3_and_4_Graph_Distances_Predictions.txt created.
	File Consecutive_Sub_Networks_3_and_4_Common_Neighbors_Predictions.txt created.
	File Consecutive_Sub_Networks_3_and_4_Jaccards_Coefficient_Predictions.txt created.
	File Consecutive_Sub_Networks_3_and_4_Adamic_Adar_Predictions.txt created.
	File Consecutive_Sub_Networks_3_and_4_Preferential_Attachment_Predictions.txt created.
Consecutive sub-networks similarity metrics predictions files created.

Execution finished!
```

## References
[1] https://snap.stanford.edu/data/sx-stackoverflow.html
