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
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Advertiser, Classification, Location, WorkType, Job, SubClassification, JobLocation

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
load_dotenv()

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
    jobIds = []
    # Need to get all job ids by looping through all sub classifications. If using only the main classification id, some jobs will be missed. This is because the API stops returning data after a certain number of pages, despite there being more pages of data. This is also true for the Seek website itself.
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
        "where": "All New Zealand",
        "page": 1,
        "pageSize": 100,
        "sortmode": "ListedDate",
        "seekSelectAllPages": True,
        "hadPremiumListings": True,
        "locale": "en-NZ",
        "classification": 6281,
        "subclassification": 6282,
    }

    

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

def getJobDetails():
    jobDetails = []
    connection_string = os.getenv("SeekDatabaseConnectionString")
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    # get job ids already in the database
    jobIdsInDatabase = [job.job_Id for job in session.query(Job).all()]


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
        #insert if job details are not null
        if data["data"] != None:
            jobDetails.append(data["data"])
        else:
            logger.info(f"jobId: {jobId} has no job details")
    with open("output/jobDetails.json", "w", encoding="utf-8") as f:
        json.dump(jobDetails, f, indent=4, ensure_ascii=False)
    logger.info(f"total jobDetails: {len(jobDetails)}")

def get_nested_value(d, keys, default=None):
    for key in keys:
        d = d.get(key, default)
        if d is default:
            break
    return d

def insertJobDetailsIntoDatabase():
    connection_string = os.getenv("SeekDatabaseConnectionString")
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    with open("output/jobDetails.json", "r", encoding="utf-8") as f:
        jobDetails = json.load(f)

    #get all job ids already in the database
    jobIdsInDatabase = [job.job_Id for job in session.query(Job).all()]

    # Insert data into database
    for job in tqdm(jobDetails, desc="Inserting job details into database"):
        try:
            if job["jobDetails"]== None:
                continue
            job = job["jobDetails"]["job"]

            
            try:
                # insert into Advertisers table if the advertiser id does not exist
                new_advertiser_id = job.get("advertiser", {}).get("id")
                if new_advertiser_id is not None:
                    if new_advertiser_id == "Private Advertiser":
                        new_advertiser_id = 1
                    existing_advertiser_id = session.query(Advertiser).filter(Advertiser.advertiser_Id == new_advertiser_id).first()
                    if existing_advertiser_id == None:
                        new_advertiser_name = get_nested_value(job, ["advertiser", "name"])
                        new_advertiser_is_verified = get_nested_value(job, ["advertiser", "isVerified"])
                        new_advertiser_registration_date = get_nested_value(job, ["advertiser", "registrationDate", "dateTimeUtc"])
                        if new_advertiser_registration_date is not None:
                            new_advertiser_registration_date = datetime.datetime.strptime(new_advertiser_registration_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                        #log the new advertiser details
                        new_advertiser = Advertiser(
                            advertiser_Id=new_advertiser_id,
                            name=new_advertiser_name,
                            is_verified=new_advertiser_is_verified,
                            registration_date=new_advertiser_registration_date,
                            date_added=datetime.datetime.now()
                        )
                        session.add(new_advertiser)
            except Exception as e:
                logger.error(f"Error inserting advertiser: {new_advertiser_id}, {e}")
                session.rollback()
                continue

            try:
                # insert into Classifications table if the classification id does not exist
                # check if classification id is not null
                new_classification_id = get_nested_value(job, ["tracking", "classificationInfo", "classificationId"])
                if new_classification_id is not None:
                    existing_classification_id = session.query(Classification).filter(Classification.classification_Id == new_classification_id).first()
                    if existing_classification_id == None:
                        new_classification_label = get_nested_value(job, ["tracking", "classificationInfo", "classification"])
                        new_classification = Classification(
                            classification_Id=new_classification_id,
                            label=new_classification_label
                        )
                        session.add(new_classification)
                        session.commit()
            except Exception as e:
                logger.error(f"Error inserting classification: {new_classification_id}, {e}")
                session.rollback()
                continue
            
            try:
                # insert into SubClassifications table if the sub classification id does not exist
                new_sub_classification_id = get_nested_value(job, ["tracking", "classificationInfo", "subClassificationId"])
                if new_sub_classification_id is not None:
                    existing_sub_classification_id = session.query(SubClassification).filter(SubClassification.subClassification_Id == new_sub_classification_id).first()
                    if existing_sub_classification_id == None:
                        new_classification_id = get_nested_value(job, ["tracking", "classificationInfo", "classificationId"])
                        new_sub_classification_label = get_nested_value(job, ["tracking", "classificationInfo", "subClassification"])
                        new_sub_classification = SubClassification(
                            subClassification_Id=new_sub_classification_id,
                            classification_Id=new_classification_id,
                            label=new_sub_classification_label
                        )
                        session.add(new_sub_classification)
                        session.commit()
            except Exception as e:
                logger.error(f"Error inserting sub classification: {new_sub_classification_id}, {e}")
                session.rollback()
                continue
            
            try:
                # insert into locations table if the location id does not exist
                new_location_ids = get_nested_value(job, ["tracking", "locationInfo", "locationIds"])
                if new_location_ids is not None:
                    for location_id in new_location_ids:
                        existing_location_id = session.query(Location).filter(Location.location_Id == location_id).first()
                        if existing_location_id == None:
                            new_location_area = get_nested_value(job, ["tracking", "locationInfo", "area"])
                            new_location_location = get_nested_value(job, ["tracking", "locationInfo", "location"])
                            new_location = Location(
                                location_Id=location_id,
                                area=new_location_area,
                                location=new_location_location
                            )
                            session.add(new_location)
                            session.commit()
            except Exception as e:
                logger.error(f"Error inserting location: {location_id}, {e}")
                session.rollback()
                continue
            
            try:
                # insert into WorkTypes table if the work type id does not exist
                new_work_type_id = get_nested_value(job, ["tracking", "workTypeIds"])
                if new_work_type_id is not None:
                    existing_work_type_id = session.query(WorkType).filter(WorkType.work_type_Id == new_work_type_id).first()
                    if existing_work_type_id == None:
                        new_work_type_label = get_nested_value(job, ["workTypes", "label"])
                        new_work_type = WorkType(
                            work_type_Id=new_work_type_id,
                            label=new_work_type_label
                        )
                        session.add(new_work_type)
                        session.commit()
            except Exception as e:
                logger.error(f"Error inserting work type: {new_work_type_id}, {e}")
                session.rollback()
                continue

            try:
                # if job id already exists in the database, skip
                new_job_id = job.get("id")
                if new_job_id is not None:
                    if int(job["id"]) in jobIdsInDatabase:
                        continue
                    # insert into Jobs table
                    new_advertiser_id = get_nested_value(job, ["advertiser", "id"])
                    if new_advertiser_id == "Private Advertiser":
                        new_advertiser_id = 1
                    new_classification_id = get_nested_value(job, ["tracking", "classificationInfo", "classificationId"])
                    new_sub_classification_id = get_nested_value(job, ["tracking", "classificationInfo", "subClassificationId"])
                    new_work_type_id = get_nested_value(job, ["tracking", "workTypeIds"])
                    new_title = job.get("title")
                    new_phone_number = job.get("phoneNumber")
                    new_is_expired = job.get("isExpired")
                    new_expires_at = job.get("expiresAt")
                    if new_expires_at is not None:
                        new_expires_at = datetime.datetime.strptime(job["expiresAt"]["dateTimeUtc"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    new_is_link_out = job.get("isLinkOut")
                    new_is_verified = job.get("isVerified")
                    new_abstract = job.get("abstract")
                    new_content = job.get("content")
                    new_status = job.get("status")
                    new_listed_at = job.get("listedAt")
                    if new_listed_at is not None:
                        new_listed_at = datetime.datetime.strptime(job["listedAt"]["dateTimeUtc"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    new_salary = get_nested_value(job, ["salary", "label"])
                    new_share_link = job.get("shareLink")
                    new_date_added = datetime.datetime.now()
                    new_bullets = get_nested_value(job, ["products", "bullets"])
                    if new_bullets is not None:
                        new_bullets = json.dumps(new_bullets)
                    new_questions = get_nested_value(job, ["products", "questionnaire", "questions"])
                    if new_questions is not None:
                        new_questions = json.dumps(new_questions)
                    newJob = Job(
                        job_Id=new_job_id,
                        advertiser_Id=new_advertiser_id,
                        classification_Id=new_classification_id,
                        subClassification_Id=new_sub_classification_id,
                        work_type_Id=new_work_type_id,
                        title=new_title,
                        phone_number=new_phone_number,
                        is_expired=new_is_expired,
                        expires_at=new_expires_at,
                        is_link_out=new_is_link_out,
                        is_verified=new_is_verified,
                        abstract=new_abstract,
                        content=new_content,
                        status=new_status,
                        listed_at=new_listed_at,
                        salary=new_salary,
                        share_link=new_share_link,
                        date_added=new_date_added,
                        bullets=new_bullets,
                        questions=new_questions
                    )
                    session.add(newJob)
                    session.commit()
            except Exception as e:
                logger.error(f"Error inserting job: {new_job_id}, {e}")
                session.rollback()
                continue
            
            try:
                # insert into JobLocations table
                new_location_ids = job.get("location", {}).get("locationIds")
                new_job_id = job.get("id")
                if new_location_ids and new_job_id is not None:
                    for location_id in new_location_ids:
                        logger.info(f"new job location: {new_job_id}, {location_id}")
                        new_job_location = JobLocation(
                            job_id=new_job_id,
                            location_id=location_id
                        )
                        session.add(new_job_location)
                        session.commit()
            except Exception as e:
                logger.error(f"Error inserting job location: {new_job_id}, {location_id}, {e}")
                session.rollback()
                continue


        except Exception as e:
            logger.error(f"Error inserting job: {job['id']}, {e}")
            session.rollback()

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
    
    previousJobId = 0
    for job in jobDetails:
        if job["jobDetails"]== None:
            logger.info(f"previousJobId: {previousJobId}")
            break
        previousJobId = job["jobDetails"]["job"]["id"]

if __name__ == "__main__":
    open("logging/general.log", "w").close()
    getTechJobIds()
    #getAllJobIds()
    getJobDetails()
    insertJobDetailsIntoDatabase()
    #queryJobs()
    #classifiyClassifications()
    #sandpit()