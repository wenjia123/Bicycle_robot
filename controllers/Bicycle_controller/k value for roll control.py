from numpy import *
from matplotlib.pyplot import *
from cmath import*
a=0.51;
lamba=1.25;
m=20;
c=0.08;
V=3.75;
h=1.02;
g=9.81;
b=1.02;

k=arange(0,100,0.1);

D=m*a*h;
J=m*h*h;
a2=J;
a0=m*g*h;
b1=(D*V*sin(lamba))/(b);
b0=(m*(V*V*h-a*c*g)*sin(lamba))/(b);

lam1=( -b1*k+((b1*k)**2-4*a2*(b0*k-a2))**0.5 )/(2*a2);
lam2=( -b1*k-((b1*k)**2-4*a2*(b0*k-a2))**0.5 )/(2*a2);



figure()

#plot(real(lam1), imag(lam1), 'b', real(lam2),imag(lam2),'r')
title('root locus')
xlabel('Real')
ylabel('Image')
legend(['lam1','lam2'])

plot(k,real(lam1),k,real(lam2))
#xlabel('k')
#ylabel('real(lam)')

show()
