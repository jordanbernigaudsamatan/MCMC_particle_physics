#==========================================================================================================================
#
#	MCMC Main file : Control parameters = Nb chains, Length, Burnin.  Launch chains.
#
#==========================================================================================================================

from Class_parameter import *
from Class_observable import *
from Class_constraint import *
from chain import *
from functools import partial
import multiprocessing as mp
import os
import glob
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from setup import *


#======================================  Parameters & machine setup =======================================================

Nb_chains = 8		# Nb of chains (better to use Nb_chains = Nb_cores)

Chain_length = 200		# Nb of points / chain

Burn = 140		# Rm the first "Burn" points of chain

Nb_cores = 2			# Nb of cores used

Restart = False


#======================================  Chain launching setup =============================================================


Chain_name_list = []
for i in range(Nb_chains):
	Chain_name_list.append('Chain_'+str(i+1))		# Create list of chains name


os.system('rm -r Results')
os.system('rm -r Chain_*_Results/')
os.system('rm *Advancement.txt')
os.system('rm Likelihood*.npy')
os.system('mkdir Results')					# Delte former results folder + create new one


print('=======MAIN======== \n')
pool = mp.Pool(processes=Nb_cores)
#map(partial(chain, NPoints=Chain_length, blen=Burn), Chain_name_list)
L = pool.map_async(partial(chain, NPoints=Chain_length, blen=Burn), Chain_name_list)    # Launch chains
L.get()



os.system('mv *_Results Results/')



# ====================================== Create global data file ============================================================

# merging the files
joined_files = os.path.join('Results/', 'Chain_*/*.csv')

  
# A list of all joined files is returned
joined_list = glob.glob(joined_files)
  
# Finally, the files are joined
df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True)
df.to_csv('All_data.csv')

os.system('mv All_data.csv Results/')


# ==================================== Create Basic plots ====================================================================

dat = pd.read_csv('Results/All_data.csv')

with PdfPages('Plots_all_data.pdf') as pdf : 

	for item in param_list : 
	
		dat.hist(item[0])
		pdf.savefig()
		plt.close()
		
	for item in constraint_list : 
	
	
		dat.hist(item[0])
		plt.locator_params(axis='x', nbins=4)
		a = float(item[2])-float(item[3])
		b =float(item[2])+float(item[3])
		plt.axvspan(a,b, color ='r', alpha=0.5, lw=0)
		pdf.savefig()
		plt.close()
	





# ====================================  End ================================================================================

print('MCMC finished !')
