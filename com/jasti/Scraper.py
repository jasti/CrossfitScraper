'''
Created on May 19, 2014

@author: jasti
'''
from bs4 import BeautifulSoup 
import requests
import csv
import pandas as pd

# A utility method to generate comments
def generateURL():
    crossfitBaseUrl = 'http://www.crossfit.com/mt-archive2/YYYY_MM.html'
    #yearRange = ["2005","2007","2008","2009","2010","2011","2012","2013"]
    yearRange = range(2002, 2014)
    monthRange = ['01','02','03','04','05','06','07','08','09','10','11','12']
    #monthRange = ['01']
    crossfitUrls = [];
    for year in yearRange:
        for month in monthRange:
            crossfitYearUrl = crossfitBaseUrl.replace('YYYY', str(year))
            crossfitUrl = crossfitYearUrl.replace('MM', str(month))
            crossfitUrls.append(crossfitUrl);
    return crossfitUrls  

# Create all the URLs you need to scrape
urls = generateURL();

# Open a file so you can save your data
with open("workouts.tsv", "w+") as f:
        fieldnames = ("Date", "Workout")
        output = csv.writer(f, delimiter="\t")
        output.writerow(fieldnames)
        for url in urls:
            r = requests.get(url)
            soup = BeautifulSoup(r.text)
            #print soup
            blogBodies = soup.findAll("div", {"class" : "blogbody"})
            for line  in blogBodies:
                #print('\n~break~\n');
                workoutName = line.find("h3", {"class" : "title"})
                #print workoutName
                if workoutName is not None:
                    if(len(workoutName.text.split()) < 2):
                        # Some entries only have the day and not the actual date
                        #workoutDate = np.nan;
                        break;
                    else:
                        #Add 20 to the year part, so Pandas can easily extract the date format
                        workoutDate = "20"+workoutName.text.split()[1];
                para =line.findAll('p')
                workout = "";
                for p in para:
                    # Sometime their workouts have links and they need to be filtered for
                    anchorExists = p.find("a")
                    if (p.text=='Enlarge image') |('Post' in p.text)|('comments' in p.text)|(p.text == "") :
                        break;
                    else:
                        workout = workout+p.text.encode('utf-8') 
                output.writerow([workoutDate,workout.strip().replace('\n',' ')]) 

# Columns you would like to create              
cols =['Date','Workout']
#Read the previously created tab seperated file using Pandas utility
df = pd.read_csv('workouts.tsv', sep='\t', converters={'Date': str})  
#Drop rows that are np.Nan()
df = df.dropna()
#Print the DataFrame
print df
