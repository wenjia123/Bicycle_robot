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


q=zeros(size(tmodel));
rollmodel=zeros(size(tmodel));

#rollmodel[0]=rolldata_range[0];


a=0.51;
lamba=1.25;
m=20;
c=0.08;

V=3.7;
h=1.02;
g=9.81;
b=1.02;


p=V*V*sin(lamba)-b*g*cos(lamba);
D=m*a*h;
J=m*h*h;
a1=(D*V*g)/(J*p);
a0=(m*g*g*(b*h*cos(lamba)-a*c*sin(lamba)))/(J*p);
b1=(D*V*b)/(J*a*c*m*p);
b0=(b*(V*V*h-a*c*g))/(J*a*c*p);
T=0.008;

roll_ss=(b*T*(V*V*h-a*c*g))/(a*c*m*g*g*(b*h*cos(lamba)-a*c*sin(lamba)));
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
print(roll_ss);

for k in range(1,len(tmodel)):
	#if(k>1):
		#rollddot = 0
		#T=k_roll*(d_roll-rollmodel);
		qd=-a0*rollmodel[k-1]-a1*(q[k-1]+b1*T)+b0*T;
		rolld=q[k-1]+b1*T;
		q[k]=q[k-1]+(tmodel[k]-tmodel[k-1])*qd;
		rollmodel[k]=rollmodel[k-1]+(tmodel[k]-tmodel[k-1])*rolld;


figure()
x_interp=np.interp(roll_ss,rollmodel,tmodel);
#t_ss=np.where(rollmodel[roll_ss])
plot(tdata_range,rolldata_range-rolldata_range[0],'b',tmodel,rollmodel,'r',x_interp,roll_ss,'ks')
title('roll angle when using T control')
xlabel('Time (s)')
ylabel('$\phi$ (radians)')
legend(['experiment','model'])

savefig("")


show()
