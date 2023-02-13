# !pip install python-Levenshtein 

import pandas as pd
from Levenshtein import distance as levenshtein_distance
from geopy.distance import geodesic

df = pd.read_csv("assignment_data.csv") # Read the CSV file

x = df["name"] #To extract name column

lat_log = [] #To add latitude and longitude in (lat,log) format so it's easier to find distance
for i in range(len(df)):
    lat_log.append((df["latitude"][i],df["longitude"][i]))

x = [i.lower() for i in x] #converting captilized to small alphabets to compare easily

x = [i.replace(" ","") for i in x] #Removing space in alphabets to compare easily

#This function helps to measure geodesic distance in meters between two points and pass True if distance is less than 200 else False
def lat_lon_distance(lat_log,x,y):
  if geodesic(lat_log[x],lat_log[y]).meters < 200:
    return True
  else:
    return False

def simillar_alphabets(alphabet,lat_log):
  o = [0]*len(alphabet) # this results in having 0's in a list with a lenth of dataframe
  for i in alphabet: # navigates all elements in x
    for j in alphabet: # navigates all elements in x , two loops to compare among them
       """comparision between themselves ex: [1,2,3] results in {(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)}
           i!=j eliminates (1,1),(2,2),(3,3) 
            and
            alphabet.remove(i) eliminates (2,1),(2,3)
           Therefore O/P : (1,2),(1,3),(3,2)
        """
       if i!=j: 
         k = levenshtein_distance(i,j) # calculate levenshtein_distance
         if k < 2: # eliminates if levenshtein_distance > 2
           index_1 = alphabet.index(i) # capture index of ith element in alphabet
           index_2 = alphabet.index(j) # capture index of jth element in alphabet
           distance = lat_lon_distance(lat_log,index_1,index_2) # mesures distance as per the index_1 nad index_2
           if distance == True:
             # replaces the index of similarities and required distance with 1
             o[index_1] = 1 
             o[index_2] = 1
    alphabet.remove(i)
  return o

s = simillar_alphabets(x,lat_log)

df["is_similar"] = s #creates a column with "is_similar" name and stores s values

df.to_csv("solution.csv")

