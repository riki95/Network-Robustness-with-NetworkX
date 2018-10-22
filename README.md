# Network Robustness with NetworkX
This script is able to do attacks on a network in order to break his components and see the changing on the graph.

## Getting Started

To download my repo:

```
git clone https://github.com/riki95/Network-Robustness-with-NetworkX
```

The program was written in Python and compiled with Python 3.6 so you need it to run.
The program needs a graph in input which is a csv file and I used the Bitcoin Alpha Dataset.

You will also need my graph analysis script that you find here:

```
https://github.com/riki95/Bitcoin-Graph-study-with-NetworkX
```
The imports are already done because you will need only some specific functions. Just hold the files in the same directory and you're good to start.

### Bitcoin Alpha Dataset

The [Bitcoin Alpha Dataset](https://snap.stanford.edu/data/soc-sign-bitcoin-alpha.html) is a csv file that consists on 4 columns:
```
SOURCE, TARGET, RATING, TIME
```

I've decided to only study Source, Target and Rating because Time was not so important to care about.
You can just download my repo and you will find the dataset with the first row removed (it was the one with the Column's names) or you can download it from the official website.

## Reproduce experiments

Reproducing experiments is very easy, running this command on terminal is enough:

```
python network_robustness.py
```
You will see the analysys on the terminal that is increasing the number of nodes removal for different kind of centralities and in the folder of the Python script will appear a **Data** folder. Inside of it you will file some png files that represent the plots of the graph and the growth of the components number and other important data.

You can modify the Graph in input and the analysis is quite the same. Obviously you have to adapt some methods. 

You can also set to True or False some variables at the very top in order to print or not / plot or not some values or images.

## Plots examples

Thanks to this script you will be able to reproduce these images of your Graph. First of all, the Graph will be printed:

![Graph Image 1](https://i.imgur.com/FRIOkP2.jpg)

You can modify colors, nodes, scales and so on. But then the script will start removing nodes and at the end you will get a graph like this (basing on how many nodes removed and how):

![Graph Image 2](https://i.imgur.com/6jGElWV.jpg)

You will now plot some data about the node removal, for example how the diameter change:

![Diameter Image](https://i.imgur.com/wsj9hR8.png)

And finally, one of the most important data is to see the change of the components number and giant component size:

![Components Image](https://i.imgur.com/9LJJrAE.png)

## Authors

* **Riccardo Basso** - *Università degli studi di Genova*
