import datetime

timestring = '2021-04-08T17:28:59.000000Z'

timeepoch = int(datetime.datetime.strptime(timestring,'%Y-%m-%dT%H:%M:%S.%f%z').timestamp())

print(timeepoch)