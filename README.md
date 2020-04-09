# SSTA_Learning_Project
### This repostory is for SSTA team in EE595 at University of Southern California. 

## Members and Collaborative Team
Project Instructors: Shahin Nazarian and Mohammad Saeed Abrishami

Team Members:
* [Zhiyu Chen(Andrew)](https://github.com/Zhiyu-Chen-Github)
* [Hsu-Cheng Cheng(Alex)](https://github.com/HCC7952889662)
* [Harmanpreet Singh Kalsi](https://github.com/hkalsi-usc)

Collaborative Team : ATPG Team

## Fast Test of SSTA calculation:
```Bash
python3 ckt_sim.py
```

## SSTA System Diagram
![Diagram](/images/System_overview.PNG)
<p align="right">by ZhiYu</p>

## PDF(Probability Density Function) Object
In the PDF object, the constructor will create a PDF according to the given 5 arguments.
1. mu : mu is the mean value of a giveen data.
2. sigma: sigma is a square of std of a given data.
3. size(default = 201): size is the total number of data points.
4. form: form represents which kinds of PDF. 
5. sample_dist: The distance between 2 sampling points.

## Basic Functions in PDF Object:
1.SUM(PDF) : return the result of the summation of 2 PDFs. Return Type: PDF Object

2.MAX(PDF) : return the result of the maximum of 2 PDFs. Return Type: PDF Object 

3.NORM(mu,sigma,size) : creating the normal PDF data points and stored in PDF Object according to the mu, sigma and size given by the user.

4.decimal_place_generator(): return the number of the decimal place of the Sample_Dist

5.mu(): return the mean value of the PDF Object.

6.std(): return the standard deviation value of the PDF Object.

7.plot(): plot the PDF Object.

## Speed Improved Functions in PDF Object:
data_shrink(): This function delete delay delay in PDF whose probability is too small and can be ignored. By doing this, we can speed up the simulation due to the decrease of data which is needed to be dealt with.  

## Experimental Functions in PDF Object:
1. MAX_of_SUM(PDF p2, PDF pc): do the MAX(self,pc) ,MAX(p2,pc) and do the SUM of those 2 max results and return the final result. Return Type: PDF Object  

2. SUM_of_MAX(PDF p2, PDF pc): do the SUM(self,pc) ,SUM(p2,pc) and do the MAX of those 2 sum results and return the final result. Return Type: PDF Object
These 2 functions are designed for the experiment in PHASE I project, which is to see whether the results are different in these 2 functions.

## Sample Results for c6288 circuit:
![Diagram](/images/c6288.png)

