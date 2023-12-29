# Overview

A simple python code that accesses the canvas api, authenticates via access key, retrieves assignment data and calculates a final grade (in %, letter grades can be implemented if needed).

## Instructions 

-Clone repository into local system

-Install necessary packages with `pip install -r requirements.txt`

## 2 ways to run the code 

### Direct through command-line

-Run using your own Canvas API key with the following command: 

`
python3 grade.py --api_key YOUR_API_KEY
`

### Environment Variable 

-Create file called '.env', inside file should contain the following: 

~~~      
      API_KEY = " *Insert your canvas api access key here "
~~~

*The access key can be created via canvas account settings

-Save and run with the following command: 

`
python3 grade.py
` 
