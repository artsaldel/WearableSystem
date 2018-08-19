import sys

array = []
with open("configuration.conf", "r") as text:
    for line in text:
    	value = line.split(":")[1].replace("\n","")
        array.append(value)
print(array)
