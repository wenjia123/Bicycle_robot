from numpy import *
from matplotlib.pyplot import *
import control as cnt

#load the data file from webots:
data = loadtxt("webots_data.txt",delimiter=",")
tdata = data[:,0]
speeddata = data[:,1]
rolldata = data[:,2]
steerdata = data[:,3]
rollratedata = data[:,4]
steerratedata = data[:,5]
yData = data[:,6]

t_step=1;
steptime = 3000 #ms
stepindex = int(steptime/t_step)
tdata_range=tdata[stepindex:]-tdata[stepindex]
rolldata_range=rolldata[stepindex:]

#tmodel = arange(tdata_range[0],tdata_range[-1],0.001);
tmodel=arange(tdata_range[0],tdata_range[-1],0.01);
# tmodel = arange(tdata_range[0],100,0.001);


rollmodel=zeros(size(tmodel));
rollmodeld=zeros(size(tmodel));
#rollmodel[0]=rolldata_range[0];#rollmodel[0]=rolldata_range[0];


a=0.51;
lamba=1.25;
m=20;
c=0.08;

V=3.75;
h=1.02;
g=9.81;
b=1.02;

D=m*a*h;
J=m*h*h;
a2=J;
a0=m*g*h;
b1=(D*V*sin(lamba))/(b);
b0=(m*(V*V*h-a*c*g)*sin(lamba))/(b);
rolld=0.1;
k_roll=8;


#roll_sstest=(b*T*(V*V*h-a*c_test*g))/(a*c_test*m*g*g*(b*h*cos(lamba)-a*c_test*sin(lamba)));

#print("open loop eigenvalues are at +/-:")
#print(sqrt(g/h))
#print("open loop zero is at:")
#print(roots([a*h*V/b, V**2*h/b]))
#print("closed loop eigs are:")
#print(roots([1, a*V*km/(b*h), (V**2*km/(b*h) - g/h)]))
#cl_eigs = roots([1, a*V*km/(b*h), (V**2*km/(b*h) - g/h)])

#sys = cnt.tf([a*h*V/b, V**2*h/b],[h**2, 0, -g*h])
#cnt.rlocus(sys)
#plot(cl_eigs.real,cl_eigs.imag,'rx',markersize=15)

for k in range(1,len(tmodel)):
	rollmodeldd=( b1*k_roll*(rolld-rollmodeld[k-1])+b0*k_roll*(rolld-rollmodel[k-1])+a0*rollmodel[k-1]  ) / (a2);
	rollmodeld[k]=rollmodeld[k-1]+(tmodel[k]-tmodel[k-1])*rollmodeldd;
	rollmodel[k]=rollmodel[k-1]+(tmodel[k]-tmodel[k-1])*rollmodeld[k-1];

figure()

plot(tdata_range,rolldata_range,'b',tmodel,rollmodel,'r')
title('roll angle when using roll control')
xlabel('Time (s)')
ylabel('$\phi$ (radians)')
legend(['experiment','model'])

savefig("")


show()
