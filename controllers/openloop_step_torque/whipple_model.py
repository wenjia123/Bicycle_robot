from numpy import *
from matplotlib.pyplot import *
from scipy import signal
import control

def getModelMDK(U,params):
    g = 9.81 #m/s/s, graUitational constant
    a ,b ,c,hrf,mrf,xff,zff,mff,Rfw,mfw,Rrw,mrw,Jyyf,Jyyr,lam = params
    mr = mrw+mrf #mass of rear frame includes rear wheel
    hr = (mrf*hrf+mrw*Rrw)/(mr) #CG height of rear frame includes rear wheel
    Sf = Jyyf/Rfw
    Sr = Jyyr/Rrw
    St = Sf+Sr
    mf = mff+mfw #total mass of front frame includes front wheel
    xf = (mff*xff+b*mfw)/mf# total front frame x position including front wheel
    hf = (zff*mff+Rfw*mfw)/mf #total front frame mass height including front wheel
    u = hf*cos(lam)-(b+c-xf)*sin(lam) #perpendicular distance from steer axis to front frame CG (positive if CG in front of steer axis)

    #build terms for the MDK model based on Eqn32
    M11 = mr*hr**2 + mf*hf**2
    M12 = -mf*hf*u- c*sin(lam)/b*(mf*xf*hf+mr*hr*a)
    M21 = -mf*hf*u- c*sin(lam)/b*(mf*xf*hf+mr*hr*a)
    M22 = mf*(u**2+2*c*sin(lam)/b*xf*u)+c**2*sin(lam)**2/b**2*(mr*a**2+mf*xf**2)
    D11 = 0
    D12 = U*sin(lam)/b*(-mr*hr*a - mf*xf*hf)-U*c*sin(lam)/b*(mf*hf+mr*hr)-U*c*sin(lam)/b*(Jyyf/Rfw+Jyyr/Rrw)-U*Jyyf/Rfw*sin(lam)
    D21 = U*c*sin(lam)/b*(Jyyf/Rfw+Jyyr/Rrw)+Jyyf/Rfw*U*sin(lam)
    D22 = U*sin(lam)/b*mf*xf*u + U*c*sin(lam)**2/b**2*(mr*a**2+mf*xf**2)+U*c*sin(lam)/b*mf*u+U*c**2*sin(lam)**2/b**2*(mf*xf+mr*a)
    K11 = -(mr*g*hr+mf*g*hf)
    K12 = mf*g*u+g*c*sin(lam)/b*(mf*xf+mr*a)-U**2*sin(lam)/b*(mf*hf+mr*hr)-U**2*sin(lam)/b*(Jyyf/Rfw+Jyyr/Rrw)
    K21 = mf*g*u + g*c*sin(lam)/b*(mr*a+mf*xf)
    K22 = -mf*g*u-g*c*sin(lam)*cos(lam)/b*(mr*a+mf*xf) + U**2*sin(lam)/b*mf*u+U**2*c*sin(lam)**2/b**2*(mf*xf+mr*a) + Jyyf/Rfw*U**2*sin(lam)*cos(lam)/b

    M = array([[M11, M12],[M21, M22]])
    D = array([[D11, D12],[D21, D22]])
    K = array([[K11, K12],[K21, K22]])

    return M,D,K,eye(2)


def getModelSS(v,params):
    #first get the model in MDK form
    M,D,K,F = getModelMDK(v,params)
    A = hstack((zeros((2,2)),eye(2,2)))#first create the 'top half' of A matrix
    A = vstack((A,hstack((dot(-linalg.inv(M),K),dot(-linalg.inv(M),D)))))# now fill in bottom half
    B = vstack((zeros((2,2)),dot(linalg.inv(M),F)))#now stack zeros on top of our M^-1F term
    #trim B so it only takes steer.
    B = vstack(B[:,1])
    C = array([[1,0,0,0],[0,1,0,0]]) #choose the 'outputs' as just roll and steer
    D = 0 #with two possible inputs, two possible outputs, there are four terms in the D matrix when output eqn is y = Cx+Du
    sys = control.StateSpace(A,B,C,D)
    return sys
