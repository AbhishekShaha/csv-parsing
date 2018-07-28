# Task1 ![CI status](https://img.shields.io/badge/build-passing-brightgreen.svg)

This program generates a csv file with random names where each line is formated as,
RandomFirstName,RandomLastName,RandomAge
#### Code Snippets
The first snippet of code gets the dictionary listing from the web and returns a list of all the entries in that dictionary.
```python
import urllib.request
import random
import csv

word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
response = urllib.request.urlopen(word_url)
long_txt = response.read().decode()
words = long_txt.splitlines()
```
Then the list to be generated should only upper case words, only "name like" words no abbrivations, and save teh file on local machine. [Complete code file in Script-code folder]

```python
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
    for i in range(10000-3):
        row = (rand_fname(),rand_lname(),random.randint(1, 100))
        writer.writerow(row)
finally:
    f.close()
```


### Requirements
* Linux or Macos
* Python 3.3 and up
* AWS Cli

`$ pip install boto3`

# Task2 ![CI status](https://img.shields.io/badge/build-passing-brightgreen.svg)

This program line by line reads csv file created in Task1 and and writes that lines to `AWS NoSql DynamoDB`
`Usage : ` Once you get the csv file from Task1 upload the file into s3 bucket using aws cli command line or GUI or using boto3 library, the lambda function will trigger on the put event of aws s3, read the data from csv file and write the into into DynamoDB.

![](https://cloudcraft.co/view/adf8cf19-daad-4eb4-9136-84f2470ac49b?key=vSJ6v-rvOafh0SlJhenzdA)
![](https://github.com/AbhishekShaha/csv-parsing/tree/master/screenshots/a.png)

## Code Snippet

```python
import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb','eu-west-1')

def csv_reader(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    obj = s3.get_object(Bucket=bucket, Key=key)
    
    rows = obj['Body'].read().split('\n')
    
    table = dynamodb.Table('csv_parse')
    
    with table.batch_writer() as batch:
        for row in rows:
            
            batch.put_item(Item={
                
                'FirstName':row.split(',')[0],
                'LastName':row.split(',')[1],
                'Age':row.split(',')[2]
            })
```
### Requirements
* AWS s3 bucket
* IAM role with policies attached has access to DynamoDB, S3 and CloudWatch services 
* AWS Cli to upload csv into s3 bucket to trigget the lambda function

## Usage
```
aws s3 --profile abhishek cp Desktop/genesys/data.csv s3://genesys-code-test/
Or
Use boto3 as:

import boto3
s3 = boto3.resource('s3')
bucket = s3.Bucket('genesys-code-test')
s3.Object('genesys-code-test', 'Desktop/genesys/data.csv').put(Body=open('Desktop/genesys/data.csv', 'rb'))
```

