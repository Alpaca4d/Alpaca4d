import math

k_mod = {"Solid_Timber":{
                    1:{"permanent":0.60,"long_term":0.70,"medium_term":0.80,"short_term":0.90,"instantaneous":1.10},
                    2:{"permanent":0.60,"long_term":0.70,"medium_term":0.80,"short_term":0.90,"instantaneous":1.10},
                    3:{"permanent":0.50,"long_term":0.55,"medium_term":0.65,"short_term":0.70,"instantaneous":0.90}},
        "LVL":   {
                    1:{"permanent":0.00,"long_term":0.00,"medium_term":0.00,"short_term":0.00,"instantaneous":0.00},
                    2:{"permanent":0.00,"long_term":0.00,"medium_term":0.00,"short_term":0.00,"instantaneous":0.00},
                    3:{"permanent":0.00,"long_term":0.00,"medium_term":0.00,"short_term":0.00,"instantaneous":0.00}}
        }


safety_factor = {"Solid_Timber":1.3,"Glulam":1.25,"LVL":1.2}

# reference value in [N/mm2]

timber_properties = {"GOB_Green_Oak":
                                {"fm_k":27.8,"fv_k":4.01,"E_mean":9260,"E0_05":7130,"G_mean":590,"fc_0_k":17.2,"fc_90_k":6.1,"ft_0_k":0.00,"ft_90_k":0.00,"rho_k":000,"type":"solid Timber"},
                    "C14":
                                {"fm_k":14.0,"fv_k":3.00,"E_mean":7000,"E0_05":4700,"G_mean":440,"fc_0_k":16.0,"fc_90_k":2.0,"ft_0_k":8.00,"ft_90_k":0.40,"rho_k":290,"type":"solid Timber"},
                    "C16":
                                {"fm_k":16.0,"fv_k":1.80,"E_mean":8000,"E0_05":5400,"G_mean":500,"fc_0_k":17.0,"fc_90_k":2.2,"ft_0_k":10.0,"ft_90_k":0.50,"rho_k":310,"type":"solid Timber"},
                    "Cxx":
                                {"fm_k":0000,"fv_k":0000,"E_mean":0000,"E0_05":0000,"G_mean":000,"fc_0_k":0000,"fc_90_k":000,"ft_0_k":0000,"ft_90_k":0000,"rho_k":000,"type":"solid Timber"},
                    "Cx1":
                                {"fm_k":0000,"fv_k":0000,"E_mean":0000,"E0_05":0000,"G_mean":000,"fc_0_k":0000,"fc_90_k":000,"ft_0_k":0000,"ft_90_k":0000,"rho_k":000,"type":"solid Timber"}
                    }


straightness_factor = {"Solid_Timber":0.2,"Glulam":0.1,"LVL":0.1}


# Input [mm]

b = 75
h = 15

L_ey = 1000
L_ez = 1000

material_type = "Solid_Timber"
material_name = "GOB_Green_Oak"
service_class = 2
duration = "instantaneous"

# Units [N]

N = -4000
M_y = 100000
M_z = 100000
V = 1000


# Section Properties

Area = b * h

W_y = (b * h**2) / 6
W_z = (b**2 * h) / 6


I_y = (b * h**3) / 12
I_z = (b**3 * h) / 12
I_t = 1/3 * b**3 * h * (1-0.63*(b/h))

radii_of_gyration_y = (I_y/Area)**0.5
radii_of_gyration_z = (I_z/Area)**0.5


# Material Properties

fm_k = timber_properties[material_name]["fm_k"]
fv_k = timber_properties[material_name]["fv_k"]
fc_0_k = timber_properties[material_name]["fc_0_k"]
ft_0_k = timber_properties[material_name]["ft_0_k"]
E_mean = timber_properties[material_name]["E_mean"]
E0_05 = timber_properties[material_name]["E0_05"]
G_mean = timber_properties[material_name]["G_mean"]
G0_05 = E0_05/16


# Design Factor

gamma_m = safety_factor[material_type]
kmod = k_mod[material_type][service_class][duration]


ky_h = min( (150/h)**0.2 , 1.3 )
kz_h = min( (150/b)**0.2 , 1.3 )

ky_h = 1.0 if ky_h < 1.0 else ky_h
kz_h = 1.0 if kz_h < 1.0 else kz_h

print("ky_h: {}".format(ky_h))
print("kz_h: {}".format(kz_h))


# Biaxial bending factor
km = 0.70


lambda_y = L_ey / radii_of_gyration_y
lambda_z = L_ez / radii_of_gyration_z

print("lambda_y: {}".format(lambda_y))
print("lambda_z: {}".format(lambda_z))


lambda_rel_y = (lambda_y/math.pi) * (fc_0_k/E0_05)**0.5
lambda_rel_z = (lambda_z/math.pi) * (fc_0_k/E0_05)**0.5

print("lambda_rel_y: {}".format(lambda_rel_y))
print("lambda_rel_z: {}".format(lambda_rel_z))


beta_c = straightness_factor[material_type]


k_y = 0.5 * (1 + beta_c * (lambda_rel_y - 0.3) + lambda_rel_y**2)
k_z = 0.5 * (1 + beta_c * (lambda_rel_z - 0.3) + lambda_rel_z**2)

print("k_y: {}".format(k_y))
print("k_z: {}".format(k_z))


kc_y = 1 / (k_y + math.sqrt(k_y**2 - lambda_rel_y**2))
kc_z = 1 / (k_z + math.sqrt(k_z**2 - lambda_rel_z**2))

print("kc_y: {}".format(kc_y))
print("kc_z: {}".format(kc_z))


kc = min(kc_y,kc_z)

print("kc: {}".format(kc))

#update formula to check b < h

if b > h:
        b_temp = h
        h_temp = b
sigma_m_crit = E0_05 * (0.78 * b_temp**2) / (h_temp * L_ey)
lambda_rel_m = math.sqrt(fm_k/sigma_m_crit)

print("sigma_m_crit: {}".format(sigma_m_crit))
print("lambda_rel_m: {}".format(lambda_rel_m))


if lambda_rel_m < 0.75:
        k_crit = 1.00
elif lambda_rel_m <= 1.40:
        k_crit = 1.56-0.75*lambda_rel_m
elif lambda_rel_m > 1.40:
        k_crit = 1/lambda_rel_m**2

print("k_crit: {}".format(k_crit))
print("\n")

# Design Strength
if N < 0.00:
        sigma_c_0_d = N / Area
        sigma_t_0_d = 0.00
        print("sigma_c_0_d: {}".format(sigma_c_0_d))
        print("sigma_t_0_d: {}".format(sigma_t_0_d))
elif N > 0.00:
        sigma_c_0_d = 0.00
        sigma_t_0_d = N / Area
        print("sigma_c_0_d: {}".format(sigma_c_0_d))
        print("sigma_t_0_d: {}".format(sigma_t_0_d))
    
sigma_m_y_d = M_y / W_y
print("sigma_m_y_d: {}".format(sigma_m_y_d))

sigma_m_z_d = M_z / W_z
print("sigma_m_z_d: {}".format(sigma_m_z_d))

k_cr = 0.67
Area_eff = b * k_cr * h
tau_d = 1.5 * V / Area_eff
print("tau_d: {}".format(tau_d))

fc_0_d = kmod * fc_0_k / gamma_m
print("fc_0_d: {}".format(fc_0_d))

fm_y_d = kmod * ky_h * fm_k / gamma_m
print("fm_y_d: {}".format(fm_y_d))

fm_z_d = kmod * kz_h * fm_k / gamma_m
print("fm_z_d: {}".format(fm_z_d))

fv_d = kmod * fv_k / gamma_m
print("fv_d: {}".format(fv_d))

# Design Combination

if N > 0.0:
        util_bendind_tens_y = (sigma_t_0_d/fc_0_d) + (sigma_m_y_d/fm_y_d) + kmod * (sigma_m_z_d/fm_z_d)
        util_bending_tens_z = (sigma_t_0_d/fc_0_d) + kmod * (sigma_m_y_d/fm_y_d) + (sigma_m_z_d/fm_z_d)
        util_bendin_comp_y = 0.00
        util_bendin_comp_z = 0.00
        util_LTB_capacity = (sigma_m_y_d-sigma_t_0_d)/(k_crit*fm_y_d) + km * sigma_m_z_d/fm_z_d
else:
        util_bendind_tens_y = 0.00
        util_bending_tens_z = 0.00
        util_bendin_comp_y = (abs(sigma_c_0_d)/(kc_y * fc_0_d)) + (sigma_m_y_d/fm_y_d) + km * (sigma_m_z_d/fm_z_d)
        util_bendin_comp_z = (abs(sigma_c_0_d)/(kc_z * fc_0_d)) + km * (sigma_m_y_d/fm_y_d) + (sigma_m_z_d/fm_z_d)
        util_LTB_capacity = (sigma_m_y_d/ (k_crit * fm_y_d))**2 + (abs(sigma_c_0_d)/(kc_z*fc_0_d))


# Summary

if sigma_c_0_d >= 0.0:
        util_axial = sigma_c_0_d/fc_0_d
elif sigma_c_0_d < 0:
        util_axial = sigma_c_0_d/(kc*fc_0_d)

util_bending_y_1 = sigma_m_y_d/fm_y_d
util_bending_y_2 = kmod * sigma_m_y_d/fm_y_d

util_bending_z_1 = sigma_m_z_d/fm_z_d
util_bending_z_2 = kmod * sigma_m_z_d/fm_z_d

util_bending_y = min(util_bending_y_1,util_bending_y_2)
util_bending_z = min(util_bending_z_1,util_bending_z_2)

util_shear = tau_d/fv_d


print("\n")
print("Util Axial: {}".format(abs(round(util_axial,2))))
print("Util Bending y: {}".format(abs(round(util_bending_y,2))))
print("Util Bending z: {}".format(abs(round(util_bending_z,2))))
print("Util Shear: {}".format(abs(round(util_shear,2))))

print("\n")
print("Util Combined Bending_y Tension: {}".format(abs(round(util_bendind_tens_y,2))))
print("Util Combined Bending_z Tension: {}".format(abs(round(util_bending_tens_z,2))))
print("Util Combined Bending_y Compression: {}".format(abs(round(util_bendin_comp_y,2))))
print("Util Combined Bending_z Compression: {}".format(abs(round(util_bendin_comp_z,2))))
print("Util Lateral Buckling: {}".format(abs(round(util_LTB_capacity,2))))