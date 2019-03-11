'''
NAME: Animesh Chaudhry
PROJECT: vAuto Programming Challenge
DATE Submitted: Mar. 10, 2019

'''

import requests
import json

"""
Base API url
"""
base_url = 'http://vautointerview.azurewebsites.net'


###################### Generic Functions used throughout ################################################

################ Generic Method 1: Generic Function that gets the required JSON data ################
"""
Methond name: get_ID_Info
Purpose: Retrieves either Dataset ID, Vehicle ID, or Information About a vehicle.
            Depends on the url provided as a parameter
Parameters: API url (url)
Return: The retrieved Dataset ID, Vehicle ID, or Information About a vehicle in JSON format
"""


def get_ID_Info(url):
    response = requests.get(url)
    json_data = json.loads(response.text)
    return(json_data)


################ Generic Method 2: Gets all key values from a JSON file/object ################
def get_keys(dl, keys_list):
    if isinstance(dl, dict):
        keys_list += dl.keys()
        map(lambda x: get_keys(x, keys_list), dl.values())
    elif isinstance(dl, list):
        map(lambda x: get_keys(x, keys_list), dl)


"""
DatasetID_url
URL to obtain a new Dataset ID
GET -- /api/datasetId -- Creates new dataset and returns its ID
Obtain the new dataset_id
"""
DatasetID_url = base_url + '/api/datasetId'
dataset_id = get_ID_Info(DatasetID_url)[get_ID_Info(
    DatasetID_url).keys()[0]]


"""
vehicle_id_url
URL to obtain the list of vehicle ID's from the specified dataset
GET -- /api/{datasetId}/vehicles -- Get a list of all vehicleids in dataset
"""
vehicle_id_url = base_url + '/api/' + dataset_id + '/vehicles'


"""
The List of Vehicle ID's for a given dataset
"""
Vehicle_ID_List = get_ID_Info(vehicle_id_url)[
    get_ID_Info(vehicle_id_url).keys()[0]]


###################### API Method 1: Obtain Vehicle info ######################
"""
Methond name: get_vehicle_info
Purpose: Retrives the Vehicle info
Parameters: The list of Vehicle ID's (Vehicle_ID_List)
Return: List of vehicle info JSON Objects
Sample JSON object in list: {u'make': u'Ford', u'dealerId': 356723490, u'model': u'F150', u'vehicleId': 2313441577, u'year': 2009}
"""


def get_vehicle_info(Vehicle_ID_List):
    vehicle_info_list = []
    for i in Vehicle_ID_List:
        vehicle_id_url = base_url + '/api/' + \
            dataset_id+'/vehicles/' + str(i) + ''

        response = requests.get(vehicle_id_url)
        json_data = json.loads(response.text)
        vehicle_info_list.append(json_data)
    return vehicle_info_list


###################### API Method 2: Obtain the names of the Dealers ######################
"""
First we obtain all the vehicle info to get the dealer ID's
"""
Vehicle_Info = get_vehicle_info(Vehicle_ID_List)

"""
Methond name: get_Dealer_Name
Purpose: Retrives the Dealer names based on dataset ID and dealer ID
Parameters: Dataset ID
Return: List of dealer ID's along with Dealer names as JSON Objects
Sample JSON object in list: {u'dealerId': 143456738, u'name': u"Doug's Doozies"}
"""


def get_Dealer_Name(dataset_id):
    dealer_list = []
    dealer_URL = []
    for i in range(len(Vehicle_Info)):
        dealer_URL.append(base_url + '/api/' +
                          dataset_id + '/dealers/' +
                          str(Vehicle_Info[i][Vehicle_Info[i].keys()[1]]) + '')
    dealer_URL = list(dict.fromkeys(dealer_URL))
    for i in range(len(dealer_URL)):
        response = requests.get(dealer_URL[i])
        json_data = json.loads(response.text)
        dealer_list.append(json_data)
    return dealer_list


###################### API Method 3: POST to the Answer Endpoint ######################
"""
{u'make': u'Bentley', u'dealerId': 609649738,
    u'model': u'Mulsanne', u'vehicleId': 1888393329, u'year': 2016}
{u'dealerId': 1358760607, u'name': u'House of Wheels'}
"""


def post_answer(dealer_list, vehicle_list):
    """Base JSON to post as answer"""
    answer = """
            {
                "dealers": [
                    {
                        "dealerId": 0,
                        "name": "string",
                        "vehicles": [
                            {
                                "vehicleId": 0,
                                "year": 0,
                                "make": "string",
                                "model": "string"
                            }
                        ]
                    }
                ]
            }
"""

    answer = json.loads(answer)
    """All the necessary keys needed for the construction of the Answer JSON object"""
    keys = []
    get_keys(answer, keys)
    dealer_key = str(keys[0])  # dealers
    vehicle_key = str(keys[1])  # vehicles
    dealer_id_key = str(keys[2])  # dealerId

    for i in range(len(dealer_list)):
        answer[dealer_key].append(dealer_list[i])
        answer[dealer_key][i+1][vehicle_key] = []
        for j in range(len(vehicle_list)):
            if(str(dealer_list[i][dealer_id_key]) == str(vehicle_list[j][dealer_id_key])):
                answer[dealer_key][i+1][vehicle_key].append(vehicle_list[j])

    """Delete the initial skeleton object at index 0"""
    del answer[dealer_key][0]

    """Delete the delearId key value pair from the vehicles list inside the dealers list"""
    for i in range(len(answer[dealer_key])):
        for j in range(len(answer[dealer_key][i][vehicle_key])):
            del answer[dealer_key][i][vehicle_key][j][dealer_id_key]

    answer_url = base_url + '/api/' + \
        dataset_id+'/answer'
    data = json.dumps(answer, indent=2, sort_keys=True)
    headers = {'Content-type': 'application/json'}
    response = requests.post(answer_url, headers=headers, data=data)
    json_data = json.loads(response.text)

    return json.dumps(json_data, indent=2)


"""The final output as required:
You will receive a response structure when you post to the answer
endpoint that describes status and total ellapsed time; 
your program should output this response.
"""
print(post_answer(get_Dealer_Name(dataset_id), Vehicle_Info))
