import requests
import sys
import io
import logging
import json
import re
from tqdm import tqdm
import pyodbc
import os
import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logging/general.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

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
    logger.debug(f"page: {page}, ids: {len(ids)}")
    return ids

def getTechJobIds():
    open("logging/jobIds.log", "w").close()
    subClassifications = {
        6282,  # Architects
        6283,  # Business/Systems Analysts
        6284,  # Computer Operators
        6285,  # Consultants
        6286,  # Database Development & Administration
        6287,  # Developers/Programmers
        6288,  # Engineering - Hardware
        6289,  # Engineering - Network
        6290,  # Engineering - Software
        6291,  # Help Desk & IT Support
        6292,  # Management
        6293,  # Networks & Systems Administration
        6294,  # Product Management & Development
        6295,  # Programme & Project Management
        6296,  # Sales - Pre & Post
        6297,  # Security
        6298,  # Team Leaders
        6299,  # Technical Writing
        6300,  # Telecommunications
        6301,  # Testing & Quality Assurance
        6302,  # Web Development & Production
        6303,  # Other
    }
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
        "classification": 6281,
        "subclassification": 6282,
        "worktype": 242,
        "pageSize": 20,
        "include": "seodata",
        "locale": "en-NZ",
        "seekerId": "27376419",
        "solId": "c36c28b4-1546-4592-a67e-36a9c420f87d",
    }

    jobIds = []

    for subClassification in subClassifications:
        subClassificationJobCount = 0
        queryParameters["subclassification"] = subClassification
        page = 1
        while True:
            ids = fetch_job_ids(queryParameters, page)
            subClassificationJobCount += len(ids)
            if not ids:
                break
            for id in ids:
                # if id not in jobIds:
                jobIds.append(id)

            page += 1
        logger.info(
            f"subClassification: {subClassification}, ids: {subClassificationJobCount}"
        )
    logger.info(f"total jobIds: {len(jobIds)}")
    jobIds = list(set(jobIds))
    logger.info(f"total jobIds after removing duplicates: {len(jobIds)}")
    with open("output/jobIds.txt", "w", encoding="utf-8") as f:
        for jobId in jobIds:
            f.write(str(jobId) + "\n")

def getAllJobIds():
    connection_string = os.getenv("SeekEnhancementsDatabaseConnectionString")
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT mainClassificationId FROM MainClassifications")
    mainClassificationIds = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT subClassificationId FROM SubClassifications")
    subClassificationIds = [row[0] for row in cursor.fetchall()]

    conn.autocommit = False
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
        "classification": 6281,
        #"worktype": 242,
        "pageSize": 100,
        "include": "seodata",
        "locale": "en-NZ",
        "seekerId": "27376419",
        "solId": "c36c28b4-1546-4592-a67e-36a9c420f87d",
    }

    jobIds = []

    for mainClassificationId in mainClassificationIds:
        queryParameters["classification"] = mainClassificationId
        logger.info(f"mainClassificationId: {mainClassificationId}")
        page = 1
        while True:
            logger.info(f"page: {page}")
            ids = fetch_job_ids(queryParameters, page)
            if not ids:
                break
            for id in ids:
                if id not in jobIds:
                    jobIds.append(id)
            page += 1
    logger.info(f"total jobIds: {len(jobIds)}")
    with open("output/jobIds.txt", "w", encoding="utf-8") as f:
        for jobId in jobIds:
            f.write(str(jobId) + "\n")
    conn.close()

def getJobDetails():
    connection_string = os.getenv("SeekEnhancementsDatabaseConnectionString")
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # get job ids already in the database
    cursor.execute("SELECT job_id FROM Jobs")
    jobIdsInDatabase = [row[0] for row in cursor.fetchall()]

    jobDetails = []
    with open("output/jobIds.txt", "r", encoding="utf-8") as f:
        jobIds = [int(line.strip()) for line in f]

    # remove job ids already in the database from the jobIds list
    jobIds = list(set(jobIds) - set(jobIdsInDatabase))
  
    for jobId in tqdm(jobIds, desc="Getting job details from Seek"):
        url = "https://www.seek.co.nz/graphql"
        payload = {
            "operationName": "jobDetails",
            "variables": {
                "jobId": jobId,
                "jobDetailsViewedCorrelationId": "d753e3e4-8158-41c3-bab8-ec87f8d77cdb",
                "sessionId": "b75b2db1-191b-4ea3-98f7-f8f488fd6359",
                "zone": "anz-2",
                "locale": "en-NZ",
                "languageCode": "en",
                "countryCode": "NZ",
                "timezone": "Pacific/Auckland",
            },
            "query": 'query jobDetails($jobId: ID!, $jobDetailsViewedCorrelationId: String!, $sessionId: String!, $zone: Zone!, $locale: Locale!, $languageCode: LanguageCodeIso!, $countryCode: CountryCodeIso2!, $timezone: Timezone!) {\n  jobDetails(\n    id: $jobId\n    tracking: {channel: "WEB", jobDetailsViewedCorrelationId: $jobDetailsViewedCorrelationId, sessionId: $sessionId}\n  ) {\n    job {\n      sourceZone\n      tracking {\n        adProductType\n        classificationInfo {\n          classificationId\n          classification\n          subClassificationId\n          subClassification\n          __typename\n        }\n        hasRoleRequirements\n        isPrivateAdvertiser\n        locationInfo {\n          area\n          location\n          locationIds\n          __typename\n        }\n        workTypeIds\n        postedTime\n        __typename\n      }\n      id\n      title\n      phoneNumber\n      isExpired\n      expiresAt {\n        dateTimeUtc\n        __typename\n      }\n      isLinkOut\n      contactMatches {\n        type\n        value\n        __typename\n      }\n      isVerified\n      abstract\n      content(platform: WEB)\n      status\n      listedAt {\n        label(context: JOB_POSTED, length: SHORT, timezone: $timezone, locale: $locale)\n        dateTimeUtc\n        __typename\n      }\n      salary {\n        currencyLabel(zone: $zone)\n        label\n        __typename\n      }\n      shareLink(platform: WEB, zone: $zone, locale: $locale)\n      workTypes {\n        label(locale: $locale)\n        __typename\n      }\n      advertiser {\n        id\n        name(locale: $locale)\n        isVerified\n        registrationDate {\n          dateTimeUtc\n          __typename\n        }\n        __typename\n      }\n      location {\n        label(locale: $locale, type: LONG)\n        __typename\n      }\n      classifications {\n        label(languageCode: $languageCode)\n        __typename\n      }\n      products {\n        branding {\n          id\n          cover {\n            url\n            __typename\n          }\n          thumbnailCover: cover(isThumbnail: true) {\n            url\n            __typename\n          }\n          logo {\n            url\n            __typename\n          }\n          __typename\n        }\n        bullets\n        questionnaire {\n          questions\n          __typename\n        }\n        video {\n          url\n          position\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    companyProfile(zone: $zone) {\n      id\n      name\n      companyNameSlug\n      shouldDisplayReviews\n      branding {\n        logo\n        __typename\n      }\n      overview {\n        description {\n          paragraphs\n          __typename\n        }\n        industry\n        size {\n          description\n          __typename\n        }\n        website {\n          url\n          __typename\n        }\n        __typename\n      }\n      reviewsSummary {\n        overallRating {\n          numberOfReviews {\n            value\n            __typename\n          }\n          value\n          __typename\n        }\n        __typename\n      }\n      perksAndBenefits {\n        title\n        __typename\n      }\n      __typename\n    }\n    companySearchUrl(zone: $zone, languageCode: $languageCode)\n    learningInsights(platform: WEB, zone: $zone, locale: $locale) {\n      analytics\n      content\n      __typename\n    }\n    companyTags {\n      key(languageCode: $languageCode)\n      value\n      __typename\n    }\n    restrictedApplication(countryCode: $countryCode) {\n      label(locale: $locale)\n      __typename\n    }\n    sourcr {\n      image\n      imageMobile\n      link\n      __typename\n    }\n    gfjInfo {\n      location {\n        countryCode\n        country(locale: $locale)\n        suburb(locale: $locale)\n        region(locale: $locale)\n        state(locale: $locale)\n        postcode\n        __typename\n      }\n      workTypes {\n        label\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',
        }
        response = requests.post(url, json=payload)
        data = response.json()
        jobDetails.append(data["data"])
    with open("output/jobDetails.json", "w", encoding="utf-8") as f:
        json.dump(jobDetails, f, indent=4, ensure_ascii=False)
    logger.info(f"total jobDetails: {len(jobDetails)}")
    conn.close()


def insertJobDetailsIntoDatabase():
    connection_string = os.getenv("SeekEnhancementsDatabaseConnectionString")
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    with open("output/jobDetails.json", "r", encoding="utf-8") as f:
        jobDetails = json.load(f)

    #get all job ids already in the database
    cursor.execute("SELECT job_id FROM Jobs")
    jobIdsInDatabase = [row[0] for row in cursor.fetchall()]

    # Insert data into database
    for job in tqdm(jobDetails, desc="Inserting job details into database"):
        try:
            if job["jobDetails"]== None:
                continue
            job = job["jobDetails"]["job"]

            # if job id already exists in the database, skip
            if job["id"] in jobIdsInDatabase:
                continue

            # insert into Advertisers table if the advertiser id does not exist
            # if advertiser["id"] is not an integer, then it is a private advertiser - use id 1 for private advertisers
            if not isinstance(job["advertiser"]["id"], int):
                job["advertiser"]["id"] = 1
            cursor.execute("SELECT COUNT(*) FROM Advertisers WHERE advertiser_id = ?", (job["advertiser"]["id"],))
            if cursor.fetchone()[0] == 0:
                cursor.execute("SET IDENTITY_INSERT Advertisers ON")
                cursor.execute(
                    "INSERT INTO Advertisers (advertiser_id, name, is_verified, registration_date, date_added) VALUES (?,?,?,?,?)",
                    (
                        job["advertiser"]["id"],
                        job["advertiser"]["name"],
                        job["advertiser"]["isVerified"],
                        job["advertiser"]["registrationDate"]["dateTimeUtc"],
                        datetime.datetime.now()
                    ),
                )
                cursor.execute("SET IDENTITY_INSERT Advertisers OFF") 

            # insert into Jobs table
            cursor.execute("SET IDENTITY_INSERT Jobs ON")
            cursor.execute(
                "INSERT INTO Jobs (job_id, advertiser_id, subclassification_id, work_type_id, title, abstract, [content], phone_number, location, is_expired, expires_at, is_link_out, is_verified, status, listed_at, salary, share_link, date_added) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    job["id"],
                    job["advertiser"]["id"],
                    job["tracking"]["classificationInfo"]["subClassificationId"],
                    job["tracking"]["workTypeIds"],
                    job["title"],
                    job["abstract"],
                    job["content"],
                    job["phoneNumber"],
                    job["location"]["label"],
                    job["isExpired"],
                    job["expiresAt"]["dateTimeUtc"],
                    job["isLinkOut"],
                    job["isVerified"],
                    job["status"],
                    job["listedAt"]["dateTimeUtc"],
                    job["salary"]["label"] if job.get("salary") and job["salary"].get("label") else None,
                    job["shareLink"],
                    datetime.datetime.now()
                ),
            )
            cursor.execute("SET IDENTITY_INSERT Jobs OFF")
        except Exception as e:
            logger.error(f"Error inserting job: {job['id']}, {e}")
            continue
    
    conn.commit()
    conn.close()

def queryJobs():
    remoteKeywords = [
        "remote",
        "work from home",
        "telecommute",
        "telework",
        "anywhere",
        "home based",
        "home office",
        "home-based",
        "wfh",
        "flexible",
        "home",
    ]
    entryLevelKeywords = [
        "junior",
        "graduate",
        "entry level",
        "intern",
        "internship",
        "trainee",
        "apprentice",
        "apprenticeship",
        "student",
        "starter",
        "beginner",
        "student",
        "assistant",
        "trainee",
        "intern",
        "entry",
        "newcomer",
        "beginner",
        "starter",
    ]
    titleKeywords = [
        "engineer"
    ]
    ignore = "senior"
    foundJobs = []
    with open("output/jobDetails.json", "r", encoding="utf-8") as f:
        jobs = json.load(f)
    for job in jobs:
        jobContent = job["jobDetails"]["job"]["content"].lower()
        jobTitle = job["jobDetails"]["job"]["title"].lower()
        if (
            any(re.search(r'\b' + re.escape(keyword) + r'\b', jobContent) for keyword in remoteKeywords) and \
            any(re.search(r'\b' + re.escape(keyword) + r'\b', jobContent) for keyword in entryLevelKeywords)
            #and any(keyword in jobTitle for keyword in titleKeywords)
            and ignore not in jobTitle
        ):
            # add the remoteKeywords that are found in the jobContent to the job
            job["remoteKeywords"] = [
                keyword for keyword in remoteKeywords if keyword in jobContent
            ]
            job["entryLevelKeywords"] = [
                keyword for keyword in entryLevelKeywords if keyword in jobContent
            ]
            foundJobs.append(job)
    # sort jobs by date
    foundJobs = sorted(
        foundJobs,
        key=lambda job: job["jobDetails"]["job"]["listedAt"]["dateTimeUtc"],
        reverse=True,
    )
    with open("output/foundJobs.json", "w", encoding="utf-8") as f:
        foundJobsOutput = []
        for job in foundJobs:
            foundJobsOutput.append(
                {
                    "jobId": job["jobDetails"]["job"]["id"],
                    "title": job["jobDetails"]["job"]["title"],
                    "location": job["jobDetails"]["job"]["tracking"]["locationInfo"][
                        "location"
                    ],
                    "advertiser": job["jobDetails"]["job"]["advertiser"]["name"],
                    "listedAt": job["jobDetails"]["job"]["listedAt"]["dateTimeUtc"],
                    "remoteKeywords": job["remoteKeywords"],
                    "entryLevelKeywords": job["entryLevelKeywords"],
                    "url": "https://www.seek.co.nz/job/"+str(job["jobDetails"]["job"]["id"]),
                }
            )
        json.dump(foundJobsOutput, f, indent=4, ensure_ascii=False)
    print(f"foundJobs: {len(foundJobs)}")


def classifiyClassifications():
    # get all classifications
    url = "https://jobsearch-api-ts.cloud.seek.com.au/v4/counts?siteKey=NZ-Main&sourcesystem=houston&userid=b75b2db1-191b-4ea3-98f7-f8f488fd6359&usersessionid=b75b2db1-191b-4ea3-98f7-f8f488fd6359&eventCaptureSessionId=b75b2db1-191b-4ea3-98f7-f8f488fd6359&where=All+New+Zealand&page=1&seekSelectAllPages=true&include=seodata&locale=en-NZ"
    response = requests.get(url)
    data = response.json()
    allClassificationIds = []
    mainClassifications = []
    subClassifications = []
    for item in data["counts"]:
        if item["name"] == "classification":
            allClassificationIds = list(item["items"])
            break
    for classificationId in tqdm(allClassificationIds, desc="Classifying classifications into main and sub classifications"):
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
    
    for subClassification in tqdm(subClassifications, desc="Linking sub classifications to main classifications"):
        for mainClassification in mainClassifications:
            if subClassification["mainClassification"] == mainClassification["label"]:
                subClassification["mainClassificationId"] = mainClassification["id"]
                break

    with open("output/classifications.json", "w", encoding="utf-8") as f:
        json.dump({"mainClassifications": mainClassifications, "subClassifications": subClassifications}, f, indent=4, ensure_ascii=False)


    # Iterate through all the classification IDs using url https://www.seek.co.nz/jobs?classification=[classification_id]
    # If the redirect url is different from the original url, then the classification id is a main classification and the main classification label can be extracted from the redirected url.
    # If the redirect url is the same as the original url, then the classification id is a sub classification.
    # Make a list of all main and sub classifications and their labels.

def sandpit():
    with open("output/jobDetails.json", "r", encoding="utf-8") as f:
        jobDetails = json.load(f)
    
    for job in jobDetails:
        if job["jobDetails"]== None:
            logger.info(f"job: {job}")
            break
if __name__ == "__main__":
    open("logging/general.log", "w").close()
    #getTechJobIds()
    #getAllJobIds()
    #getJobDetails()
    insertJobDetailsIntoDatabase()
    #queryJobs()
    #classifiyClassifications()
    #sandpit()