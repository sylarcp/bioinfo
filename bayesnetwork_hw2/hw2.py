import bisect
import copy
import random
from math import exp, log

def fill_table(child,parents,data):
	
	if len(parents)==0:
		count_positive=0
		count=0
	 	for row in data:	
 			count +=1
 			if row[child]==1:
 				count_positive +=1
 		if count==0:
 			count=100000   #if total count is 0, means any probabilty will not affect the score of graph. 
 		table=count_positive/float(count)
 	elif len(parents)==1:
 		table=[0 for x in range(2)] 
 		for i in xrange(0,2):
 			count_positive=0
			count=0
	 		for row in data:		
	 			if row[parents[0]]==i:
	 				count +=1
	 				if row[child]==1:
	 					count_positive +=1
	 		if count==0:
 				count=100000   #if total count is 0, means any probabilty will not affect the score of graph.
	 		table[i]=count_positive/float(count)
	elif len(parents)==2:
		table=[[0 for x in range(2)] for x in range(2)]
		for i in xrange(0,2):
			for j in xrange(0,2):
				count_positive=0
				count=0
		 		for row in data:		
		 			if row[parents[0]]==i and row[parents[1]]==j:
		 				# print parents
		 				# print parents[0]
		 				count +=1
		 				if row[child]==1:
		 					count_positive +=1
		 		if count==0:
 					count=100000   #if total count is 0, means any probabilty will not affect the score of graph.
		 		table[i][j]=count_positive/float(count)
	elif len(parents)==3:
		table=[[[0 for x in range(2)] for x in range(2)] for x in range(2)]
		for i in xrange(0,2):
			for j in xrange(0,2):
				for k in xrange(0,2):
					count_positive=0
					count=0
					for row in data:
						if row[parents[0]]==i and row[parents[1]]==j and row[parents[2]]==k:
							count +=1
							if row[child]==1:
								count_positive +=1
					if count==0:
 						count=100000   #if total count is 0, means any probabilty will not affect the score of graph.
					table[i][j][k]=count_positive/float(count)
	else:
		print "Error!!! More than 3 parents nodes exist!"
	return table

def score(net,data):
	score=0
	for row in data:
		for n in range(len(row)):
			parents=net['graph_pa'][n] #nth node's parents
			table=net['prob_tables'][n] #nth node's table
			if len(parents)==0:
				if row[n]==1:
					score += log(table) #might overflow
				elif row[n]==0:
					score += log(1-table) 
			elif len(parents)==1:
				i=row[parents[0]]
				if row[n]==1:
					score += log(table[i])
				if row[n]==0:
					score += log(1-table[i])
			elif len(parents)==2:
				i=row[parents[0]]
				j=row[parents[1]]
				if row[n]==1:
					score += log(table[i][j])
				if row[n]==0:
					score += log(1-table[i][j])
			elif len(parents)==3:
				i=row[parents[0]]
				j=row[parents[1]]
				k=row[parents[2]]
				if row[n]==1:
					score += log(table[i][j][k])
				if row[n]==0:
					score += log(1-table[i][j][k])
	return score
# before adding the edge, check whether the graph contains a path
# This way is much faster than checking whether the whole graph contains cycle.
def contain_path(graph,node1,node2):
	if node2 in graph[node1]:
		return 1
	if graph[node1]==[]:
		return 0
	exist=0
	for node in graph[node1]:
		exist += contain_path(graph,node,node2) #recursive
	return exist
#add edge from node1 to node2
def add_edge(net_origin, data, node1, node2):
	#deepcopy to save the origin one
	net=copy.deepcopy(net_origin)
	if node2 not in net['graph'][node1]:
	 	bisect.insort(net['graph'][node1],node2) #put node2 into graph['node1'] in order
	if node1 not in net['graph_pa'][node2]:
	 	bisect.insort(net['graph_pa'][node2],node1) #put node1 into graph_pa['node2'] in order
	 	parents_list=net['graph_pa'][node2]
	 	if len(parents_list)>3:
	 		return 0
	 	net['prob_tables'][node2]=fill_table(node2,parents_list, data)
	# only need to check wheter the original graph contain a path from node2 to node1
	#if the path exist, return 0
	#else return the net with new edge
	if contain_path(net_origin['graph'],node2,node1): return 0
	else: return net

#remove edge from node1 to node2
def remove_edge(net_origin, data, node1, node2):
	#deepcopy to save the origin one
	net=copy.deepcopy(net_origin)
	net['graph'][node1].remove(node2) 
	net['graph_pa'][node2].remove(node1)
	parents_list=net['graph_pa'][node2]
 	net['prob_tables'][node2]=fill_table(node2,parents_list, data) 	
	return net

def predict(net,data,child):
	parents=net['graph_pa'][child]
	table=net['prob_tables'][child]
	count=0
	correct=0
	if len(parents)==0:
		for row in data:	
 			count +=1
 			if int(2*table)==row[child]:
 				correct +=1
	elif len(parents)==1:
		for row in data:
			i=row[parents[0]]
 			count +=1
 			if int(2*table[i])==row[child]:
 				correct +=1
 	elif len(parents)==2:
		for row in data:
			i=row[parents[0]]
			j=row[parents[1]]	
 			count +=1
 			if int(2*table[i][j])==row[child]:
 				correct +=1
 	elif len(parents)==3:
		for row in data:
			i=row[parents[0]]
			j=row[parents[1]]
			k=row[parents[2]]	
 			count +=1
 			if int(2*table[i][j][k])==row[child]:
 				correct +=1
 	else:
		print "Error!!! More than 3 parents nodes exist!"

	if count==0:
		count=100000   #if total count is 0, means any probabilty will not affect the score of graph. 
	accuracy=correct/float(count)
	return accuracy

#open data files
f = open ( 'hw2_train.dat' , 'r')
data = [ map(int,line.strip().split('\t')) for line in f if line.strip() != '' ]
f2= open ( 'hw2_test.dat' , 'r')
test_data = [ map(int,line.strip().split('\t')) for line in f2 if line.strip() != '' ]

#generate the initial blank network
graph={}
graph_pa={}   #parents graph
prob_tables={}
for i in range(len(data[0])):
	graph[i]=[]
	graph_pa[i]=[]
	prob_tables[i]=0.44
net=net={'graph':graph,'graph_pa':graph_pa,'prob_tables':prob_tables}



best_score=-1000
current_score=-100
best_net={}
for x in range(2000):
	a=random.randint(0, len(data[0])-1)
	b=random.randint(0, len(data[0])-1)
	if a==b: continue
	# already have edge from b to a
	if b in net['graph_pa'][a]:  
		new_net=remove_edge(net,data,b,a) # remove
		if random.random()<0.5:
			new_net=add_edge(new_net,data,a,b) # half chance to reverse edge
	# already have edge from a to b
	elif b in net['graph'][a]: 
		new_net=remove_edge(net,data,a,b) # remove
		if random.random()<0.5:
			new_net=add_edge(new_net,data,b,a) # half chance to reverse edge
	# no direct edge between a and b
	else:
		new_net=add_edge(net,data,a,b)
	#new_net=0 when it is not valid or have cycle
	if new_net!=0:
		new_score=score(new_net,data)
	  	if new_score>current_score or random.random()<.2:
			current_score=new_score
			net=new_net
		if new_score>best_score:
			best_score=new_score
			best_net=new_net
	# print new_net
		print 'score=',new_score,'best=', best_score,"\n",new_net['graph']
		for i in range(6):
			print ' ',i, new_net['prob_tables'][i] 

		print "----"
print 'best net'
print best_score
print 'graph\t',best_net['graph']
print 'parent graph',best_net['graph_pa']
print 'conditional probability table:'
for i in range(6):
	print ' ',i, best_net['prob_tables'][i] 

print '\t\t\t',
for i in range(6):
	print 'g'+str(i+1),'\t',
print ''
print 'train-data-accuracy\t',
for i in range(6):
	print predict(best_net,data,i),'\t', # 2 is gene3.
print ''
print 'test-data-accuracy\t',
for i in range(6):
	print predict(best_net,test_data,i), '\t',# 2 is gene3.
print ''




