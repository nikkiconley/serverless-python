import logging
import json
import requests
import uuid
from datetime import datetime

import azure.functions as func
#from azure.cosmos import exceptions, CosmosClient, PartitionKey


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_api_base = "https://serverlessohuser.trafficmanager.net/api/GetUser"
    product_api_base = "https://serverlessohproduct.trafficmanager.net/api/GetProduct"
    headers = {'Content-Type': 'application/json'}

    inputDict = req.get_json()
    userId = inputDict['userId']
    productId = inputDict['productId']
    rating = inputDict["rating"]

    outputDict = {
        "id": str(uuid.uuid1()),
        "userId": userId,
        "productId": productId,
        "locationName": inputDict["locationName"],
        "rating": rating,
        "userNotes": inputDict["userNotes"],
        "timestamp": str(datetime.now())
    }

    # Validte the userID
    if userId:
        userIdCheck = requests.get(user_api_base+"?userId="+userId, headers=headers)
        if userIdCheck.status_code != 200:
            logging.info('ERROR from getting the user validated.')
            return func.HttpResponse(f'ERROR from getting the user validated error= ' + userIdCheck.status_code)
    else:
        logging.info('NO user id passed into function.')
        return func.HttpResponse(f'NO user id passed into function = ' + json.dumps(inputDict))

    # Validte the productID
    if productId:
        productIdCheck = requests.get(product_api_base+"?productId="+productId, headers=headers)
        if productIdCheck.status_code != 200:
            logging.info('ERROR from getting the product validated.')
            return productIdCheck.status_code
    else:
        logging.info('NO product id passed into function.')
        return func.HttpResponse(f'NO product id passed into function = ' + json.dumps(inputDict))

    # Validte the rating
    if not isinstance(rating, int):
        logging.info('Rating is not an integer.')
        # add error handling
    elif not (0 <= rating <= 5):
        logging.info('Rating must be between 0 and 5.')
        # add error handling

    # Write to the Cosmos DB
    # <create_cosmos_client>
    #client = CosmosClient(endpoint, key)

    return func.HttpResponse(json.dumps(outputDict), status_code=200)
#    return func.HttpResponse(outputDict, status_code=200)
