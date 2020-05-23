#  I pledge my honor that I have abided by the Stevens Honor System
#  Author:  Brandon Patton 
#  Assignment 05 - Processing various csv files and evaluating triad network relationships based on trust
#  assign05.py [LIGHT DESCRIPTION OF WHAT PROGRAM CODE ACTUALLY DOES]

# To run from terminal window:   python3 assign05.py 
#           The program will then ask you to provide the path to the file you wish to process

import sys, csv
import pandas as pd 
import networkx as nx
from itertools import combinations as combs 


def graph_setup(data):
    new_Graph = nx.Graph()    #create an empty graph to work with
    for i, row in data.iterrows():
        reviewer = row['reviewer'] 
        reviewee = row['reviewee']
        trust = row['trust']

        new_Graph.add_node(reviewer)
        new_Graph.add_node(reviewee)
        new_Graph.add_edge(reviewer, reviewee, weight = trust)
    return new_Graph

def self_loops(graph):
    count = 0
    for rev, rwe, trust in graph.edges(data=True):
        count += 1 if rev == rwe else 0
    return count

def trust_eval(graph, totedges):
    trusted = 0
    not_trusted = 0

    for rev, rwe, trust in graph.edges(data=True): #set to true to guarantee 3-tuple return value
        if trust['weight'] == 1:
            trusted += 1
        if trust['weight'] == -1:
            not_trusted += 1
    print("Amount Trust Edges: ", trusted)
    print("Amount Distrust Edges: ", not_trusted)
    p_pos = round(trusted/totedges, 4)
    p_neg = round(1 - (trusted/totedges), 4)
    print("P(positive edge) = p: ", p_pos)
    print("P(negative edge) = 1 - p: ", p_neg)
  

    #expected and actual distributions
    triangles = nx.triangles(graph)
    t_count = sum(triangles.values())/3
    print("Amount of Triangles: ", t_count)

    #expected distribution
    print("\n-Expected Distribution-")
    print("Type\t|\tPercent\t|\tNumber")

    TTT_percent = round((p_pos ** 3) * 100,1)
    TTT_num = round((t_count * TTT_percent)/100,1)
    print("TTT\t|\t" + str(TTT_percent) + "\t|\t" + str(TTT_num))
    
    TTD_percent = round((p_pos ** 2 * p_neg * 3) * 100,1)
    TTD_num = round((t_count * TTD_percent)/100,1)
    print("TTD\t|\t" + str(TTD_percent) + "\t|\t" + str(TTD_num))
    
    TDD_percent= round((p_pos * (p_neg ** 2) * 3) * 100,1)
    TDD_num= round((t_count * TDD_percent)/100,1)
    print("TDD\t|\t" + str(TDD_percent) + "\t|\t" + str(TDD_num))
    
    
    DDD_percent= round((p_neg ** 3) * 100,1)
    DDD_num= round((t_count * DDD_percent)/100,1)
    print("DDD\t|\t" + str(DDD_percent) + "\t|\t" + str(DDD_num))
    
    print("Total\t|\t" + str(100) + "\t|\t" + str(t_count))

    #actual distribution

    print('\nTriads:')
    weight = nx.get_edge_attributes(graph, 'weight')
    Triads = [edge for edge in nx.enumerate_all_cliques(graph)if len(edge) == 3]
    triad_list = list(map(lambda edge: list(map(lambda edge: (edge, weight[edge]), combs(edge, 2))), Triads))
    TTT_count = 0
    TTD_count = 0
    TDD_count = 0
    DDD_count = 0
    
    for triad in triad_list:
        e1_weight = triad[0][1]
        e2_weight = triad[1][1]
        e3_weight = triad[2][1]
    
        #identify type based on weight
        if(e1_weight == 1 and e2_weight == 1 and e3_weight == 1):
            triad_type = "TTT"
            TTT_count += 1
        if(e1_weight == 1 and e2_weight == 1 and e3_weight == -1) or (e1_weight == -1 and e2_weight == 1 and e3_weight == 1) or (e1_weight == 1 and e2_weight == -1 and e3_weight == 1):
            triad_type = "TTD"
            TTD_count += 1
        if(e1_weight == -1 and e2_weight == -1 and e3_weight == 1) or (e1_weight == 1 and e2_weight == -1 and e3_weight == -1) or (e1_weight == -1 and e2_weight == 1 and e3_weight == -1):
            triad_type = "TDD"
            TDD_count += 1 
        if(e1_weight == -1 and e2_weight == -1 and e3_weight == -1):
            triad_type = "DDD"
            DDD_count += 1
        print(triad_type + "\t|\t" + str(triad[0]) + "\t|\t" + str(triad[1]) + "\t|\t" + str(triad[2]))
    
    TTT_percent = round((TTT_count *100)/t_count, 1)
    TTD_percent = round((TTD_count *100)/t_count, 1)
    TDD_percent = round((TDD_count *100)/t_count, 1)
    DDD_percent = round((DDD_count *100)/t_count, 1)

    print("\nActual Distribution:")

    print("Type\t|\tpercent\t|\tnumber")
    print("TTT\t|\t" + str(TTT_percent) + "\t|\t" + str(TTT_count))
    print("TTD\t|\t" + str(TTD_percent) + "\t|\t" + str(TTD_count))
    print("TDD\t|\t" + str(TDD_percent) + "\t|\t" + str(TDD_count))
    print("DDD\t|\t" + str(DDD_percent) + "\t|\t" + str(DDD_count))
    print("Total\t|\t" + str(100) + "\t|\t" + str(t_count))

def do_requirements(data):
    #Does all the requirements in the spec in order specified, numbered below for convenience
    #Most are facilitated by helper functions created specifically for each task
    data_graph = graph_setup(data)
    nodes = data_graph.number_of_nodes()
    edges = data_graph.number_of_edges()            #Req 1
    s_Loops = self_loops(data_graph)                #Req 2
    totedges = edges - s_Loops
    print("Amount of Nodes: ", nodes)        
    print("Amount of Edges: ", edges)
    print("Amount of Self Loops: ", s_Loops)
    print("TotEdges: ", totedges)                   #Req 3
    trust_eval(data_graph, totedges)                #Req 4, 5, 6, 7, 8, and 9

def main():
    
    print("Please provide the path to the file you wish to process: ")
    input_file = input()
    graph_data = pd.read_csv(input_file, names = ["reviewer", "reviewee", "trust"])
    do_requirements(graph_data)



main()