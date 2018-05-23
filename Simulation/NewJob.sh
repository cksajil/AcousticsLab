#!/bin/bash
#Name of job
#$ -N RIR
#$ -cwd
#$ -V
#$ -q hp
#Here we tell the queue that we want the orte parallel enivironment and request 8 slots
#$ -pe orte 8
#$ -S /bin/bash
#command to run
#/home/sajilck/anaconda2/bin/python ClusterSplit.py>log1.txt
/home/sajilck/anaconda2/bin/python RunMeClustered.py>log.txt
