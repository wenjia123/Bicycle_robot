from numpy import *
### PHYSICAL PARAMETERS
m_rider = 0.
h_rider = 0.5
#overall
b = 0.767 #wheelbase
c = 0.02285999 #trail
alph = 1.16 # 1.16 is from Fusion 2/14/23 #1.186 #90-rake: measured from forward x
g = 9.81 #gravity
v = 3 # forward speed

#rear wheel
Rrw = 0.15875 # radius of real wheel
mrw = 2.462 #mass of rear wheel
Axx = 0.027708579 #moment of inertia of rear wheel about x
Ayy = 0.033968214 #moment of inertia of rear wheel about y
Azz = 0.027708579 #moment of inertia of rear wheel about z

#rear frame
mrf = 11.065 #kg, rear frame mass
xrf = .3386 #position of rear frame CG
yrf = 0
hrf = .25606 + (h_rider*m_rider + .25606*mrf)/(mrf+m_rider)
mrf = mrf+m_rider

#mass moments of rear frame
Bxx = 0.1+m_rider*h_rider**2
Bxz = -0.017
Byy = 0.31
Bzz = 0.249

#front frame
xff = .62218#position of front frame CG
yff = 0
hff = .46531
mff = 2.2047 #mass of front frame
Cxx = 0.0659
Cxz = 0.02565
Cyy = 0.06293
Czz = 0.03182

#front wheel
Rfw = 0.15875
mfw = 1.486
Dxx,Dyy,Dzz = 0.016724187,0.020502342,0.016724187


#intermediate terms

#total
mt = mrw+mrf+mff+mfw #total mass
xt = (xrf*mrf+xff*mff+b*mfw)/mt #CG location x
ht = (Rrw*mrw+hrf*mrf+hff*mff+Rfw*mfw)/mt #CG location z
#print("CoM: x: "+str(xt)+", z: "+str(ht))
print("Total mass: "+str(mt)+", Z CoM: "+str(ht))
Txx = Axx+Bxx+Cxx+Dxx+mrw*Rrw**2 +mrf*hrf**2 + mff*hff**2 +mfw*Rfw**2 #global inertia XX
Txz = Bxz+Cxz-mrf*xrf*hrf-mff*xff*hff-mfw*b*Rfw
Tzz = Azz+Bzz+Czz+Dzz+mrf*xrf**2+mfw*b**2
#print("Txx: "+str(Txx))
#print("Txz: "+str(Txz))
#print("Tzz: "+str(Tzz))

#front frame
mf = mff+mfw
xf = (mff*xff+b*mfw)/mf
hf = (hff*mff+Rfw*mfw)/mf
Fxx = Cxx+Dxx+mff*(hff-hf)**2+mfw*(Rfw-hf)**2
Fxz =  Cxz - mff*(xff-xf)*(hff-hf)+mfw*(b-xf)*(-Rfw+hf)
Fzz = Czz+Dzz+mff*(xff-xf)**2 + mfw*(b-xf)**2
#print("Fxx: "+str(Fxx))
#print("Fxz: "+str(Fxz))
#print("Fzz: "+str(Fzz))

#steering frame
lam = pi/2 - alph #angle of steering axis with global z in the vertical plane
u = (xf-b-c)*cos(lam)+hf*sin(lam) #perp distance that CM of front is ahead of steering axis
Fll = mf*u**2+Fxx*sin(lam)**2-2*Fxz*sin(lam)*cos(lam)+Fzz*cos(lam)**2
#print("ff lambda inertia: "+str(Fll))
#print("u: "+str(u))

Flx = (-mf*u*hf - Fxx*sin(lam) + Fxz*cos(lam))
Flz = mf*u*xf - Fxz*sin(lam)+Fzz*cos(lam)
#print("Flx: "+str(Flx))
#print("Flz: "+str(Flz))

f = c*cos(lam)/b #ratio of trail to wheelbase

#angular momentum divided by speed:
Sr = Ayy/Rrw
Sf = Dyy/Rfw
St = Sr+Sf

#frequently appearing static moment term:
Su = mf*u+f*mt*xt

#print(Sf)
print(xf)
prinr(hf)
print(lam)
print(xt)
print(ht)