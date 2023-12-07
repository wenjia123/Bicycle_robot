from numpy import *
from matplotlib.pyplot import *
from scipy import signal
import control
import control.matlab as cnt
from whipple_model import getModelSS

#construct Whipple model of the bike.
param_names = ['a ','b ','c','hrf','mrf','xff','zff','mff','Rfw','mfw','Rrw','mrw','Jyyf','Jyyr','lam']
# params = array([.3,1.02,.08,.9,85,.9,.7,4,.35,3,.3,3,.28*.65,.12*.65,1.25])
params = array([.3,1.02,.08,.9,85,.9,.7,4,.35,3,.3,3,3*.35**2,3*.3**2,1.25])

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
t,spd,tq,roll,rollrate,steer,steerrate = loadtxt("step_data_saved.txt",delimiter=",",unpack=True)
U = mean(spd)#what was the speed of the test
T = mean(tq)#what was the step magnitude?
print("Testing at velocity "+str(U)+" and step torque "+str(T))





#get state space model of bike based on Whipple
sys = getModelSS(U,params)
#perform a step response (default magnitude is 1)
yout,tout = cnt.step(sys)
#scale step response to match data file's torque magnitude
yout*=T

#now plot data vs. whipple
figure()
subplot(2,1,1)
plot(tout,yout[:,0],'k',t,roll,'r')
legend(['Whipple','Webots'])
ylabel('Roll (rad)')
subplot(2,1,2)
plot(tout,yout[:,1],'k',t,steer,'r')
ylabel('Steer (rad)')
xlabel('Time (s)')
show()
