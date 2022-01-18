# Exercise 2, GEM5 Design Space Exploration | Computer Architecture
_Bountioukos-Spinaris Athanasios, Semester 7, 2021, AUTh_

## Sector 1. Executing SPEC CPU2006 Benchmarks
### 1. General stats
#### Why the commited and the simulated instructions are different?
Probably I couldnt understand fully the question, but the commtes and the simulated instructions were the same on all benchmarks.
#### Total number of L1 data cache replacements and how could we fild the number of L2 cache accesses without looking at its stat?
The total number of L1 cache replacements is different on every simulation. That's pretty natural because the opperation that each benchmark uses vary. 
 
The CPU accesses the L2 cache when some information cannot be retrieved by the L1 cache. So we could find the number of the L2 accesses finding the L1 cache misses.
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
The price is inversly proportional to the size of the size of the memory. Also, the L1 caches are more expencive than L2 caches. I couldn't find exactly how many times more expencive is but reading [this article] (https://www.extremetech.com/extreme/188776-how-l1-and-l2-cpu-caches-work-and-why-theyre-an-essential-part-of-modern-chips) I will guess that the price differnce of the log2 of L1 cache is 3 times bigger than the log8 of L2 cache. This gives the 3∗(log2(L1i)+log2(L1d))+log8(L2)
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


https://www.extremetech.com/extreme/188776-how-l1-and-l2-cpu-caches-work-and-why-theyre-an-essential-part-of-modern-chips
