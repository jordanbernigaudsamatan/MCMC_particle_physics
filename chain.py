# ========================================================================================================================
# ========================================================================================================================
#                                          MCMC Chain function 
# ========================================================================================================================
# ========================================================================================================================


#Preamble
import random as rnd
import numpy as np
import sys
import os
import os.path
from Class_parameter import *
from Class_observable import *
from Class_constraint import *
from setup import *
from Model import *
import scipy
import pandas as pd


# ===================================================================================================
#                             Setup the chain - declare variables and initialize class instances
# ===================================================================================================



def chain(chain_name,NPoints,blen):	# chain is a function that can be mapped on a chain name list






	rnd.seed()		# ensure good randomisation if parrallelized start
    
    
# =============================== Create Dictionaries =======================================

	All_Dict = {}		# Store all dictionnaries in one super dictionary
	Likelihood_Dict = {}
	
	initialise = True
	Accepted_points = 0

    


# ===== Setup dictionnaries from parameters, constraints and observables ======================


	Dict_parameters = chain_name + '_variables'
	Dict_observables = chain_name + '_observables'
	Dict_constraints = chain_name + '_constraints'
	likelihood_list = chain_name + '_likelihood_list_NO_BURNING'
	All_Dict[Dict_parameters] = {}
	All_Dict[Dict_observables] = {}			# create and encapsulates all dictionaries in 1 : All_Dict
	All_Dict[Dict_constraints] = {}
	Likelihood_Dict[likelihood_list] = []

    
# ===== Create paramters, constraints and observables class instances from lists in setup.py ===




    
	print('============================    SETUP Dictionnaries of CHAIN: '+ chain_name + ' =================================')

	for param in param_list :
		All_Dict[Dict_parameters][param[0]] = parameter(param[0], param[1], param[2], param[3])

	for const in constraint_list :
		All_Dict[Dict_constraints][const[0]] = Constraint(const[0], const[1], const[2], const[3])

	for obs in observable_list :
		All_Dict[Dict_observables][obs[0]] = observable(obs[0], obs[1], obs[2], obs[3])


# ===== ================================= Create results folder ===================================

	chain_result_dir = chain_name+'_Results'

	os.system('mkdir '+chain_result_dir)    
	
	
# ======== Create dictionary for data (pandas dataframe) =================

	DATA = {}

	for item in param_list : 
		DATA[item[0]] = []
	
	for item in constraint_list : 
		DATA[item[0]] = []
	
	for item in observable_list : 
		DATA[item[0]] = []
		
	DATA['likelihood'] = []
	
    
    
    





# ===================================================================================================
#                  INITIALIZATION OF CHAIN - Randomly find a non zero likelihood starting point
# ===================================================================================================

# ============================= Advancement stated in printings + file  =============================


	print('\n============================    INITIALIZE CHAIN: '+ chain_name + ' =================================\n')

	Ini = 0	# number of initialization tries

	while initialise :

		Ini += 1
		
		
			
			

		

		
# ============================= Initialise parameters -> STARTING point proposal ==========================================

		# Initialise parameters
		for param in param_list :
			All_Dict[Dict_parameters][param[0]].initialise()	# The parameter class method initialise -> give the param a random value between min and max allowed
			
			
		
# ============================= Compute constraints values ================================================================
			
		All_Dict = Compute_observables(All_Dict, Dict_parameters, Dict_constraints)


# ============================= Likelihood test for initialization (must be non zero even if tiny) ==========================

		Initial_likelihood = 1.0
		

		
		

		for const in constraint_list:
			All_Dict[Dict_constraints][const[0]].compute_likelihood() # compute the likelihood associated to each constraint for this point
			Initial_likelihood = Initial_likelihood * All_Dict[Dict_constraints][const[0]].likelihood	# product of all likelihood
			
			# ===================================================================================#
			# Update the likelihoods file to follow the value of the individual likelihoods	#
			
		if Ini%200 == 0 or Ini == 0 : 
		
			#============================================================================================
			#Create a file to follow advancement								#
			f = open(chain_name+'_Advancement.txt','a')							#
			f.write('===================   Initialization    ================= \n')	
			f.write('Number of tries : '+ str(Ini))						#
			f.write('\n')
			f.write('Current global likelihood test for initialization : '+ str(Initial_likelihood)+ ' \n')			#
			f.write('\n \n')
			f.write('Current individual likelihoods and constraint values: \n')
			for const in constraint_list:
				f.write(str(All_Dict[Dict_constraints][const[0]].name))				#
				f.write(" : ")									#	
				f.write(str(All_Dict[Dict_constraints][const[0]].likelihood  ) )			#
				f.write( " with the value  " )							#
				f.write( str(All_Dict[Dict_constraints][const[0]].value) )
				f.write('\n')			#
			f.write("\n \n")									#
			f.close()										#
			# ===================================================================================#
		
			

			
		if Initial_likelihood != 0.0 :	# test the non zero-iness of the final likelihood
			
			for param in param_list:					# All parameters have now an initial value.
				All_Dict[Dict_parameters][param[0]].accepted()
				initialise = False
				


		#else : print('Initialization : Likelihood = ',Initial_likelihood,', Try new point') # If L = 0 -> restart a new point)




	print('\n============================    INITIALIZATION OF : '+ chain_name + ' DONE !!! (After '+str(Ini)+' tries) =================================\n')

	print('Initial likelihood = ', Initial_likelihood)
	
	# ==================================================================  Save progress of chain ===================================================================
	f = open(chain_name+'_Advancement.txt','a')
	f.write('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   SUCCESS IN INITIALIZATION   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
	f.write('\n')
	f.write('Nb of tries : '+str(Ini)+'\n')
	f.write('Initial Likelihood : ' + str(Initial_likelihood))
	f.write('\n \n')
	f.write('Current individual likelihoods and constraint values: \n')
	for const in constraint_list:
		f.write(str(All_Dict[Dict_constraints][const[0]].name))				#
		f.write(" : ")									#	
		f.write(str(All_Dict[Dict_constraints][const[0]].likelihood  ) )			#
		f.write( " with the value  " )							#
		f.write( str(All_Dict[Dict_constraints][const[0]].value) )
		f.write('\n')			#
	f.write("\n \n")									#
	f.close()
	#============================================================================================================================================================
	






# ===================================================================================================
#                  MCMC CHAIN - Evolve the chain finding highest likelihood places
# ===================================================================================================

	Old_likelihood = Initial_likelihood
	i = 0
	while Accepted_points < NPoints:
	
		if i%20000 == 0 : print('========== MCMC evolution of '+chain_name+' ============\n Test point n = ', i, ' \n N accepted : ', Accepted_points)
	

	
		i += 1


# ============================= Propose a point n+1 to be tested =======================

		for param in param_list :
			All_Dict[Dict_parameters][param[0]].jump()	
			

			
# ============================= Compute constraints values ==============================
			
		All_Dict = Compute_observables(All_Dict, Dict_parameters, Dict_constraints)


# ==================== Compute likelihood ================


		New_likelihood = 1.0


		for const in constraint_list:
		
			All_Dict[Dict_constraints][const[0]].compute_likelihood()
			New_likelihood *= All_Dict[Dict_constraints][const[0]].likelihood	# compute proposal likelihood

			


# =========================== Test, accept/rejetct point =================================


		u_test = rnd.uniform(0.0,1.0)
			
		R_likelihood = New_likelihood / Old_likelihood


		if u_test < min(1, R_likelihood):
				
			Accepted_points += 1

				
			
			
				
				
# ======================= Some print statements to follow the advancement on scree ===

			if Accepted_points % 10 == 0 : 
			
				print('\n================== Advancement of chain '+chain_name+' = ', float(Accepted_points)/NPoints*100, ' % ============\n')
				print('Global likelihood proposal = '+str(New_likelihood)+'\nwith current individual likelihoods '+chain_name+' : ')
			
				# =====================================================
				#    Write accepted points in file 			#
				f = open(chain_name+'_Advancement.txt','a')	
				f.write('============================== Scan MCMC chain ========================== \n')
				f.write("Number of accepted points : ")		#
				f.write(str(Accepted_points))	
				f.write('\n with : Proposal likelihood = '+str(New_likelihood) + '\n And individual likelihoods : \n' )
				for const in constraint_list:
					print(All_Dict[Dict_constraints][const[0]].name, 'Likelihood = ', All_Dict[Dict_constraints][const[0]].likelihood, '  with value = ' +str(All_Dict[Dict_constraints][const[0]].value ))	
					f.write( All_Dict[Dict_constraints][const[0]].name+ 'Likelihood = ' +str(All_Dict[Dict_constraints][const[0]].likelihood )+'  with value = ' +str(All_Dict[Dict_constraints][const[0]].value )+'\n')		
											#
											#
				f.write('\n\n')
				f.close()						#
				# =====================================================

				
				




# ======================== Accept the proposal point ==================================
			for param in param_list:
				All_Dict[Dict_parameters][param[0]].accepted()		# accept the proposal
				
			Old_likelihood = New_likelihood
			Likelihood_Dict[likelihood_list].append(Old_likelihood)				# create a likelihood list for plot
				
				
				
				
# ============================= Save data ===========================================
			
			if Accepted_points > blen : 
				
				for item in param_list : 
					DATA[item[0]].append(  All_Dict[Dict_parameters][item[0]].val  ) 
	
				for item in constraint_list : 
					DATA[item[0]].append(  All_Dict[Dict_constraints][item[0]].value  ) 
	
				for item in observable_list : 
					DATA[item[0]].append(  All_Dict[Dict_observables][item[0]].value  ) 
				
				DATA['likelihood'].append(Old_likelihood)


		else : 
		
			for param in param_list:
				All_Dict[Dict_parameters][param[0]].rejected()


		


# ===================================================================================================
#                  END OF CHAIN - Save files
# ===================================================================================================



	df = pd.DataFrame(DATA)
	
	df.to_csv(chain_name+'_data.csv')

	np.save('Likelihood_list_'+chain_name, Likelihood_Dict[likelihood_list])
	
	
	os.system('mv '+chain_name+'_Advancement.txt '+chain_result_dir)
	os.system('mv Likelihood_list_'+chain_name+'.npy '+chain_result_dir)
	os.system('mv '+chain_name+'_data.csv '+chain_result_dir)




	print('=======================================================  Chain FINISHED =====================================================================================')
	
	





































