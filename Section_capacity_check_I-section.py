#section capacity check I-Section

import Rhino.Geometry as rg
import math

"""
input:
    Depth (h)-mm
    top flange width (b_top)-mm
    bottom flange width (b_bottom)-mm
    Web thickness (tw)-mm
    Top Flange thickness (tf_top)-mm
    Bottom flange Thickness (tf_bottom)-mm
    material properties
    gamma_M0

output:
    tensionUtilisation
    bendingUtilisation
"""

gamma_M0 = 1.0
gamma_M1 = 1.0
gamma_M2 = 1.1

upsilon= 0.3
G= E/2*(1+upsilon)
eta = 1.2 if fy<= 460 else 1

var_set= [h,b_top, b_bottom, tw, tf_top, tf_bottom]

if any(i<=0 for i in var_set):
  raise ValueError('Negative or zero value detected')
elif any (i<=3 for i in var_set) :
    raise ValueError('Thickness is less then 3 mm') 

Area = (h*tw) + (b_top-tw)*tf_top + (b_bottom-tw)*tf_bottom
h_web = h-tf_bottom-tf_top #web height excluding flange thickness

A1= b_bottom*tf_bottom ; y1= tf_bottom/2  #bottom flaneg area
A2= (h-tf_bottom-tf_top)*tw ; y2= h/2     #web area
A3= b_top*tf_top ; y3= h/2- tf_top/2      #top flange area

cy_pos = (A1*y1 + A2*y2 + A3*y3)/(A1 + A2 + A3)
cy_neg = h - cy_pos

Iy1= b_bottom*tf_bottom**3/12; Iy2 = tw*(h-tf_bottom-tf_top)**3/12; Iy3 = b_top*tf_top**3/12   
Iy = Iy1 + A1*(cy_pos- y1) + Iy2 + A2*(cy_pos- y2) + Iy3 + A3*(cy_pos- y3)
Iz_web= (h-tf_bottom-tf_top)*tw**3/12
Iz = tf_bottom*b_bottom**3/12 + Iz_web + tf_top*b_top**3/12


alpham = [0.13, 0.21, 0.34, 0.49, 0.76]  #buckling curves
epsilon = math.sqrt(235/fy)


#Shear Area
Av_z = max(h*tw, eta*A2) #web max area
Av_y = A1 + A3   #flange area only

[Rx_0, Ry_0, Rz_0,Mxx_0, Myy_0, Rx_1, Ry_1, Rz_1,Mxx_1, Myy_1]= [1,1,1,1,1,1,1,1,1,1]

#Torsional property and checks
if T!=0: 
    h_web_T= h_web + (tf_bottom + tf_top)/2
    #h0 =2*((dy-t) + (dz-t))
    #Ah = (dy-t)*(dz-t)
    J= (b_bottom*tf_bottom**3 + b_top*tf_top**3 + h_web_T*tw**3)/3  #torsional constant
    Cw= h_web_T**2*tf_bottom*tf_top*b_bottom**3*b_top**3/(12*(tf_top*b_top**3 + tf_bottom*b_bottom**3))   #warping constant

    K_t = Lb*math.sqrt(G*J/(E*Cw))

    if [Mxx_0, Myy_0, Mxx_1, Myy_1] == [0,0,0,0] : #Mxx, Myy,MZZ end moment restrain; Rx,Ry,Rz = end translation restrain
        alpha_T = 3.7 ; beta_T = 1.08
    elif [Mxx_0, Myy_0, Mxx_1, Myy_1] == [1,1,1,1] :
        alpha_T = 6.9 ; beta_T = 1.14
    elif [Rx_0, Ry_0, Rz_0, Rx_1, Ry_1, Rz_1] == [0,0,0,1,1,1] or [Rx_0, Ry_0, Rz_0, Rx_1, Ry_1, Rz_1] == [1,1,1,0,0,0]:
        alpha_T = 2.7 ; beta_T = 1.11

    chi_torsion = 1/(beta_T + (alpha_T/K_t)**2)
    T_warp = T*(1-chi_torsion)
    T_vernant = T*chi_torsion
    
    #Trd= Cw*(fy/math.math.sqrt(3))/gamma_M0


var_classsection = [h,b_top, b_bottom, tw, tf_top, tf_bottom,epsilon]

def classSection_I_Compression(var_set):  #class section for compression in Y
    c_web= h-tf_top- tf_bottom
    c_flange_top = (tf_top-tw)/2
    c_flange_bottom = (tf_bottom-tw)/2

    if (b_bottom != b_top) or (tf_top != tf_bottom):  #check if unsymmetrical I-section, considering elasric capacity always
        
        if (c_web/tw <= 42*epsilon) and (i<=14*epsilon for i in [c_flange_top/tf_top, c_flange_bottom/tf_bottom]) :
            classSection = 3
        else:
            raise ValueError('section unsymmetrical and in class 4')
    else:
        if c_web/tw <= 33 * epsilon and (i<=9*epsilon for i in [c_flange_top/tf_top,c_flange_bottom/tf_bottom]):
            classSection = 1
        elif c_web/tw <= 38 * epsilon and (i<=10*epsilon for i in [c_flange_top/tf_top,c_flange_bottom/tf_bottom]) :
            classSection = 2
        elif c_web/tw <= 42 * epsilon and (i<=14*epsilon for i in [c_flange_top/tf_top,c_flange_bottom/tf_bottom]):
            classSection = 3
        else:
            raise ValueError('section in class 4')
    
    return classSection

def classSection_I_Moment(var_set):  #class section for compression in Z
    c_web= h-tf_top- tf_bottom
    c_flange_top = (tf_top-tw)/2
    c_flange_bottom = (tf_bottom-tw)/2

    if b_bottom != b_top or tf_top != tf_bottom:  #check if unsymmetrical I-section, considering elastic capacity always, check in with marco
        if c_web/tw <= 124*epsilon and (i<=14*epsilon for i in [c_flange_top/tf_top,c_flange_bottom/tf_bottom]):
            classSection=3
        else: 
            raise ValueError('section unsymmetrical and in class 4')

    else:
        if c_web/tw <= 72 * epsilon and (i<=9*epsilon for i in [c_flange_top/tf_top,c_flange_bottom/tf_bottom]):
            classSection = 1
        elif c_web/tw <= 83 * epsilon and (i<=10*epsilon for i in [c_flange_top/tf_top,c_flange_bottom/tf_bottom]):
         classSection = 2
        elif c_web/tw <= 124 * epsilon and (i<=14*epsilon for i in [c_flange_top/tf_top,c_flange_bottom/tf_bottom]):
            classSection = 3
        else:
            raise ValueError('section in class 4')
    return classSection

def classSection_I_Compression_Moment(var_set):  #class section for compression in Z
    c_web= h-tf_top- tf_bottom
    c_flange_top = (tf_top-tw)/2
    c_flange_bottom = (tf_bottom-tw)/2

    alpha_local_web= 0.5*(1+ abs(Ned)/(fy*c_web*tw))
    alpha_local_flange_top= 0.5*(1+ abs(Ned)/(fy*c_flange_top*tf_top))    # check if c*tf is correct for area
    alpha_local_flange_bottom=0.5*(1+ abs(Ned)/(fy*c_flange_bottom*tf_bottom))

    psi_web= 2*Ned/(c_web*tw*fy) - 1
    psi_flange_top= 2*Ned/(c_flange_top*tf_top*fy) - 1
    psi_flange_bottom= 2*Ned/(c_flange_bottom*tf_bottom*fy) - 1

    if psi_flange_top == 1 :
        k_sigma_top= 0.43
    elif 0< psi_flange_top < 1 :
        k_sigma_top = 0.578/(psi_flange_top + 0.34)
    elif psi_flange_top == 0:
        k_sigma_top= 1.7
    elif -1< psi_flange_top< 0 :
        k_sigma_top = 1.7 - 5*psi_flange_top + 17.1*psi_flange_top**2
    elif psi_flange_top == -1 :
        k_sigma_top= 23.8
    

    if psi_flange_bottom == 1 :
        k_sigma_bottom= 0.43
    elif 0< psi_flange_bottom < 1 :
        k_sigma_bottom = 0.578/(psi_flange_bottom + 0.34)
    elif psi_flange_bottom == 0 :
        k_sigma_bottom= 1.7
    elif -1< psi_flange_bottom< 0 :
        k_sigma_bottom = 1.7 - 5*psi_flange_bottom + 17.1*psi_flange_bottom**2
    elif psi_flange_bottom == -1 :
        k_sigma_bottom= 23.8
    

    if alpha_local_web >0.5:
        class_1_limit= 396*epsilon/(13*alpha_local_web - 1)
        class_2_limit= 456*epsilon/(13*alpha_local_web - 1)
    else :
        class_1_limit= 36*epsilon/alpha_local_web
        class_2_limit= 41.5*epsilon/alpha_local_web

    if psi_web > -1:
        class_3_limit = 42*epsilon/(0.67 + 0.33*psi_web)
    else :
        class_3_limit= 62*epsilon*(1-psi_web)*math.sqrt(abs(psi_web))



    if b_bottom != b_top or tf_top != tf_bottom:  #check if unsymmetrical I-section, considering elasric capacity always
        if c_web/tw <= class_3_limit and c_flange_top/tf_top<= 21*epsilon*math.math.sqrt(k_sigma_top) and c_flange_bottom/tf_bottom<=21*epsilon*math.math.sqrt(k_sigma_bottom):
            classSection = 3
        else: 
           raise ValueError('section Unsymmetrical and in class 4') 
    else:
        if c_web/tw <= class_1_limit and c_flange_top/tf_top<=9*epsilon/alpha_local_flange_top and c_flange_bottom/tf_bottom<=9*epsilon/alpha_local_flange_bottom  :
            classSection = 1
        elif c_web/tw <= class_2_limit and c_flange_top/tf_top<=10*epsilon/alpha_local_flange_top and c_flange_bottom/tf_bottom<=10*epsilon/alpha_local_flange_bottom :
            classSection = 2
        elif c_web/tw <= class_3_limit and c_flange_top/tf_top<= 21*epsilon*math.math.sqrt(k_sigma_top) and c_flange_bottom/tf_bottom<=21*epsilon*math.math.sqrt(k_sigma_bottom) :
            classSection = 3
        else:
            raise ValueError('section in class 4')
    return classSection


if Medy/Ned + Medz/Ned <= 0.05: # if moment arm is 0.05 of the section capacity, do check this value 
    classSection= classSection_I_Compression(var_set)
elif Ned/Medy + Ned/Medz <= 0.05 : # have to check this
    classSection = classSection_I_Moment(var_set)
else:
    classSection = classSection_I_Compression_Moment(var_set)





# shear Check
var_shear= [Vedy,Vedz, Av_y,Av_z, fy, gamma_M0, T] 
def shearCheck(var_shear):
    if (h_web/tw > 72*epsilon/eta) :  #only applies for unstiffened webs, have to make an boolean toggle for this
        sigma_E = math.pi**2*E*tw**2/(12*(1-upsilon**2)*h_web**2)     #EN 1993-1-5 , A.1
        k_tau_st = max(9*(h_web/Lb)**2*math.pow(math.pow((Iz_web/tw**3*h_web), 3),1/4) , 2.1*math.pow(Iz_web/h_web,1/3)/tw, 1/3)    #Lb= a EN 1993-1-5 , A.3
        k_tau = 5.34 + 4*(h_web/Lb)**2 + k_tau_st # if a/h_web <=1 , else k_tau = 4 + 5.34*(h_web/Lb)**2 + k_tau_st - ignore for web without stiffner only
        lamda_w = 0.76*math.sqrt(fy/(k_tau*sigma_E))
        if lamda_w < 0.83/eta:   #1993-1-5 , 5.2
            chi_w = eta  
        elif 0.83/eta <= lamda_w < 1.08 :
            chi_w = 0.83/lamda_w
        else:
            chi_w = 1.37/(0.7 + lamda_w)
        
        VplRdy = chi_w*fy*h_web*tw/(math.sqrt(3)*gamma_M1)
    else: 
        VplRdy = (Av_y * (fy/math.sqrt(3)) )/gamma_M0
    
    VplRdz = (Av_z * (fy/math.sqrt(3)) ) / gamma_M0

    if T !=0 :
        tau_ed_web = T_vernant/tw  #shear stress due to torsion, where T is saint venant torsion
        tau_ed_flange = T_vernant/min(tf_bottom,tf_top)
    VplRdy = (1-(tau_ed_web/(fy/math.sqrt(3)/ gamma_M0)))*VplRdy
    VplRdz = (1-(tau_ed_flange/(fy/math.sqrt(3)/ gamma_M0)))*VplRdz
    shearUtilisation_y = Vedy/VplRdy # for combined shear in both direction
    shearUtilisation_z = Vedz/VplRdz
    
    return VplRdy, VplRdz, shearUtilisation_y, shearUtilisation_z

shearUtilisation_y= shearCheck(var_shear)[2]
shearUtilisation_z= shearCheck(var_shear)[3]


if shearUtilisation_y < 0.5 and shearUtilisation_z < 0.5:
    rho = 0
else:
    rho =  ((2*shearUtilisation) -1)**2 # does this make sense? (shear Utilization)
fy = (1-rho)*fy


# bending check
var_moment= [h,b_top, b_bottom, tw, tf_top, tf_bottom]

def Moment_check(var_set) :
    #section modulus check
    if classSection == 3:
        Wly = Iy/max(cy_pos, cy_neg) #elastic modulus y-y
        Wlz = Iz/max(b_top, b_bottom) #elastic modulus z-z
    elif classSection == 1 or 2 :
        Wly= (h-cy_neg-tf_bottom)**2*tw/2 + b_bottom*tf_bottom*(cy_pos-(tf_bottom/2))  #plastic modulus y-y
        Wlz = (A3*b_top+ A1*b_bottom)/4    #plastic modulus z-z
    else:
        raise valueerror('section in Class4, too slender')

    MRdy = Wly*fy/gamma_M0 
    MRdz = Wlz*fy/gamma_M0

    # 6.2.9 bending + axial
    Ncpr= (Area * fy) / gamma_M0 #compression plastic resistance

    if Ned > 0.25*Ncpr or Ned > 0.5*h_web*tw*fy/gamma_M0:
        n = Ned/Ncpr
        a= min((area - A1- A3)/area, 0.5)
        MRdy = min(MRdy*(1-n/(1- 0.5*a)), MRdy)
    elif Ned > h_web*tw*fy/gamma_M0:
        if n>a:
            MRdz = MRdz*(1- ((n-a)/(1-a))**2)
    
    Ma= 100 #bending moment at quater point have to get Ma,Mb,Mc value from opensees analysis
    Mb = 100 #bending moment at mid point
    Mc = 100 #bending moment at end point
    M_max = 100 #maximum bending moment on the member
    Cb = 12.5*M_max/(2.5*M_max + 3*Ma + 4*Mb + 3*Mc)  # shape factor based on bending diagram (AISC), only applies for moment in Y-Y

    #EN-1993-1-1 6.3.2.2
    k=1 ; k_w = 1  # end rotation factor ; end warping factor, have to include this going forward
    L_ltb = Lb ; k_ltb = 1 #length of unbraced member  # effective length factor for lateral torsional buckling, overriding L_ltb
    L_cr_ltb = L_ltb*k_ltb # effective critical length


    M_cr = Cb*math.pi**2*E*Iz*(math.sqrt((k*Cw/(k_w*Iz)) + (L_cr_ltb**2*G*J/(math.pi**2*E*Iz))))/L_cr_ltb**2  # , M_cr critical Bending moment
    Lamda_lt = math.sqrt(Wly*fy/M_cr)
    beta_lt = 0.75 #recommended value
    Lamda_lt_0 = 0.4 # recommended value

    if type==0 :
        if h/min(b_bottom,b_top) <= 2: #hot rolled sections
            alpha_lt = alpham[1]
        else:
            alpha_lt = alpham[2]
    if type== 1 :
        if h/min(b_bottom,b_top) <= 2:    #cold form section
            alpha_lt = alpham[3]
        else:
            alpha_lt = alpham[4]

    phi_lt = 0.5*(1 + alpha_lt*(Lamda_lt - Lamda_lt_0) + beta_lt*Lamda_lt**2)
    chi_lt = min(1/(phi_lt + math.sqrt(phi_lt**2 - beta_lt*Lamda_lt**2)), 1, 1/(Lamda_lt**2))

    if chi_lt <1:
         MRdy =chi_lt*MRdy

    return MRdy, MRdz 

MRdy = Moment_check(var_moment)[0]
MRdz = Moment_check(var_moment)[1]


var_Axial = [Ned,Area,fy,Lb, Lb,gamma_M0, type]
# compression Check

def Axial_check(var_Axial):

    NplRd = (Area * fy) / gamma_M0
    if Ned <=0 : # - indicates member in tension
        Nrd = NplRd    #require sign to be assigned to tesion force
    else:
        Ncpl =  NplRd
        k_cr_y = 1 ; k_cr_z = 1 ; Lcry= k_cr_y*Lb ; Lcrz= k_cr_z*Lb # k_cr is effective length factor in respective direction

        Ncry = math.pi**2*E*Iy/Lcry**2   #euler critical buckling y direction
        Ncrz = math.pi**2*E*Iz/Lcrz**2   #euler critical buckling z direction
        Lamda_y = math.math.sqrt((Area*fy)/Ncry) ; Lamda_z = math.math.sqrt((Area*fy)/Ncrz) #slenderness ratio
        if type == 0 : #0= hot rolled, 1= cold formed
            if h/min(b_bottom, b_top) >1.2:
                if min(tf_bottom, tf_top) <= 40: #mm:
                    if fy>420: #Mpa:
                        alpha_y = alpham[0] 
                        alpha_z = alpham[0]
                    else:
                        alpha_y = alpham[1] 
                        alpha_z = alpham[2]
                elif 40< min(tf_bottom, tf_top) <= 100 : #mm
                    if fy>420: #Mpa:
                        alpha_y = alpham[1] 
                        alpha_z = alpham[1]
                    else:
                        alpha_y = alpham[2] 
                        alpha_z = alpham[3]
                else:
                    raise ValueError('flange thickness out of limits')
            
            else:
                if min(tf_bottom, tf_top) <= 100 :  #mm:
                    if fy>420: #Mpa:
                        alpha_y = alpham[1] 
                        alpha_z = alpham[1]
                    else:
                        alpha_y = alpham[2] 
                        alpha_z = alpham[3]
                elif  min(tf_bottom, tf_top) >100 : #mm
                    if fy>420: #Mpa:
                        alpha_y = alpham[3] 
                        alpha_z = alpham[3]
                    else:
                        alpha_y = alpham[4] 
                        alpha_z = alpham[4]
                else:
                    raise ValueError('flange thickness out of limits')    
        elif type == 1 :
            if min(tf_bottom, tf_top) <= 40 : #mm:
                alpha_y = alpham[2] 
                alpha_z = alpham[3]
            else:
                alpha_y = alpham[3] 
                alpha_z = alpham[4]

        phi_y= 0.5*(1 + alpha_y*(Lamda_y - 0.2) + Lamda_y**2) 
        phi_z= 0.5*(1 + alpha_z*(Lamda_z - 0.2) + Lamda_z**2)
        chi_yy = 1/(phi_y+ math.sqrt(phi_yy**2 - Lamda_y**2))
        chi_zz = 1/(phi_z+ math.sqrt(phi_zz**2 - Lamda_z**2))

        Nbrd_y= chi_yy*Ncpl ; Nbrd_z= chi_zz*Ncpl
        Nbrd = min(Nbrd_y, Nbrd_z)
        Nrd= min(Ncpl, Nbrd)
    return Nrd

Nrd = Axial_check(var_Axial)

# need to add second order effecrs for bending + axial



# bending-cpmpression reduction in bending capacity due to compression probably can igonore it, have to confirm with marco

#n = Ned/Nrd
#MnRd = Wpl*fyred*(1-math.pow(n,1.7))

if Ned>0:
    combine_Utilisation = abs(Ned)/Nrd
elif Ned <= 0:
    combine_Utilisation = abs(Ned)/Nrd + Medy/MRdy + Medz/MRdz
print(combine_Utilisation)

shearUtilisation = max(shearUtilisation_y ,shearUtilisation_z)

print("classSection: {}".format(classSection))
print("Ned/Nrd = {}".format(Ned/Nrd))
print("reduced yield strength= {}".format(fy))

print("Nrd: {} kN".format(round(Nrd/1000)))
print("VplRd: {} kN".format(round(shearUtilisation/1000)))
print("Mrdy: {} kNm".format(round(MRdy/1000000,2)))
print("Mrdz: {} kNm".format(round(MRdz/1000000,2)))
