import requests
import sys
import io
import logging
import json
import re
from tqdm import tqdm

def fetch_job_ids(queryParameters, page):
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

def getAllJobIds():
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
        ids = fetch_job_ids(queryParameters, page)
        if not ids:
            break
        for id in ids:
            # if id not in jobIds:
            jobIds.append(id)
        page += 1
    logging.info(f"total jobIds: {len(jobIds)}")
    jobIds = list(set(jobIds))
    logging.info(f"total jobIds after removing duplicates: {len(jobIds)}")

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
    baseUrl = "https://jobsearch-api-ts.cloud.seek.com.au/v4/counts?"
    url = baseUrl + "&".join(
        [f"{key}={value}" for key, value in queryParameters.items()]
    )
    response = requests.get(url)
    data = response.json()
    __ProcessLocations(data)
    __ProcessClassifications(data)
    __ProcessWorkTypes(data)

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
        url = f"https://www.seek.co.nz/jobs?classification={classificationId}"
        response = requests.get(url, allow_redirects=True)
        redirected_url = response.url

        # this is a main classification
        if url != redirected_url:
            mainClassification = redirected_url.split("/")[-1]
            mainClassifications.append({"id": classificationId, "label": mainClassification})

        # this is a sub classification
        if url == redirected_url:
            url = f"https://www.seek.co.nz/jobs?subclassification={classificationId}"
            response = requests.get(url, allow_redirects=True)
            redirected_url = response.url
            #parse the sub classification label from the redirected url. for example, 'accounts payable' should be extracted from https://www.seek.co.nz/jobs-in-accounting/accounts-payable
            subClassification = redirected_url.split("/")[-1]
            mainClassification = redirected_url.split("/")[-2]
            subClassifications.append({"id": classificationId, "label": subClassification, "mainClassification": mainClassification})
    
    # Link sub classifications to main classifications
    for subClassification in tqdm(subClassifications, desc="Linking sub classifications to main classifications"):
        for mainClassification in mainClassifications:
            if subClassification["mainClassification"] == mainClassification["label"]:
                subClassification["mainClassificationId"] = mainClassification["id"]
                break

    # Save classifications to a file
    with open("temp/classifications.json", "w") as f:
        # main classifications and sub classifications
        json.dump({"mainClassifications": mainClassifications, "subClassifications": subClassifications}, f, indent=4, ensure_ascii=False)

def __ProcessWorkTypes(data):
    pass