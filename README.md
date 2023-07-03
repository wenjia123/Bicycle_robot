Based on our previous experiments in Webots, it's extremely complicated to adjust the premeters like trail c and fork angle $&lambda;$, so we build a PROTO for the basic bicycle that we can change the premeters really easy. All the defalut values are based on the Papadopoulos model.



![Screenshot 2023-06-28 142626](https://github.com/wenjia123/Bicycle_robot/assets/97308209/474cf359-0828-4b3d-922e-3e29746008ba)

Next, we want to try with differnt controllers to see how bike can stabilize. First, we use the open-loop control system with the Torque applied on the front fork. Bike can not stabilize. (graph), then, we used close-loop control system, setting $T=k_roll*(roll_d-roll)+k_d(roll_d-roll)$ , the $k_roll$ is getting from the root locus. (graph), however, the bike still cannot be stablied. 

The reason could be, the Astrom front fork Model assumed that the wheels are massless, there are no inertia and energy stored in wheels. However, in Webots, we cannot set the mass of wheels to be 0, so the bike we built has a really small mass which is 1kg. This could be a reason why we cannot use the Torque control based on the Astrom model to achieve the bike stabilization in the real life.


Then, we tried with steering control, we set $&delta;= k_roll *(roll_d-roll)$, $k_(roll)$ is coming from from root locus(graph below). Under the steering control, the bike can be stabilzed. 

