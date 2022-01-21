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














### 2. Observations on the produced stats

![benchmark stats](https://github.com/n45os/Advanced-Computer-Architecture-Exercise-1-11-2021/blob/main/GEM5_memoryRAM.png)
As we look at the graph we can make some interesting observations. Firstly, while the specmcf benchmark has the worst performance (by a lot) when it comes to L1 i cache miss rate, it is not the worst performing benchmark (contrary, it performs the best CPI-wise). The worst performing benchmark is the specsjeng, which has the biggest L2 cache miss rate. That’s because the L2 cache is way slower than the L1 and the lack of performance on it can make the CPU very slow.
We can also see that MinorCPU does a great job handling specbzip benchmark keeping balanced performance on the memory.

### 3. Changing the CPU clock

Looking at the stats.txt file we can see that by changing the —cpu-clock=1.5GHz, it changes the CPU clock and not the system clock. I’m not sure but I assume that -for example- doubling the cpu clock is the equivalent of adding one more CPU in our system. The system and the cpu clock have the same values in a real single core machine.
The scaling is not perfect and this is natural because MinorCPU uses a pipeline and even using more cpu clocks in the same system time (like adding a CPU), we cannot perfectly parallelize all our processes.

## Sector 2. Design Exploration

### Testing for different parameters

The possibilities of the different parameters of the memory of the MinorCPU are about 15,000, so I tried to run one benchmark for fewer instructions and for fewer parameters to approximate the optimal combination of these. So, I ran the specbzip benchmark with some of the values of the parameters and collected the cpi of each simulation wuth a simple python script.

This test showed that the cachline size plays a significant role at the decreasement of the cpi. The second measurement that we could extract from an observation is the size of the L2 cache. The bigger the L2 cache, the better the performance of the CPU. The CPIs were sorted according to this measurement. In the benchmark and in its first 100000 instructions we couldn't extract any info about the L1 d cache size nor it's associativity. The L1 i cache showed an improvement when it was decreased and did not show a difference in the associativity.

The next step is to run another test, this time keeping L2 size and coachline size the highest possible and we’ll try to get an observation about the other parameters. Running it we can see that in this benchmark the CPI gets better when we decrease the L1 i and d cache.

With this approach I could get some usefull information about the first benchmark. Although, it was very time consuming and it needed really good automization. So I tried another approach as well.

### Another approach

According to our measurements of the previous questions, we will run about 20 times each benchmark with values that the previous measurements could stabilise. For example, specsjeng benchmark has a bad performance for L1 data cache and the L2 cache so we will increase these values.

In order to get it done, I made a python script that gave all these values to the simulations and ran them one by one. Then the CPIs are collected in a file and I can see the performance of the simulations.

## Sector 3. Performance/Cost Optimisation

### Making the cost formula

We need to focus to 3 parameters that affect the performance/cost ratio:

* manufacturing price
* speed
* complexity

The final ratio will be evaluated according to these parameters and the CPI.

* #### Manufacturing price

The price is inversly proportional to the size of the size of the memory. Also, the L1 caches are more expencive than L2 caches. I couldn't find exactly how many times more expencive is but reading [this article] (<https://www.extremetech.com/extreme/188776-how-l1-and-l2-cpu-caches-work-and-why-theyre-an-essential-part-of-modern-chips>) I will guess that the price differnce of the log2 of L1 cache is 3 times bigger than the log8 of L2 cache. This gives the 3∗(log2(L1i)+log2(L1d))+log8(L2)

* #### Speed

The speed depends on the size of the memory as well. Although because the use of the cache can be also optimazed from the compilers and the software in general, we'll multiply this price with 0.8. Also it is known that the L1 cache is about 10 times faster than L2. I also chose 80 as the weight. So, we will have this 80/log2(L1i)+80/log2(L1d)+8/log8(L2)

* #### Complexity

The complexty has to do with the associetivity and the cacheline size. We'll use the log2 of the associetivity on each cache and the log4 of the cachline size divided by 2.
So we get this: log2(L1iassoc)+log2(L1dassoc)+log2(L2assoc)+log4(cls)/2

We need to give weight to the CPI of the CPU, so we won't just multiply the sum of the above with the CPI but will multiply it with the cube of the CPI. We will get:
**CPI^3[3∗(log2(L1is)+log2(L1ds))+log8(L2s)+
80/log2(L1i)+80/log2(L1d)+8/log8(L2)+
log2(L1iassoc)+log2(L1dassoc)+log2(L2assoc)+log4(cls)/2]**

Now having the outputs of the previous question, we can find the optimal combination or the parameters, according to my cost/performance formula.

## Exercise Review

Η εργασία ήταν πολύ κατανοητή από την εκφώνηση της. Το αρχείο έδινε τις απαραίτητες πληροφορίες για να ξεκινήσει κάποιος να μαθαίνει τον gem5 ακόμα και χωρίς κανένα γνωστικό υπόβαθρο. Τα βήματα για την εκτέλεση της προσομοίωσης ήταν πολύ κατανοητά και κατατοπιστικά.

Ένα σημείο που μάλλον θα χρειαστεί μια διώρθωση είναι σε ένα σημείο που εξηγεί πως να τρέξουμε τον gem5 με το αρχείο se.py και -στην δική μου έκδοση τουλαχιστον- δεν μπόρεσε να τρέξει όπως επιδεινύοταν. Μετά από μερικό ψάξιμο στο documentation βρήκα ότι στα flags αντί για "--cpu" πρέπει να χρησιμοποιηθεί το "--cpu-type" και πριν δωθεί το εκτρλέσιμο πρέπει να συνοδευτεί με το flag --cmd.

Σε γενικές γραμμές μπορώ να πω ότι δεν υπήρξε σημείο που κόλλησα και κάτι που υπήρχε γραμμενο στις οδηγείες δεν το κατλάβαινα.

<https://www.extremetech.com/extreme/188776-how-l1-and-l2-cpu-caches-work-and-why-theyre-an-essential-part-of-modern-chips>
