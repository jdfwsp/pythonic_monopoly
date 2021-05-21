# 🐍🏘️🎩 PYTHONIC MONOPOLY 🎩🏘️🐍
![San Francisco image by Joost Daniels](https://lp-cms-production.imgix.net/2019-06/9cf024dfd5c0bcb2b17f4785340145ea-san-francisco.jpg)
Image by Joost Daniels
#### This is an analysis of rentals in the neighborhoods of San Francisco, CA.  It examines the average price per square foot and gross rent in every neighborhood over a 5-year period.  The first notebook works out all of the analysis:
[Rental Anlysis](https://github.com/jdfwsp/pythonic_monopoly/blob/main/Code/rental_analysis.ipynb)

#### This second notebook organizes the analysis code so that it can be displayed in a Panel presentation:
[Dashboard](https://github.com/jdfwsp/pythonic_monopoly/blob/main/Code/dashboard.ipynb)

## Procedure for viewing the presentation
#### Enter these commands into your terminal (GitBash or WSL on Windows):
### Step 1 : Clone the repository
```
git clone https://github.com/jdfwsp/pythonic_monopoly.git
```
### Step 2 : Enter the directory containing the script
```
cd pythonic_monopoly/Code
```
### Step 3 : Display script permissions
```git pus
ls -l run.sh
```
🚨 You should get an output like this with ``run.sh`` marked as executable (with an x)- proceed to Step 4
```

-rwxrwxr-x 1 user user      27 May 20 12:14 run.sh
```
🚨 If you see this, it is NOT executable- proceed to Step 3+
```
-rw-rw-r-- 1 user user      27 May 20 12:14 run.sh
```
### Step 3+ : Make script executable
```
chmod +x run.sh
```
### Step 4 : Execute script
```
./run.sh
```
### Step 5 : Open presentation in browser
Paste ``http://localhost:5006/dashboard`` into your browser and explore the Dashboard!!




