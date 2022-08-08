import numpy as np
import math
from numpy import linalg as LA
from numpy.linalg import inv

import chain


# ========== Prerequired Functions ===================================================

def dag(x):
	return x.conjugate().T
	
def square(x):
	return np.dot(x,dag(x))
	
def seesaw(x,y):
	return np.dot(np.dot(x, LA.inv(y)), x.T)

def Md(alpha,beta,a,b,gamma,delta):
	return np.array([[0,a*np.exp(1j*(alpha+beta+gamma)),a*np.exp(1j*(beta+gamma))],[a*np.exp(1j*(alpha+beta+gamma)),(b*np.exp(-1j*gamma)+2*a*np.exp(-1j*delta))*np.exp(1j*(2*alpha+gamma+delta)),b*np.exp(1j*(alpha+delta))],  [a*np.exp(1j*(beta+gamma)),b*np.exp(1j*(alpha+delta)),(1+b*np.exp(1j*delta)-2*a*np.exp(1j*gamma))]])

def Mm(alpha,beta,x,y,rho,phi,scale):
	return np.array([[0,y*np.exp(1j*(alpha+beta+rho)),y*np.exp(1j*(beta+rho))],[y*np.exp(1j*(alpha+beta+rho)),(x*np.exp(-1j*(rho))+2*y*np.exp(-1j*(phi)))*np.exp(1j*(2*alpha+rho+phi)),x*np.exp(1j*(alpha+phi))],  [y*np.exp(1j*(beta+rho)),x*np.exp(1j*(alpha+phi)),(1+x*np.exp(1j*(phi))-2*y*np.exp(1j*(rho)))]])*scale
	



# ===================================== Main function to be called ================================================================

def Compute_observables(All_Dict, Dict_parameters, Dict_constraints) : 



	# ========================== Parameters =============================

	a_d = All_Dict[Dict_parameters]['a_d'].val
	b_d = All_Dict[Dict_parameters]['b_d'].val
	gamma_d = All_Dict[Dict_parameters]['gamma_d'].val
	delta_d = All_Dict[Dict_parameters]['delta_d'].val
	
	a_u = All_Dict[Dict_parameters]['a_u'].val
	b_u = All_Dict[Dict_parameters]['b_u'].val
	gamma_u = All_Dict[Dict_parameters]['gamma_u'].val
	delta_u = All_Dict[Dict_parameters]['delta_u'].val
	
	a_n = All_Dict[Dict_parameters]['a_n'].val
	b_n = All_Dict[Dict_parameters]['b_n'].val
	gamma_n = All_Dict[Dict_parameters]['gamma_n'].val
	delta_n = All_Dict[Dict_parameters]['delta_n'].val
	
	x = All_Dict[Dict_parameters]['x'].val
	y = All_Dict[Dict_parameters]['y'].val
	rho = All_Dict[Dict_parameters]['rho'].val
	phi = All_Dict[Dict_parameters]['phi'].val
	scale = All_Dict[Dict_parameters]['scale'].val




	# ===================== Params list =================================
	
	#for now I simply input the parameters associated to the best-fit from the 2017 paper.  This is what we will scan over!
	
	#VEV phases (universal to all family sectors)
	#For now we take these to be zero working under the assumption that, as per Roberts, Romanino & Ross that two phases can #be eliminated from our analysis (we did this in the original UTZ 	paper as well, so it's good to check it anyway)
	
	Vp = [0., 0.]

	#Down quark parameters (a_d, b_d, gamma_d, delta_d)

	Dp = [a_d, b_d, gamma_d, delta_d]

	#Up quark parameters (a_u, b_u, gamma_u, delta_u)

	Up = [a_u, b_u, gamma_u, delta_u]

	#Charged lepton parameters are given in terms of down-quark parameters due to GUT relations
	#(a_e, b_e, gamma_e, delta_e) = (a_d, -3*b_d, gamma_d, delta_d)

	#Dirac neutrino parameters (a_n, b_n, gamma_n, delta_n)

	Np = [a_n, b_n, gamma_n, delta_n]

	#Majorana neutrino parameters (x, y, rho, phi, scale)
	#I don't think we need to scan over the seesaw scale, so this can probably in the code.  But I've included it for completeness for #now

	Mp = [x,y,rho,phi,scale]

	# ===================== Mass Matrices =================================

	flip = np.array([[0,0,1],[0,1,0],[1,0,0]])


	#define mass matrices in each family sector	

	M_down = square(Md(Vp[0],Vp[1],Dp[0],Dp[1],Dp[2],Dp[3]))
	M_up = square(Md(Vp[0],Vp[1],Up[0],Up[1],Up[2],Up[3]))
	M_lepton = square(Md(Vp[0],Vp[1],Dp[0],-3*Dp[1],Dp[2],Dp[3]))

	M_dirac = Md(Vp[0],Vp[1],Np[0],Np[1],Np[2],Np[3])
	M_majorana = Mm(Vp[0],Vp[1],Mp[0],Mp[1],Mp[2],Mp[3],Mp[4])
	M_neutrino = square(seesaw(M_dirac,M_majorana))

	# ===================== Parameter Extraction =================================

	eVal_down, U_down = LA.eig(M_down)
	eVal_down_sort = eVal_down.argsort()[::1] 
	eVal_down = eVal_down[eVal_down_sort]
	U_down = U_down[:,eVal_down_sort]
	#::1 notation orients evalues lightest to heaviest, ::-1 heaviest to lightest

	eVal_up, U_up = LA.eig(M_up)
	eVal_up_sort = eVal_up.argsort()[::1] 
	eVal_up = eVal_up[eVal_up_sort]
	U_up = U_up[:,eVal_up_sort]

	eVal_lepton, U_lepton = LA.eig(M_lepton)
	eVal_lepton_sort = eVal_lepton.argsort()[::1] 
	eVal_lepton = eVal_lepton[eVal_lepton_sort]
	U_lepton = U_lepton[:,eVal_lepton_sort]

	eVal_neutrino, U_neutrino = LA.eig(M_neutrino)
	eVal_neutrino_sort = eVal_neutrino.argsort()[::1] 
	eVal_neutrino = eVal_neutrino[eVal_neutrino_sort]
	U_neutrino = U_neutrino[:,eVal_neutrino_sort]

	#define mass ratios in each family sector

	downbottom_massratio = (np.sqrt(eVal_down[0])/np.sqrt(eVal_down[2])).real
	strangebottom_massratio = (np.sqrt(eVal_down[1])/np.sqrt(eVal_down[2])).real
	#note that masses are only defined up to an overall scale.  Only mass ratios are considered predictions in this model.
	
	uptop_massratio = (np.sqrt(eVal_up[0])/np.sqrt(eVal_up[2])).real
	charmtop_massratio = (np.sqrt(eVal_up[1])/np.sqrt(eVal_up[2])).real
	
	etau_massratio = (np.sqrt(eVal_lepton[0])/np.sqrt(eVal_lepton[2])).real
	mutau_massratio = (np.sqrt(eVal_lepton[1])/np.sqrt(eVal_lepton[2])).real
	 
	nu12_massdifference = (eVal_neutrino[2]-eVal_neutrino[1]).real
	nu23_massdifference = (eVal_neutrino[1]-eVal_neutrino[0]).real
	nu2312_massratio = nu23_massdifference/nu12_massdifference
	
	#define CKM/PMNS matrices and extract mixing angles and Dirac phases
	
	#CKMtest = np.dot(np.dot(flip,dag(Utest)),np.dot(Utest2,flip))
	CKM = np.dot(dag(U_up),U_down)
	
	#note that the flip matrix just reorients the evectors associated to different e-values.  It is not needed if the e-values are #ordered from the lightest to heaviest generations (as is 	standard normalization)

	Jarlskogq = (CKM[0][2]*CKM[1][0]*np.conjugate(CKM[0][0])*np.conjugate(CKM[1][2])).imag
	stheta13q = np.abs(CKM[0][2])
	stheta23q = np.abs(CKM[1][2])/np.sqrt(1-np.abs(CKM[0][2])**2)
	stheta12q = np.abs(CKM[0][1])/np.sqrt(1-np.abs(CKM[0][2])**2) 
	sdeltaq = Jarlskogq/(np.sqrt(1-stheta12q**2)*(1-stheta13q**2)*np.sqrt(1-stheta23q**2)*stheta12q*stheta13q*stheta23q)


	PMNS=np.dot(dag(U_lepton),U_neutrino)

	Jarlskogl = (PMNS[0][2]*PMNS[1][0]*np.conjugate(PMNS[0][0])*np.conjugate(PMNS[1][2])).imag
	stheta13l = np.abs(PMNS[0][2])
	stheta23l = np.abs(PMNS[1][2])/np.sqrt(1-np.abs(PMNS[0][2])**2)
	stheta12l = np.abs(PMNS[0][1])/np.sqrt(1-np.abs(PMNS[0][2])**2) 
	sdeltal = Jarlskogl/(np.sqrt(1-stheta12l**2)*(1-stheta13l**2)*np.sqrt(1-stheta23l**2)*stheta12l*stheta13l*stheta23l)


	# ===================== Assign values to constraints =================================

	All_Dict[Dict_constraints]['stheta_q_12'].value = stheta12q
	All_Dict[Dict_constraints]['stheta_q_13'].value = stheta13q
	All_Dict[Dict_constraints]['stheta_q_23'].value = stheta23q
	All_Dict[Dict_constraints]['sdelta_q'].value = sdeltaq
	
	All_Dict[Dict_constraints]['stheta_l_12'].value = stheta12l
	All_Dict[Dict_constraints]['stheta_l_13'].value = stheta13l
	All_Dict[Dict_constraints]['stheta_l_23'].value = stheta23l
	All_Dict[Dict_constraints]['sdelta_l'].value = sdeltal

	All_Dict[Dict_constraints]['m_e_OVER_m_tau'].value = etau_massratio
	All_Dict[Dict_constraints]['m_mu_OVER_m_tau'].value = mutau_massratio

	All_Dict[Dict_constraints]['m_d_OVER_m_b'].value = downbottom_massratio
	All_Dict[Dict_constraints]['m_s_OVER_m_b'].value = strangebottom_massratio

	All_Dict[Dict_constraints]['m_u_OVER_m_t'].value = uptop_massratio	
	All_Dict[Dict_constraints]['m_c_OVER_m_t'].value = charmtop_massratio	
	
	All_Dict[Dict_constraints]['Delta_msol_OVER_delta_matm'].value = nu2312_massratio	
		
	return All_Dict
	
	
	
	
	
	
	
	
	
	
	
	
	
	

