import requests
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris'
filename = 'iris.data'
with open(filename, 'wb') as ofile:
   response = requests.get(url)
   ofile.write(response.content)