run the program :

python hw1.py


By default the program will run Metropolis Algorithm with 10000 loops and T=1. 
At the end of hw1.py, you can set the parameters for Metropolis(sequence, number of loop, temperature).
	Metropolis(protein_sequence, 10000, 1)  
	# second value gives the number of generations, third number is temperature
	#GeneticAlgorithm(protein_sequence,200, 3)  

For Genetic Algorithm, you need to comment out Metropolis function, and uncomment GeneticAlgorithm function.
such as :

	#Metropolis(protein_sequence, 10000, 1)  
	# second value gives the number of generations, third number is temperature
	GeneticAlgorithm(protein_sequence,200, 3)  
By default, the number of generation is 200 and initial temperature is 3, which can be modified easily.

