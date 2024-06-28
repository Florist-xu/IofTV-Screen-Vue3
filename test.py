import requests

url = "http://192.168.1.112:5000/add_locations"
aid = 12
gid = 10
laddr = 4
locset = ""
nameid = 1

for i in range(1, 20):
    lid = 104 + i
    lname = f"E-{i:02d}"
    ldes = str(i)
    
    data = {
        "lid": lid,
        "aid": aid,
        "gid": gid,
        "laddr": laddr,
        "ldes": ldes,
        "lname": lname,
        "locset": locset,
        "nameid": nameid
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print(f"Successfully added data for lid: {lid}, lname: {lname}")
    else:
        print(f"Failed to add data for lid: {lid}, lname: {lname}, Status Code: {response.status_code}, Response: {response.text}")
