import requests
import logging
from tqdm import tqdm
import os
import pyodbc

# Entry point for the Azure Function
def ProcessJobsMetaData():
    try:
        queryParameters = {
            "siteKey": "NZ-Main",
            "sourcesystem": "houston",
            "userid": "b75b2db1-191b-4ea3-98f7-f8f488fd6359",
            "usersessionid": "b75b2db1191b-4ea3-98f7-f8f488fd6359",
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
        response.raise_for_status()
        data = response.json()
        __ProcessLocations(data)
        __ProcessClassifications(data)
        __ProcessWorkTypes(data)
    except requests.RequestException as e:
        logging.error(f"Error fetching job metadata: {e}")
        raise e
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise e

def __fetch_job_ids(queryParameters, page):
    try:
        queryParameters["page"] = page
        base_url = "https://www.seek.co.nz/api/chalice-search/v4/search?"
        url = base_url + "&".join(
            [f"{key}={value}" for key, value in queryParameters.items()]
        )
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        ids = []
        if "data" in data:
            ids = [job["id"] for job in data["data"]]
        logging.info(f"page: {page}, ids: {len(ids)}")
        return ids
    except requests.RequestException as e:
        logging.error(f"Error fetching job ids on page {page}: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error on page {page}: {e}")
        return []

def __getAllJobIds():
    try:
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
                jobIds.append(id)
            page += 1
        logging.info(f"total jobIds: {len(jobIds)}")
        jobIds = list(set(jobIds))
        logging.info(f"total jobIds after removing duplicates: {len(jobIds)}")
    except Exception as e:
        logging.error(f"Unexpected error in __getAllJobIds: {e}")

def __ProcessLocations(data):
    pass

def __ProcessClassifications(data):
    try:
        logging.info("Start processing classifications")
        allClassificationIds = __fetch_classification_ids(data)
        updateClassificationsRequired = __check_for_classification_updates(allClassificationIds)
        if not updateClassificationsRequired:
            logging.info("No classification updates detected, skipping classification processing")
            return
        logging.info("Classification updates detected")
        mainClassifications, subClassifications = __classify_classifications(allClassificationIds)
        __update_classifications_in_db(mainClassifications, subClassifications)
        logging.info("End processing classifications")
    except requests.RequestException as e:
        logging.error(f"Error fetching classification data: {e}")
        raise e
    except pyodbc.Error as e:
        logging.error(f"Database error: {e}")
        raise e
    except Exception as e:
        logging.error(f"Unexpected error in __ProcessClassifications: {e}")
        raise e

def __fetch_classification_ids(data):
    logging.info("Fetching classification ids")
    allClassificationIds = []
    for item in data["counts"]:
        if item["name"] == "classification":
            allClassificationIds = list(item["items"])
            break
    return [int(classificationId) for classificationId in allClassificationIds]

def __check_for_classification_updates(allClassificationIds):
    logging.info("Checking for classification updates")
    try:
        connection_string = os.getenv("SeekEnhancementsDatabaseConnectionString")
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute("SELECT mainClassificationId FROM MainClassifications")
        mainClassificationIds = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT subClassificationId FROM SubClassifications")
        subClassificationIds = [row[0] for row in cursor.fetchall()]
        if set(allClassificationIds) == set(mainClassificationIds + subClassificationIds):
            return False
        else:
            newClassificationIds = set(allClassificationIds) - set(mainClassificationIds + subClassificationIds)
            logging.info(f"New classification ids: {newClassificationIds}")
            return True
    except pyodbc.Error as e:
        logging.error(f"Database error checking for classification updates: {e}")
        raise e
    except Exception as e:
        logging.error(f"Error checking for classification updates: {e}")
        raise e
    finally:
        conn.close()

def __classify_classifications(allClassificationIds):
    logging.info("Start classifying classifications into main and sub classifications")
    mainClassifications = []
    subClassifications = []
    for classificationId in tqdm(allClassificationIds, desc="Classifying classifications into main and sub classifications"):
        url = os.getenv("SeekJobsUrl") + f"classification={classificationId}"
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        redirected_url = response.url

        if url != redirected_url:
            mainClassification = redirected_url.split("/")[-1]
            mainClassifications.append({"id": classificationId, "label": mainClassification})
        else:
            url = os.getenv("SeekJobsUrl") + f"subclassification={classificationId}"
            response = requests.get(url, allow_redirects=True)
            response.raise_for_status()
            redirected_url = response.url
            subClassification = redirected_url.split("/")[-1]
            mainClassificationLabel = redirected_url.split("/")[-2]
            subClassifications.append({"id": classificationId, "label": subClassification, "parentClassificationLabel": mainClassificationLabel})

    for subClassification in tqdm(subClassifications, desc="Linking sub classifications to main classifications"):
        for mainClassification in mainClassifications:
            if subClassification["parentClassificationLabel"] == mainClassification["label"]:
                subClassification["parentClassificationid"] = mainClassification["id"]
                break
    logging.info("End classifying classifications into main and sub classifications")
    return mainClassifications, subClassifications

def __update_classifications_in_db(mainClassifications, subClassifications):
    logging.info("Connecting to database")
    
    try:
        connection_string = os.getenv("SeekEnhancementsDatabaseConnectionString")
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        conn.autocommit = False
        logging.info("Updating all classifications")
        cursor.execute("delete from SubClassifications")
        cursor.execute("delete from MainClassifications")

        cursor.execute("SET IDENTITY_INSERT MainClassifications ON")
        for mainClassification in mainClassifications:
            cursor.execute("insert into MainClassifications (mainClassificationId, mainClassificationLabel) values (?, ?)", mainClassification["id"], mainClassification["label"])
        cursor.execute("SET IDENTITY_INSERT MainClassifications OFF")

        cursor.execute("SET IDENTITY_INSERT SubClassifications ON")
        for subClassification in subClassifications:
            cursor.execute("insert into SubClassifications (subClassificationId, subClassificationLabel, parentClassificationId) values (?, ?, ?)", subClassification["id"], subClassification["label"], subClassification["parentClassificationid"])
        cursor.execute("SET IDENTITY_INSERT SubClassifications OFF")
        conn.commit()
        logging.info("All classifications updated")
    except pyodbc.Error as e:
        logging.error(f"Database error updating classifications: {e}")
        conn.rollback()
        raise e
    except Exception as e:
        logging.error(f"Error updating classifications: {e}")
        conn.rollback()
        raise e
    finally:
        conn.autocommit = True
        conn.close()

def __ProcessWorkTypes(data):
    pass