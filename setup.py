
#Preamble
import numpy as np
import math



# ===================== List of parameters in the format : [Name, minim, maxi, Width] =================================

step = 0.01
Step_decreases = 0.99995 # Everytime the point is rejected the step decreases as step * Step_decreases



param_list = np.array([

['a_d', -0.05, 0.05, step],
['b_d', -0.5, 0.5, step],
['gamma_d', 0.0, 2*math.pi, step],
['delta_d', 0.0, 2*math.pi, step],

['a_u', -0.02, 0.02, step],
['b_u', -0.02, 0.02, step],
['gamma_u', 0.0, 2*math.pi, step],
['delta_u', 0.0, 2*math.pi, step],

['a_n', -5e-4, 5e-4, step],
['b_n', -1e-3, 1e-3, step],
['gamma_n', 0.0, 2*math.pi, step],
['delta_n', 0.0, 2*math.pi, step],


['x', 5e-13, 30e-13, step],
['y', 0.5e-13, 15e-13, step],
['rho', 0.0, 2*math.pi, step],
['phi', 0.0, 2*math.pi, step],

['scale', 0.5*10**10.5, 1.5*10**10.5, step],   # ASK JIM here

])

# THIS IS THE FIRST PARAMETER values jim gave me


'''
param_list = np.array([

['a_d', .0042 , .0042 , step],
['b_d', .0545/3 , .0545/3 , step],
['gamma_d', .13 , .13 , step],
['delta_d', 1.83 , 1.83 , step],

['a_u', -.00014 , -.00014 , step],
['b_u', .003 , .003 , step],
['gamma_u', 0.0 , 0.0 , step],
['delta_u', 0.0 , 0.0 , step],

['a_n', 4e-5 , 4e-5 , step],
['b_n', 11.8e-5 , 11.8e-5 , step],
['gamma_n', 2*np.pi/5 , 2*np.pi/5 , step],
['delta_n', 0.0 , 0.0 , step],


['x', 12.75e-13 , 12.75e-13 , step],
['y', 4.055e-13 , 4.055e-13 , step],
['rho', 0.0 , 0.0 , step],
['phi', -2*np.pi/5 , -2*np.pi/5 , step],

['scale', 10**10.5 , 10**10.5 , step],   # ASK JIM here

])

'''


# ===================== List of parameters in the format : [Name, type ,exp_val, uncertainty] ===============================
# Type : 'S' for step or upper bound (for limit value like mu-> e gamma), 'G' gaussian (for measured)



constraint_list = np.array([

['stheta_q_12', 'G', 0.227 , 0.001],
['stheta_q_13', 'G', 0.003385 , 0.001695],
['stheta_q_23', 'G', 0.0344  , 0.0124],
['sdelta_q', 'G', 0.593  , 0.407], # CHECK SIN VS NON-SIN PHASE

['stheta_l_12', 'G',  0.552 , 0.034 ],
['stheta_l_13', 'G', 0.150 , 0.006],
['stheta_l_23', 'G',  0.7075 , 0.0695],
['sdelta_l', 'G',  0.381 , 0.207], # CHECK SIN VS NON-SIN PHASE

['m_e_OVER_m_tau', 'G',  0.000265 , 0.000045],
['m_mu_OVER_m_tau', 'G',  0.0545 , 0.0065],

['m_u_OVER_m_t', 'G',  5.295e-6 , 3.615e-6],
['m_c_OVER_m_t', 'G',  0.00177 , 0.00093],

['m_d_OVER_m_b', 'G',  0.000775 , 0.000425],
['m_s_OVER_m_b', 'G',  0.0145 , 0.0065],

['Delta_msol_OVER_delta_matm', 'G',  0.025935 , 0.013535],



])


# ===================== List of parameters in the format : To be defined according to MODEL -> Observable framework =================================



observable_list = np.array([

])
