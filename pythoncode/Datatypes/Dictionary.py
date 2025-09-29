# Dictionary the data will be stored in key & Value pair  
# json data will work better than dictionary 
d1 = {"Name":"John", "Age":30, "City":"New York"}
print(d1)
print(type(d1))
print(d1.keys())
print(d1.values())
print(d1["Name"])

#Nested dictionary information 

cloud_infra = {
    "aws":{
        "region": "us-east-1",
        "services": ["ec2", "s3", "lambda"]

    },
    "azure":{
        "region": "eastus",
        "services": ["vm", "blob", "functions"]
    },
    "gcp":{
        "region": "us-central1",
        "services": ["compute", "storage", "functions"]
    }
}
print(cloud_infra)
print(cloud_infra["aws"]["services"][1])
print(cloud_infra["azure"]["region"])





