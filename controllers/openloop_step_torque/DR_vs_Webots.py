from numpy import *
from matplotlib.pyplot import *
#rcParams['text.usetex'] = True
from scipy import signal
import control
import control.matlab as cnt
from whipple_model import getModelSS

#construct Whipple model of the bike.
param_names = ['a ','b ','c','hrf','mrf','xff','zff','mff','Rfw','mfw','Rrw','mrw','Jyyf','Jyyr','lam']
# params = array([.3,1.02,.08,.9,85,.9,.7,4,.35,3,.3,3,.28*.65,.12*.65,1.25])
#params = array([.6888,1.45,0.115,0.5186,158.1,1.25,0.7347,10,0.356,10,0.33,13,0.62424,0.6795,1.1])
params = array([.6888,1.45,0.115,0.5186,158.1,1.25,0.7347,10,0.356,10,0.33,13,0.79811,0.832866,1.1])

#params = array([.708,1.45,0.115,0.509,158.1,1.25,0.7347,10,0.356,10,0.33,13,.3,.3,1.1])

def getEigsVecs(params):
    #create a vector of velocities to investigate
    vvec = arange(.01,10,.01)
    #create a second copy of this vector that is four rows. This will make plotting easier
    vvec2 = zeros((4,len(vvec)))

    #our model is fourth order, so will have 4 eigenvalues. each can have a real and/or imaginary part.
    eigs_re = zeros((4,len(vvec)))
    eigs_im = zeros((4,len(vvec)))

    for k in range(0,len(vvec)):
        #get current velocity
        v = vvec[k]
        #get state space model at this speed
        sys= getModelSS(v,params)
        #get eigenvalues at this speed
        eigs,vecs = linalg.eig(sys.A)
        #get real parts and place in proper matrix for storage
        eigs_re[:,k] = real(eigs)
        #get imaginary parts and place in proper matrix for storage
        eigs_im[:,k] = imag(eigs)
        #fill up velocity vector corresponding with each eigenvalue
        vvec2[:,k] = [v,v,v,v]
    return vvec,eigs_re,eigs_im
######################## EIGS VS SPEED ##########################

vvec, eigs_re, eigs_im = getEigsVecs(params)
figure()
plot(vvec,eigs_re[0,:],'k.',vvec,eigs_im[0,:],'k')
xlabel('Speed (m/s)')
ylabel('Eigenvalue (1/s)')
legend(['real','imaginary'])
plot(vvec,eigs_re[1,:],'k.',vvec,abs(eigs_im[1,:]),'k')
plot(vvec,eigs_re[2,:],'k.',vvec,abs(eigs_im[2,:]),'k')
plot(vvec,eigs_re[3,:],'k.',vvec,abs(eigs_im[3,:]),'k')
ylim([-10,10])
######################## STEP RESPONSE ##########################

#load data file from webots:
t,spd,tq,roll,rollrate,steer,steerrate = loadtxt("/Users/wenjia/Desktop/Bicycle_robot/controllers/openloop_step_torque/DR_step_data.txt",delimiter=",",unpack=True)
U = mean(spd)#what was the speed of the test
T = mean(tq)#what was the step magnitude?
X0 = array([roll[0],steer[0],rollrate[0],steerrate[0]])
print("Testing at velocity "+str(U)+" and step torque "+str(T))





#get state space model of bike based on Whipple
sys = getModelSS(U,params)
#perform an lsim using measured torque and initial condition values
yout,tout,xout = cnt.lsim(sys,tq,t,X0)


#now plot data vs. whipple
figure()
subplot(2,1,1)
plot(tout,yout[:,0],'k',t,roll,'r')
legend(['DR_model','Webots'])
title('$U=$ '+str(round(U,2))+"m/s; $T_\delta=$ "+str(round(T,2))+"Nm; $\phi_0=$"+str(round(roll[0],2))+" rad")

ylabel('Roll (rad)')
subplot(2,1,2)
plot(tout,yout[:,1],'k',t,steer,'r')
ylabel('Steer (rad)')
xlabel('Time (s)')
show()
