Based on our previous experiments in Webots, it's extremely complicated to adjust the premeters like trail c and fork angle $&lambda;$ for the bike, so we build a PROTO so that we can change the premeters really easy. All the defalut values are based on the Papadopoulos model.



![Screenshot 2023-06-28 142626](https://github.com/wenjia123/Bicycle_robot/assets/97308209/474cf359-0828-4b3d-922e-3e29746008ba)

Next, we tried with differnt controllers to see how the bike can stabilize. First, we used the Torque control: 

1. Open-loop control system Bike can not stabilize.

![open loop system ](https://github.com/wenjia123/Bicycle_robot/assets/97308209/858210c1-f55f-4125-baaa-e92e0a36377e)

2. Close-loop control system
setting $T=k_roll*(roll_d-roll)+k_d(roll_d-roll)$ , the $k_roll$ is getting from the root locus.however, the bike still cannot be stablied. 




![k for roll control](https://github.com/wenjia123/Bicycle_robot/assets/97308209/c630cd6d-f420-4b79-82a8-070283c4a1f9)
![T control](https://github.com/wenjia123/Bicycle_robot/assets/97308209/6d19a955-0e59-4de9-8e17-933082c4d438)

https://github.com/wenjia123/Bicycle_robot/assets/97308209/5f32678a-e118-4990-878c-8968912e8bf7




The reason why the Astrom Torque control doesn't work is  it assumed the front wheel is massless and  there are only 2 energy in the system, one is coming from the yawing and one is from rolling; it also assumed that the Torque applied on the front fork only coming from the Normal force and centrifuge force. But in the reality, we cannot treat the front wheel to be massless. So for our simulation in the Webtos, we set the mass of the front wheel is not zero and it also stored the energy.When the front fork steelling, there are also the gravity of the front wheel and centrifuge force of the front wheel which Astrom's mmodel didn't count in, that's why the Astrom's Torque control doesn't work for our simulation. 



Then, since the Torque control doesn't work in this situation, we tried with the Steering control, we set $&delta;= k_roll *(roll_d-roll)$, $k_(roll)$ is coming from from root locus(graph below). Under the steering control, the bike can be stabilzed.


![root locus for k(roll control)](https://github.com/wenjia123/Bicycle_robot/assets/97308209/24631400-82b9-4227-b974-7c4f402e27f1)

https://github.com/wenjia123/Bicycle_robot/assets/97308209/dd25a0e9-5ce0-4a8f-9f2e-621632da3c10

![roll control](https://github.com/wenjia123/Bicycle_robot/assets/97308209/7d7eafb6-8c94-477d-a160-8738bda8e6be)

