#! /usr/bin/python

# ********Task 1 : CSV Generator *******

import urllib.request
import random
import csv

word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
response = urllib.request.urlopen(word_url)
long_txt = response.read().decode()
words = long_txt.splitlines()

upper_words = [word for word in words if word[0].isupper()]
name_words = [word for word in upper_words if not word.isupper()]
one_name = ' '.join([name_words[random.randint(0, len(name_words))] for i in range(1)])


def rand_fname():
    name = ','.join([name_words[random.randint(0, len(name_words))] for i in range(1)])    
    return name

def rand_lname():
    name = ','.join([name_words[random.randint(0, len(name_words))] for i in range(1)])    
    return name

f = open("data.csv", 'wt')
try:
    writer = csv.writer(f)
    writer.writerow( ('FirstName','LastName', 'Age') )
    for i in range(100-3):
        row = (rand_fname(),rand_lname(),random.randint(1, 100))
        writer.writerow(row)
finally:
    f.close()


#import boto3
#s3 = boto3.resource('s3')
#bucket = s3.Bucket('genesys-code-test')
#s3.Object('genesys-code-test', 'Desktop/genesys/data.csv').put(Body=open('Desktop/genesys/data.csv', 'rb'))