# Exercise 3 | Energy-Delay-Area Product Optimization (gem5 + McPAT) | Computer Architecture

_Bountioukos-Spinaris Athanasios, Semester 7, 2022, AUTh_

## Sector 1. Introduction to McPAT

### 1. Paper Review

#### McPAT validation

McPAT is based on a paper called "McPAT: An Integrated Power, Area, and Timing Modeling Framework for Multicore and Manycore Architectures", publicized in the 42th IEEE/ACM International Symposium on Microarchitecture (MICRO) in 2009. Based to the paper, the CPUs used are **Niagara** (running at 1.2GHz with a 1.2V power supply), **Niagara2** (running at 1.4GHz with a 1.1V power supply), **Alpha 21364** (running at 1.2GHz with a 1.5V power supply) and **Xeon Tulsa** (running at 3.4GHz with a 1.25V power supply).

### 2. McPAT outputs

#### Power outputs

The power on the McPAT simulation is depicted in 3 forms. All the power is calculated with the sum of these 3 and from this formula:

![power formula](https://github.com/n45os/Advanced-Computer-Architecture-Exercise-3-1-2022/blob/main/power_formula.png)

**Dynamic Power**: the dynamic power that is spent in charging and discharging the capacitive loads when the circuit switches state, where C is the total load capacitance, Vdd is the supply voltage, ∆V is the voltage swing during switching, and fclk is the clock frequency. C depends on the circuit design and layout of each IC component; we calculate it using analytic models for regular structures such as memory arrays and wires, along with empirical models for random logic structures such as ALUs. The activity factor α indicates the fraction of total circuit capacitance being charged during a clock cycle. We calculate α using access statistics from architectural simulation together with circuit properties.

**Short Circuit Power**: the short-circuit power that is consumed when both the pull-up and pull-down devices in a CMOS circuit are partially on for a small, but finite amount of time. Short-circuit power is about 10% of the total dynamic power. When circuit blocks switch, they consume both dynamic and short-circuit power. The inherent circuit property determines the ratio of the short-circuit power to the dynamic power, which is a strong function of the Vdd to Vth ratio. Since the Vdd to Vth ratio shrinks for future low power designs, short-circuit power is expected to become more significant in future designs that require lower power and longer battery life.

**Static Power**: the static power consumed due to leakage current through the transistors, which in reality function as “imperfect” switches. There are two distinct leakage mechanisms, and the magnitude of each leakage current is proportional to the width of the transistor and depends on the logical state of the device.

#### Leakage

When it comes to leakage, there are two types of leakage. 
The first type of leakage, **_subthreshold leakage_,** occurs when a transistor that is supposedly in the off state actually allows a small current to pass between its source and drain. We let Isub denote the subthreshold through a unit-sized (off) transistor. 
The second type, _**gate leakage**_, is the current that leaks through the gate terminal. 
In order to model the leakage current for a circuit block with many transistors, we need to consider which logical state each transistor is in, then sum up the leakage current components for each. 

#### Observations

If we run different programs in a CPU, the power numbers will change accordingly. The dynamic power and the short circuit power will increase as the number of the instructions run by the CPU are increased. If we now run a program that doesn't have many instructions but it takes time to run, we will observe a rise on the static power consumption.

### 3. An Example of 2 Programs Running

If we have a battery of a given capacity and two CPUs, one with power consumption of 25W and one of 35W, then McPAT could easily give us the information we need to go to a conclusion of which CPU can stay more time on powered of the battery.

The power of the CPU is separated in many metrics, and by this we can lead to our conclusion. For example, if a CPU have a better performance when running a program but its static power consumtion is high, then for a given program that is very complex, if we can run this very fast, we can have an energy efficient run. In the other hand, if a CPU is slow but has a very small static power can run a program that is not complex but it needs time to finish better. So, the answer is that having the information that we get from McPAT, a 35W CPU could run a program with less batter consumed than a 25W CPU.

### 4. An Applied Example

In this example we have a hypothetical problem that can be run to Xeon CPU 40 times faster than the ARM 9A CPU. We have to prove using the McPAT that, even given these facts, A9 can be more energy efficient.

Looking at the numbers (https://github.com/n45os/Advanced-Computer-Architecture-Exercise-3-1-2022/tree/main/info) we can easily see that the peak power of the ARM A9 (1.74189 W) is about 80 times less than the Xeon's (134.938 W). We can also observe a 400 times bigger leakage of the Xeon CPU (0.108687 W to 36.8319 W). Taking these numbers in consideration, we can confirm that even if a program runs 40 times faster in a CPU, we cannot lead to the conclusion that it is more energy efficient because we have to take in consideration the leakage, when the CPU is idle.

## Sector 2. gem5 + McPAT: Optimizing EDAP Product

### 1. EDAP

The information for the **area** can be found just running the McPAT program and looking at the first lines. 

The total **energy** will be calculated using the total power, multipling it with the runtime of the run.

I didn't really understand what you mean with "delay". 
a) If the **delay** is the runtime of the system, then we can get this information of the stats.txt file of the GEM5 output. 
b) If it means how much time the system stayed idle waiting for something else to finish, then we could get this informaton comparing the static power with the total power and getting the proportion of this fraction of the total runtime: **(static_power/total_power)runtime**
For now I will use the first one.

### 2. Adding information to the Exercise 2 Outputs

In order to make possible this section of the exercise, I used the data from the previous exercise. To combine the GEM5 data with the McPAT as input I wrote a script in python. The script takes all the files and uses the GEMToMcPAT.py script to make the xml file and then it inputs it to the McPAT. I used the data from one of the benchmarks of the second exercise, the specbzip benvhmark.

The data that I collected, I used it to make the below graphs.

![power formula](https://github.com/n45os/Advanced-Computer-Architecture-Exercise-3-1-2022/blob/main/graph.png)

In order to make compare the graphs, I made a normalization on the cost function of the exercise 2. We can see that there is some kind of corelation between the numbers but not as distinctive as I was expecting it to be. Especially bad results can be seen when the area and the peak power is low, the cost function seems to rise. I probably have to do some changes to make it more realistic.

This is probably because the cost function I made was taking in consideration the speed of the CPU as well and I did not use this value on the graph.


## Exercise Review

Σε γενικές γραμμές, και πάλι η εργασία ήταν αρκετά κατατοπιστική και η κατανόηση των περισσότερων ερωτημάτων ήταν εύκολη. Αυτό που με μπέρδεψε αρχικά ήταν το setup και δεν κατάλαβα εξαρχής ότι κάποιες από τις οδηγίες του setup ήταν για troubleshooting και όχι για το installation και μου έφαγε κάποιες ώρες το ότι έσπασαν τα linux και έκανα εξαρχής εγκατάσταση. Η δευτερη δυσκολία που αντιμετώπισα είναι το να καταλάβω τι είναι το delay στο γινόμενο EDAP, το οποίο ακόμα δεν έχω καταλάβει και δεν μπόρεσα να βγάλω άκρη και ούτε στην επεξήγηση που δίνεται στο επίσημο paper.


### sources:

https://www.hpl.hp.com/research/mcpat/

https://www.hpl.hp.com/research/mcpat/micro09.pdf
