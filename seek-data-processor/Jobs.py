import requests
import sys
import io
import logging
import json
import re
from tqdm import tqdm
import os
import pyodbc


def ProcessJobsMetaData():
    # get all metadata: locations, classifications, work types
    queryParameters = {
        "siteKey": "NZ-Main",
        "sourcesystem": "houston",
        "userid": "b75b2db1-191b-4ea3-98f7-f8f488fd6359",
        "usersessionid": "b75b2db1-191b-4ea3-98f7-f8f488fd6359",
        "eventCaptureSessionId": "b75b2db1-191b-4ea3-98f7-f8f488fd6359",
        "where": "All New Zealand",
        "page": 1,
        "seekSelectAllPages": True,
        "include": "seodata",
        "locale": "en-NZ",
    }
    baseUrl = os.getenv("SeekJobMetaDataUrl")
    url = baseUrl + "&".join(
        [f"{key}={value}" for key, value in queryParameters.items()]
    )
    response = requests.get(url)
    data = response.json()
    __ProcessLocations(data)
    __ProcessClassifications(data)
    __ProcessWorkTypes(data)

def __fetch_job_ids(queryParameters, page):
    queryParameters["page"] = page
    base_url = "https://www.seek.co.nz/api/chalice-search/v4/search?"
    url = base_url + "&".join(
        [f"{key}={value}" for key, value in queryParameters.items()]
    )
    response = requests.get(url)
    data = response.json()
    ids = []
    if "data" in data:
        ids = [job["id"] for job in data["data"]]
    logging.info(f"page: {page}, ids: {len(ids)}")
    return ids

def __getAllJobIds():
    queryParameters = {
        "siteKey": "NZ-Main",
        "sourcesystem": "houston",
        "userqueryid": "e3b7d0ab254c4a7908be32accaaf1059-1173995",
        "userid": "b75b2db1-191b-4ea3-98f7-f8f488fd6359",
        "usersessionid": "b75b2db1-191b-4ea3-98f7-f8f488fd6359",
        "eventCaptureSessionId": "b75b2db1-191b-4ea3-98f7-f8f488fd6359",
        "where": "All New Zealand",
        "page": 1,
        "seekSelectAllPages": True,
        "hadPremiumListings": True,
        "pageSize": 100,
        "include": "seodata",
        "locale": "en-NZ",
        "seekerId": "27376419",
        "solId": "c36c28b4-1546-4592-a67e-36a9c420f87d",
    }

    jobIds = []
    page = 1
    while True:
        ids = __fetch_job_ids(queryParameters, page)
        if not ids:
            break
        for id in ids:
            # if id not in jobIds:
            jobIds.append(id)
        page += 1
    logging.info(f"total jobIds: {len(jobIds)}")
    jobIds = list(set(jobIds))
    logging.info(f"total jobIds after removing duplicates: {len(jobIds)}")

def __ProcessLocations(data):
    pass

def __ProcessClassifications(data):
    logging.info("Processing classifications")
    allClassificationIds = []
    mainClassifications = []
    subClassifications = []
    for item in data["counts"]:
        if item["name"] == "classification":
            allClassificationIds = list(item["items"])
            break
    for classificationId in tqdm(allClassificationIds[0:20], desc="Classifying classifications into main and sub classifications"):
        url = os.getenv("SeekJobsUrl") + f"classification={classificationId}"
        response = requests.get(url, allow_redirects=True)
        redirected_url = response.url

        # this is a main classification
        if url != redirected_url:
            mainClassification = redirected_url.split("/")[-1]
            mainClassifications.append({"id": classificationId, "label": mainClassification})

        # this is a sub classification
        if url == redirected_url:
            url = os.getenv("SeekJobsUrl") + f"subclassification={classificationId}"
            response = requests.get(url, allow_redirects=True)
            redirected_url = response.url
            #parse the sub classification label from the redirected url. for example, 'accounts payable' should be extracted from https://www.seek.co.nz/jobs-in-accounting/accounts-payable
            subClassification = redirected_url.split("/")[-1]
            mainClassificationLabel = redirected_url.split("/")[-2]
            subClassifications.append({"id": classificationId, "label": subClassification, "parentClassificationLabel": mainClassificationLabel})
    
    # Link sub classifications to main classifications
    for subClassification in tqdm(subClassifications, desc="Linking sub classifications to main classifications"):
        for mainClassification in mainClassifications:
            if subClassification["parentClassificationLabel"] == mainClassification["label"]:
                subClassification["parentClassificationid"] = mainClassification["id"]
                break

    # Retrieve existing data from the database
    def get_existing_data(cursor, table_name):
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Compare existing data with new data
    def data_is_different(existing_data, new_data):
        return existing_data != new_data

    # Save classifications to a file
    with open("temp/classifications.json", "w") as f:
        json.dump({"mainClassifications": mainClassifications, "subClassifications": subClassifications}, f, indent=4, ensure_ascii=False)

    # Database connection
    connection_string = os.getenv("SeekEnhancementsDatabaseConnectionString")
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Retrieve existing main classifications
    existing_main_classifications = get_existing_data(cursor, "MainClassifications")

    # Retrieve existing sub classifications
    existing_sub_classifications = get_existing_data(cursor, "SubClassifications")

    # Check if main classifications data is different
    main_classifications_different = data_is_different(existing_main_classifications, mainClassifications)

    # Check if sub classifications data is different
    sub_classifications_different = data_is_different(existing_sub_classifications, subClassifications)

    # Use a transaction to ensure atomicity
    conn.autocommit = False
    try:
        if sub_classifications_different or main_classifications_different:
            logging.info("Updating all classifications")
            cursor.execute("delete from SubClassifications")
            cursor.execute("delete from MainClassifications")

            cursor.execute("SET IDENTITY_INSERT MainClassifications ON")
            for mainClassification in mainClassifications:
                cursor.execute("insert into MainClassifications (main_classification_id, label) values (?, ?)", mainClassification["id"], mainClassification["label"])
            cursor.execute("SET IDENTITY_INSERT MainClassifications OFF")

            cursor.execute("SET IDENTITY_INSERT SubClassifications ON")
            for subClassification in subClassifications:
                cursor.execute("insert into SubClassifications (SubClassification_id, parentClassification_id, label) values (?, ?, ?)", subClassification["id"], subClassification["parentClassificationid"], subClassification["label"])
            cursor.execute("SET IDENTITY_INSERT SubClassifications OFF")

        else:
            logging.info("No changes detected")
        conn.commit()
    except Exception as e:
        logging.error(e)
        conn.rollback()
        raise e
    finally:
        conn.autocommit = True
        conn.close()

def __ProcessWorkTypes(data):
    pass