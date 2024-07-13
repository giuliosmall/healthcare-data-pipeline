# Welcome to the Mighty Data Engineering Test 

we are a small patient advocat group (PAG) who help and monitor patients with various diseases. We have a contract with United Healthcare and Humana, clients of the firm. Although we are not allowed to see all details of United healthcare, we are allowed to see some aggregate data. The same goes for patients without a health insurance.

The sample dataset that we have managed acquire exists of patient data, procedures, insurance companies, a single hospital and a linking file. 

We would like to get a more accurate, and live reporting of this data. In the past the excel files were fine, but nowadays its becoming too much and therefore harder to read. Some of our Program managers are struggling to know what is what. For the client reporting we are not always allowed to show them all the data, and since we are hosting the data we are not allowed to share personal details. Some clients also request an extract of the patient data specific to them. 

We are currently in the process of setting up a database connection to tableau, since we already have a salesforce account and tableau can be used for reporting. We have an airbyte instance to run a few etls on a daily basis to a reporting data warehouse (postrgres database). This database is also one which we are connecting to tableau. We already have some way of creating excel files and providing them to our clients. Most of our infratstructure runs on AWS, and we use python and SQL as our main languages for many applications and data analysis. We have started a transition to use DBT in stead of SQL, but Rome was not built in a day. 

## Task 1: Data Cleaning

Starting with and looking at input/procedures.csv we would like you to create a script that cleans the data and removes duplicates. Where possible slightly alter the data for the purpose of cleaning it, and having less duplicates. 

next add one new column to the csv that shows the overall duration of the procedure in seconds

follwing this, extract the year, month (name), week (number) and days (name) into new columns 

Finally, use python to filter out the procedures that cost more than 30000 per day. 

please include a small reasoning in code, to explain the purpose of use and reasoning of use. 

## Task 2 ETL pipeline

extract the data from input, transform it (specifically for procedures.csv) and load it into a relational database. It should suffice to only do the cleaning from task one, but do take into account the effects it has on the other data. Where possible normalize the data even more.

finally use this data to write a query to rank the payers, by costs payed. Write a query to get the top 5 highest costing patients, and a query to get the top 5 most expensive procedures on a daily basis (median). 


## Task 3 Data marts

After succesfully extracting the data and loading it into a relational database, create two new separate data marts about the data from both of our clients (united healthcare and humana). If you feel the need/usefullness of staging tables, you can use them. Please use as much detail as possible for the data mart, but try and keep it clean. It is preferred to have the least amount of duplicates, and in all honesty we do not really care about patients, but we do care about those who have to pay for procedures themselves.

## Notes
We know some of the questions are vague and maybe impossible to do given the tools you are using. This is on purpose. We want to see how you would handle these situations, therefore it is okay to include an explanation of the process/solution that you would suggest had you been using the tools that do support these requirements. 

## Instructions

Step one is to go to: "https://github.com/myTomorrows/MightyDataEngineeringTest" and download this as a zip, or fork it into your own private repository (preferably github). 
Step 2 is to give us access to this repository. You do not have to give us access immediately, this can be done after you have completed the test as well. You will be given a notice who to add to your repository. 
Finally, you may do the tasks described above in any way you like. Input contains the data that is used for the test and this readme file contains the questions. Good luck and above all, have fun!
