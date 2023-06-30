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

p=V*V*sin(lamba)-b*g*cos(lamba);
D=m*a*h;
J=m*h*h;
a2=J;
a1=(D*V*g)/(p);
a0=(m*g*g*(b*h*cos(lamba)-a*c*sin(lamba)))/(p);
b1=(D*V*b)/(a*c*m*p);
b0=(b*(V*V*h-a*c*g))/(a*c*p);

lam1=(-(a1+b1*k)+((a1+b1*k)*(a1+b1*k)-4*a2*(a0+b0*k))**0.5)/(2*a2);
lam2=(-(a1+b1*k)-((a1+b1*k)*(a1+b1*k)-4*a2*(a0+b0*k))**0.5)/(2*a2);



figure()

#plot(real(lam1), imag(lam1), 'b', real(lam2),imag(lam2),'r')
plot(k,real(lam1),k,real(lam2))
title('root locus')
xlabel('Real')
ylabel('Image')
legend(['lam1','lam2'])

show()
