import os
import requests
import hashlib
import pandas as pd

pd.options.display.max_columns = None
pd.options.display.max_rows = None


def hash_function(input_str, salt):
        """Run pbkdf2_hmac with a 20byte salt, and 120,000 round on the input."""
        if input_str is None:
                return None
        return hashlib.pbkdf2_hmac('sha256', input_str.encode(), salt.encode(), 120000)

url = "https://randomuser.me/api/?results=500"
res = requests.get(url).json()
print("completed get request")

# flatten json
df = pd.json_normalize(res['results'])

today = pd.to_datetime('today').normalize()

# create ID's
df['user_id'] = range(1, len(df.index)+1)
df['address_id'] = pd.factorize(df["location.street.number"].astype(str)
                                        + df["location.street.name"]
                                        + df["location.city"]
                                        + df["location.state"]                                
                                        + df["location.postcode"].astype(str)
                                        + df["location.coordinates.latitude"]
                                        + df["location.coordinates.longitude"])[0]
# hash sensitive data
df["login.password"] = df["login.password"].apply(lambda x: hash_function(x, os.environ['PASSWORD']))
df["id.value"] = df["id.value"].apply(lambda x: hash_function(x, os.environ['PII']))
print("Sensitive data hashed")

# ------ address table ------ 
drop_columns = [
                "login.uuid",
                "login.username",
                "login.password",
                "login.salt",
                "login.md5",
                "login.sha1",
                "login.sha256",
                "id.name",
                "id.value",
                "gender",
                "email",
                "phone",
                "cell",
                "nat",
                "name.title",
                "name.first",
                "name.last",
                "dob.date",
                "dob.age",
                "registered.date",
                "registered.age",
                "picture.large",
                "picture.medium",
                "picture.thumbnail",
                "user_id"
                ]
subset_drop_na =  ["location.street.number",
                "location.street.name",
                "location.postcode",
                "location.coordinates.latitude",
                "location.coordinates.longitude",
                "location.timezone.offset",
                "location.timezone.description",
                "location.city",
                "location.state",
                "location.country"]

df_address = df.drop(drop_columns , axis=1).dropna(subset=subset_drop_na, how='all')

rename_columns = {
                "location.street.number": "number",
                "location.street.name": "name",
                "location.postcode": "postcode",
                "location.coordinates.latitude": "latitude",
                "location.coordinates.longitude": "longitude",
                "location.timezone.offset": "offset",
                "location.timezone.description": "description",
                "location.city": "city",
                "location.state": "state",
                "location.country": "country",
                                }
df_address.rename(columns=rename_columns, inplace=True)

file_name = str(today).split(" ")[0].replace("-","") + "_address.csv"
df_address.to_csv(file_name, encoding='utf-8', index=False)
print("saved address csv table")

  # ------ user table ------ 
drop_columns = [
                "login.uuid"
                , "login.username"
                , "login.password"
                , "login.salt"
                , "login.md5"
                , "login.sha1"
                , "login.sha256"
                , "location.street.number"
                , "location.street.name"
                , "location.postcode"
                , "location.coordinates.latitude"
                , "location.coordinates.longitude"
                , "location.timezone.offset"
                , "location.timezone.description"
                , "location.city"
                , "location.state"
                , "location.country"
                , "id.name"
                , "id.value"
                , "nat"
                        ]
df_users = df.drop(drop_columns , axis=1).dropna(how="all")

rename_columns = {
                                "name.title" : "title"
                                , "name.first" : "first_name"
                                , "name.last" : "last_name"
                                , "gender": "gender"
                                , "nat": "nationality"
                                , "dob.date": "dob_date"
                                , "dob.age": "dob_age"
                                , "registered.date": "registered_date"
                                , "registered.age": "registered_age"
                                , "email" : "email"
                                , "phone" : "phone"
                                , "cell" : "cell"
                                , "picture.large" : "picture_large"
                                , "picture.medium" : "picture_medium"
                                , "picture.thumbnail" : "picture_thumbnail"
                                }
df_users.rename(columns=rename_columns, inplace=True)

file_name = str(today).split(" ")[0].replace("-","") + "_users.csv"
df_users.to_csv(file_name, encoding='utf-8', index=False)
print('User table csv saved')

# ------ login table ------
drop_columns = [
                "login.salt",
                "login.md5",
                "login.sha1",
                "login.sha256",
                "location.street.number",
                "location.street.name",
                "location.postcode",
                "location.coordinates.latitude",
                "location.coordinates.longitude",
                "location.timezone.offset",
                "location.timezone.description",
                "location.city",
                "location.state",
                "location.country",
                "id.name",
                "id.value",
                "gender",
                "email",
                "phone",
                "cell",
                "nat",
                "name.title",
                "name.first",
                "name.last",
                "dob.date",
                "dob.age",
                "registered.date",
                "registered.age",
                "picture.large",
                "picture.medium",
                "picture.thumbnail",
                "address_id"
                ]

df_login = df.drop(drop_columns , axis=1).dropna(subset=["login.uuid"])


rename_columns = {
                        "login.uuid": "uuid",
                        "login.username": "username",
                        "login.password": "password",
                                }
df_login.rename(columns=rename_columns, inplace=True)
df_login.head()

file_name = str(today).split(" ")[0].replace("-","") + "_login.csv"
df_login.to_csv(file_name, encoding='utf-8', index=False)
print("Saved login data csv")

