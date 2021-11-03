import math
import json
import os


# reference value in [N/mm2]

# Input [mm]

# b = 
# h = 

# L_ey = 
# L_ez = 


# Timber_Class = "C22"
# service_class = 1
# duration = "instantaneous"

# # Units [N]

# N_x = 
# V_y = 
# V_z = 
# M_x = 
# M_y = 
# M_z = 



# Opening JSON
def load_timber_properties(folder_path):

    collected_properties = []

    properties = ['timber_properties.json','k_mod.json','safety_factor.json','straightness_factor.json']

    for properti in properties:

        file_path = os.path.join(folder_path, properti)
        with open(file_path, 'r') as json_file:
            collected_properties.append(json.load(json_file))
    
    timber_properties, k_mod, safety_factor, straightness_factor = collected_properties

    return timber_properties, k_mod, safety_factor, straightness_factor


# Section Properties
def section_properties(b, h):

        Area = b * h

        W_y = (b * h**2) / 6
        W_z = (b**2 * h) / 6

        I_y = (b * h**3) / 12
        I_z = (b**3 * h) / 12

        I_t = 1/3 * b**3 * h * (1-0.63*(b/h))

        radii_of_gyration_y = (I_y/Area)**0.5
        radii_of_gyration_z = (I_z/Area)**0.5

        return Area, W_y, W_z, I_y, I_z, I_t, radii_of_gyration_y, radii_of_gyration_z


# Material Properties
def material_properties(timber_properties, Timber_Class):

        material_type = timber_properties[Timber_Class]["type"]
        fm_k = timber_properties[Timber_Class]["fm_k"]
        fv_k = timber_properties[Timber_Class]["fv_k"]
        fc_0_k = timber_properties[Timber_Class]["fc_0_k"]
        ft_0_k = timber_properties[Timber_Class]['ft_0_k']
        E_mean = timber_properties[Timber_Class]["E_mean"]
        E0_05 = timber_properties[Timber_Class]["E0_05"]
        G_mean = timber_properties[Timber_Class]["G_mean"]
        G0_05 = E0_05/16

        return material_type, fm_k, fv_k, fc_0_k, ft_0_k, E_mean, E0_05, G_mean, G0_05



# Design Factor
def design_parameters(b, h, safety_factor, material_type, k_mod, service_class, duration):

    km = 0.70
    gamma_m = safety_factor[material_type]
    kmod = k_mod[material_type][service_class][duration]

    print("kmod: {0:.2f}".format(kmod))


    ky_h = min( (150/h)**0.2 , 1.3 )
    kz_h = min( (150/b)**0.2 , 1.3 )

    ky_h = 1.0 if ky_h < 1.0 else ky_h
    kz_h = 1.0 if kz_h < 1.0 else kz_h

    print("ky_h: {0:.2f}".format(ky_h))
    print("kz_h: {0:.2f}".format(kz_h))


    kh = min(ky_h,kz_h)

    print("kh: {0:.2f}".format(kh))

    return km, gamma_m , kmod, ky_h, kz_h, kh


def buckling_parameters(b, h, L_ey, L_ez, radii_of_gyration_y, radii_of_gyration_z, fm_k, fc_0_k, E0_05, straightness_factor, material_type):
    

    lambda_y = L_ey / radii_of_gyration_y
    lambda_z = L_ez / radii_of_gyration_z

    print("lambda_y: {0:.2f}".format(lambda_y))
    print("lambda_z: {0:.2f}".format(lambda_z))


    lambda_rel_y = (lambda_y/math.pi) * (fc_0_k/E0_05)**0.5
    lambda_rel_z = (lambda_z/math.pi) * (fc_0_k/E0_05)**0.5

    print("lambda_rel_y: {0:.2f}".format(lambda_rel_y))
    print("lambda_rel_z: {0:.2f}".format(lambda_rel_z))


    beta_c = straightness_factor[material_type]

    k_y = 0.5 * (1 + beta_c * (lambda_rel_y - 0.3) + lambda_rel_y**2)
    k_z = 0.5 * (1 + beta_c * (lambda_rel_z - 0.3) + lambda_rel_z**2)

    print("k_y: {0:.2f}".format(k_y))
    print("k_z: {0:.2f}".format(k_z))


    kc_y = 1 / (k_y + math.sqrt(k_y**2 - lambda_rel_y**2))
    kc_z = 1 / (k_z + math.sqrt(k_z**2 - lambda_rel_z**2))

    print("kc_y: {0:.2f}".format(kc_y))
    print("kc_z: {0:.2f}".format(kc_z))


    kc = min(kc_y,kc_z)

    print("kc: {0:.2f}".format(kc))


    sigma_m_crit_y = E0_05 * (0.78 * b**2) / (h * L_ey)
    lambda_rel_m_y = math.sqrt(fm_k/sigma_m_crit_y)

    sigma_m_crit_z = E0_05 * (0.78 * h**2) / (b * L_ez)
    lambda_rel_m_z = math.sqrt(fm_k/sigma_m_crit_z)


    print("sigma_m_crit_y: {0:.2f}".format(sigma_m_crit_y))
    print("lambda_rel_m_y: {0:.2f}".format(lambda_rel_m_y))
    print("sigma_m_crit_z: {0:.2f}".format(sigma_m_crit_z))
    print("lambda_rel_m_z: {0:.2f}".format(lambda_rel_m_z))


    if lambda_rel_m_y < 0.75:
            k_crit_y = 1.00
    elif lambda_rel_m_y <= 1.40:
            k_crit_y = 1.56-0.75*lambda_rel_m_y
    elif lambda_rel_m_y > 1.40:
            k_crit_y = 1/lambda_rel_m_y**2


    if lambda_rel_m_z < 0.75:
            k_crit_z = 1.00
    elif lambda_rel_m_z <= 1.40:
            k_crit_z = 1.56-0.75*lambda_rel_m_z
    elif lambda_rel_m_z > 1.40:
            k_crit_z = 1/lambda_rel_m_z**2

    print("k_crit_y: {0:.2f}".format(k_crit_y))
    print("k_crit_z: {0:.2f}".format(k_crit_z))
    print("\n")

    return kc_y, kc_z, kc, k_crit_y, k_crit_z



# Design Strength

def axial_stress(N_x, Area):
    if N_x < 0.00:
            sigma_c_0_d = abs(N_x) / Area
            sigma_t_0_d = 0.00
            print("sigma_c_0_d: {0:.2f}".format(sigma_c_0_d))
            print("sigma_t_0_d: {0:.2f}".format(sigma_t_0_d))
    elif N_x > 0.00:
            sigma_c_0_d = 0.00
            sigma_t_0_d = abs(N_x) / Area
            print("sigma_c_0_d: {0:.2f}".format(sigma_c_0_d))
            print("sigma_t_0_d: {0:.2f}".format(sigma_t_0_d))
    else:
            sigma_c_0_d = 0.00
            sigma_t_0_d = 0.00
            print("sigma_c_0_d: {0:.2f}".format(sigma_c_0_d))
            print("sigma_t_0_d: {0:.2f}".format(sigma_t_0_d))
    
    return sigma_c_0_d, sigma_t_0_d


def bending_stress(M_y, M_z, W_y, W_z):
    
    sigma_m_y_d = abs(M_y) / W_y
    sigma_m_z_d = abs(M_z) / W_z
    
    print("sigma_m_y_d: {0:.2f}".format(sigma_m_y_d))
    print("sigma_m_z_d: {0:.2f}".format(sigma_m_z_d))

    return sigma_m_y_d, sigma_m_z_d


def shear_stress(V_y, V_z, b, h):

    k_cr = 0.67
    Area_eff = b * k_cr * h
    tau_y_d = 1.5 * abs(V_y) / Area_eff
    tau_z_d = 1.5 * abs(V_z) / Area_eff

    tau_d = math.sqrt(tau_y_d**2 + tau_z_d**2)

    print("tau_y_d: {0:.2f}".format(tau_y_d))
    print("tau_z_d: {0:.2f}".format(tau_z_d))
    print("tau_d: {0:.2f}".format(tau_d))

    return tau_d


def axial_resistance(kmod, fc_0_k, ft_0_k, gamma_m):

    fc_0_d = kmod * fc_0_k / gamma_m
    ft_0_d = kh * kmod * ft_0_k / gamma_m

    print("fc_0_d: {0:.2f}".format(fc_0_d))
    print("ft_0_d: {0:.2f}".format(ft_0_d))

    return fc_0_d, ft_0_d


def bending_resistance(kmod, ky_h, kz_h, fm_k, gamma_m):

    fm_y_d = kmod * ky_h * fm_k / gamma_m
    fm_z_d = kmod * kz_h * fm_k / gamma_m

    print("fm_y_d: {0:.2f}".format(fm_y_d))
    print("fm_z_d: {0:.2f}".format(fm_z_d))
    return fm_y_d, fm_z_d


def shear_resistance(kmod, fv_k, gamma_m):

    fv_d = kmod * fv_k / gamma_m
    print("fv_d: {0:.2f}".format(fv_d))

    return fv_d



# Design Combination

def utilisation_axial(sigma_c_0_d, sigma_t_0_d, ft_0_d, fc_0_d, kc):
    
    util_axial_tens = sigma_t_0_d/ft_0_d
    util_axial_comp = abs(sigma_c_0_d/(kc*fc_0_d))
    util_axial = max(util_axial_tens,util_axial_comp)

    return util_axial_tens, util_axial_comp, util_axial


def utilisation_bending(sigma_m_y_d, sigma_m_z_d, fm_y_d, fm_z_d, km):

    util_bending_y_1 = sigma_m_y_d/fm_y_d
    util_bending_y_2 = km * sigma_m_y_d/fm_y_d

    util_bending_z_1 = sigma_m_z_d/fm_z_d
    util_bending_z_2 = km * sigma_m_z_d/fm_z_d

    util_bending_y = max(util_bending_y_1,util_bending_y_2)
    util_bending_z = max(util_bending_z_1,util_bending_z_2)

    return util_bending_y, util_bending_z

def utilisation_shear(tau_d, fv_d):

    util_shear = tau_d/fv_d

    return util_shear


def utilisation_tension_bending(sigma_t_0_d, ft_0_d, sigma_m_y_d, fm_y_d, sigma_m_z_d, fm_z_d, km):
    
    util_bending_tens_y = (sigma_t_0_d/ft_0_d) + (sigma_m_y_d/fm_y_d) + km * (sigma_m_z_d/fm_z_d)
    util_bending_tens_z = (sigma_t_0_d/ft_0_d) + km * (sigma_m_y_d/fm_y_d) + (sigma_m_z_d/fm_z_d)

    return util_bending_tens_y, util_bending_tens_z


def utilisation_compression_bending(sigma_c_0_d, fc_0_d, sigma_m_y_d, fm_y_d, sigma_m_z_d, fm_z_d, kc_y, kc_z, km):

    util_bending_comp_y_1 = (abs(sigma_c_0_d)/(kc_y * fc_0_d)) + (sigma_m_y_d/fm_y_d) + km * (sigma_m_z_d/fm_z_d)
    util_bending_comp_y_2 = (abs(sigma_c_0_d)/(fc_0_d))**2 + (sigma_m_y_d/fm_y_d) + km * (sigma_m_z_d/fm_z_d)
    util_bending_comp_z_1 = (abs(sigma_c_0_d)/(kc_z * fc_0_d)) + km * (sigma_m_y_d/fm_y_d) + (sigma_m_z_d/fm_z_d)
    util_bending_comp_z_2 = (abs(sigma_c_0_d)/(fc_0_d))**2 + km * (sigma_m_y_d/fm_y_d) + (sigma_m_z_d/fm_z_d)
        
        
    util_bending_comp_y = max(util_bending_comp_y_1,util_bending_comp_y_2)
    util_bending_comp_z = max(util_bending_comp_z_1,util_bending_comp_z_2)

    return util_bending_comp_y, util_bending_comp_z


def utilisation_LTB(b, h, sigma_c_0_d, fc_0_d, sigma_t_0_d, sigma_m_y_d, fm_y_d, sigma_m_z_d, fm_z_d, k_crit_y, k_crit_z, kc_z, kc_y, km):

    util_LTB_capacity_y = (sigma_m_y_d-sigma_t_0_d)/(k_crit_y*fm_y_d) + km * sigma_m_z_d/fm_z_d
    util_LTB_capacity_z = (sigma_m_z_d-sigma_t_0_d)/(k_crit_z*fm_z_d) + km * sigma_m_y_d/fm_y_d

    util_LTB_capacity_y = (sigma_m_y_d/ (k_crit_y * fm_y_d))**2 + (abs(sigma_c_0_d)/(kc_z*fc_0_d))
    util_LTB_capacity_z = (sigma_m_z_d/ (k_crit_z * fm_z_d))**2 + (abs(sigma_c_0_d)/(kc_y*fc_0_d))

    if h >= b:
        util_LTB_capacity = util_LTB_capacity_y
    else:
        util_LTB_capacity = util_LTB_capacity_z

    return util_LTB_capacity



# utilisation = [util_axial, util_bending_y, util_bending_z, util_shear, util_bending_tens_y, util_bending_tens_z, util_bending_comp_y, util_bending_comp_z, util_LTB_capacity]
# utilisation = [round(number,2) for number in utilisation]



# print("\n")
# print("Util Axial: {}".format(abs(round(util_axial,2))))
# print("Util Bending y: {}".format(abs(round(util_bending_y,2))))
# print("Util Bending z: {}".format(abs(round(util_bending_z,2))))
# print("Util Shear: {}".format(abs(round(util_shear,2))))

# print("\n")
# print("Util Combined Bending_y Tension: {}".format(abs(round(util_bending_tens_y,2))))
# print("Util Combined Bending_z Tension: {}".format(abs(round(util_bending_tens_z,2))))
# print("Util Combined Bending_y Compression: {}".format(abs(round(util_bending_comp_y,2))))
# print("Util Combined Bending_z Compression: {}".format(abs(round(util_bending_comp_z,2))))
# print("Util Lateral Buckling: {}".format(abs(round(util_LTB_capacity,2))))