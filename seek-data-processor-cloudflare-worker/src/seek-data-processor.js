/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');
const { Sequelize, DataTypes } = require('sequelize');
const { Advertiser, Classification, Location, WorkType, Job, SubClassification, JobLocation } = require('./models');

const scriptDir = __dirname;
const logFilePath = path.join(scriptDir, 'logging/general.log');
const jobIdsFilePath = path.join(scriptDir, 'output/jobIds.txt');
const jobDetailsFilePath = path.join(scriptDir, 'output/jobDetails.json');

// Configure logging
const logger = require('simple-node-logger').createSimpleLogger(logFilePath);
logger.setLevel('info');

async function fetchJobIds(queryParameters, page) {
    queryParameters.page = page;
    const baseUrl = 'https://www.seek.co.nz/api/jobsearch/v5/search?';
    const url = baseUrl + Object.keys(queryParameters).map(key => `${key}=${queryParameters[key]}`).join('&');
    const response = await axios.get(url);
    const data = response.data;
    const ids = data.data ? data.data.map(job => job.id) : [];
    logger.debug(`page: ${page}, ids: ${ids.length}`);
    return ids;
}

async function getTechJobIds() {
    const jobIds = [];
    const subClassifications = [
        6282, 6283, 6284, 6285, 6286, 6287, 6288, 6289, 6290, 6291, 6292, 6293, 6294, 6295, 6296, 6297, 6298, 6299, 6300, 6301, 6302, 6303
    ];
    const queryParameters = {
        siteKey: 'NZ-Main',
        sourcesystem: 'houston',
        where: 'All New Zealand',
        page: 1,
        pageSize: 100,
        sortmode: 'ListedDate',
        seekSelectAllPages: true,
        hadPremiumListings: true,
        locale: 'en-NZ',
        classification: 6281,
        subclassification: 6282
    };

    for (const subClassification of subClassifications) {
        let subClassificationJobCount = 0;
        queryParameters.subclassification = subClassification;
        let page = 1;
        while (true) {
            const ids = await fetchJobIds(queryParameters, page);
            subClassificationJobCount += ids.length;
            if (ids.length === 0) break;
            jobIds.push(...ids);
            page++;
        }
        logger.info(`subClassification: ${subClassification}, ids: ${subClassificationJobCount}`);
    }
    logger.info(`total jobIds: ${jobIds.length}`);
    const uniqueJobIds = [...new Set(jobIds)];
    logger.info(`total jobIds after removing duplicates: ${uniqueJobIds.length}`);
    fs.writeFileSync(jobIdsFilePath, uniqueJobIds.join('\n'), 'utf-8');
}

async function getJobDetails() {
    const jobDetails = [];
    const connectionString = process.env.SeekDatabaseConnectionString;
    const sequelize = new Sequelize(connectionString);
    const jobIdsInDatabase = await Job.findAll({ attributes: ['job_Id'] }).map(job => job.job_Id);

    const jobIds = fs.readFileSync(jobIdsFilePath, 'utf-8').split('\n').map(Number);
    const newJobIds = jobIds.filter(jobId => !jobIdsInDatabase.includes(jobId));

    for (const jobId of newJobIds) {
        const url = 'https://www.seek.co.nz/graphql';
        const payload = {
            operationName: 'jobDetails',
            variables: {
                jobId,
                jobDetailsViewedCorrelationId: 'd753e3e4-8158-41c3-bab8-ec87f8d77cdb',
                sessionId: 'b75b2db1-191b-4ea3-98f7-f8f488fd6359',
                zone: 'anz-2',
                locale: 'en-NZ',
                languageCode: 'en',
                countryCode: 'NZ',
                timezone: 'Pacific/Auckland'
            },
            query: 'query jobDetails($jobId: ID!, $jobDetailsViewedCorrelationId: String!, $sessionId: String!, $zone: Zone!, $locale: Locale!, $languageCode: LanguageCodeIso!, $countryCode: CountryCodeIso2!, $timezone: Timezone!) { ... }'
        };
        const response = await axios.post(url, payload);
        const data = response.data;
        if (data.data) {
            jobDetails.push(data.data);
        } else {
            logger.info(`jobId: ${jobId} has no job details`);
        }
    }
    fs.writeFileSync(jobDetailsFilePath, JSON.stringify(jobDetails, null, 4), 'utf-8');
    logger.info(`total jobDetails: ${jobDetails.length}`);
}

function getNestedValue(obj, keys, defaultValue = null) {
    return keys.reduce((acc, key) => (acc && acc[key] !== undefined) ? acc[key] : defaultValue, obj);
}

async function insertJobDetailsIntoDatabase() {
    const connectionString = process.env.SeekDatabaseConnectionString;
    const sequelize = new Sequelize(connectionString);
    const jobDetails = JSON.parse(fs.readFileSync(jobDetailsFilePath, 'utf-8'));
    const jobIdsInDatabase = await Job.findAll({ attributes: ['job_Id'] }).map(job => job.job_Id);
    let newJobIds = 0;

    for (const jobDetail of jobDetails) {
        try {
            const job = jobDetail.jobDetails.job;
            const newAdvertiserId = getNestedValue(job, ['advertiser', 'id']);
            if (newAdvertiserId && !await Advertiser.findByPk(newAdvertiserId)) {
                const newAdvertiser = {
                    advertiser_Id: newAdvertiserId,
                    name: getNestedValue(job, ['advertiser', 'name']),
                    is_verified: getNestedValue(job, ['advertiser', 'isVerified']),
                    registration_date: getNestedValue(job, ['advertiser', 'registrationDate', 'dateTimeUtc']) ? new Date(getNestedValue(job, ['advertiser', 'registrationDate', 'dateTimeUtc'])) : null,
                    date_added: new Date()
                };
                await Advertiser.create(newAdvertiser);
            }

            const newClassificationId = getNestedValue(job, ['tracking', 'classificationInfo', 'classificationId']);
            if (newClassificationId && !await Classification.findByPk(newClassificationId)) {
                const newClassification = {
                    classification_Id: newClassificationId,
                    label: getNestedValue(job, ['tracking', 'classificationInfo', 'classification'])
                };
                await Classification.create(newClassification);
            }

            const newSubClassificationId = getNestedValue(job, ['tracking', 'classificationInfo', 'subClassificationId']);
            if (newSubClassificationId && !await SubClassification.findByPk(newSubClassificationId)) {
                const newSubClassification = {
                    subClassification_Id: newSubClassificationId,
                    classification_Id: newClassificationId,
                    label: getNestedValue(job, ['tracking', 'classificationInfo', 'subClassification'])
                };
                await SubClassification.create(newSubClassification);
            }

            const newLocationIds = getNestedValue(job, ['tracking', 'locationInfo', 'locationIds']);
            if (newLocationIds) {
                for (const locationId of newLocationIds) {
                    if (!await Location.findByPk(locationId)) {
                        const newLocation = {
                            location_Id: locationId,
                            area: getNestedValue(job, ['tracking', 'locationInfo', 'area']),
                            location: getNestedValue(job, ['tracking', 'locationInfo', 'location'])
                        };
                        await Location.create(newLocation);
                    }
                }
            }

            const newWorkTypeId = getNestedValue(job, ['tracking', 'workTypeIds']);
            if (newWorkTypeId && !await WorkType.findByPk(newWorkTypeId)) {
                const newWorkType = {
                    work_type_Id: newWorkTypeId,
                    label: getNestedValue(job, ['workTypes', 'label'])
                };
                await WorkType.create(newWorkType);
            }

            const newJobId = job.id;
            if (newJobId && !jobIdsInDatabase.includes(newJobId)) {
                const newJob = {
                    job_Id: newJobId,
                    advertiser_Id: newAdvertiserId,
                    classification_Id: newClassificationId,
                    subClassification_Id: newSubClassificationId,
                    work_type_Id: newWorkTypeId,
                    title: job.title,
                    phone_number: job.phoneNumber,
                    is_expired: job.isExpired,
                    expires_at: job.expiresAt ? new Date(job.expiresAt.dateTimeUtc) : null,
                    is_link_out: job.isLinkOut,
                    is_verified: job.isVerified,
                    abstract: job.abstract,
                    content: job.content,
                    status: job.status,
                    listed_at: job.listedAt ? new Date(job.listedAt.dateTimeUtc) : null,
                    salary: getNestedValue(job, ['salary', 'label']),
                    share_link: job.shareLink,
                    date_added: new Date(),
                    bullets: JSON.stringify(getNestedValue(job, ['products', 'bullets'])),
                    questions: JSON.stringify(getNestedValue(job, ['products', 'questionnaire', 'questions']))
                };
                await Job.create(newJob);
                newJobIds++;
            }

            if (newLocationIds && newJobId) {
                for (const locationId of newLocationIds) {
                    const newJobLocation = {
                        job_Id: newJobId,
                        location_Id: locationId
                    };
                    await JobLocation.create(newJobLocation);
                }
            }
        } catch (error) {
            logger.error(`Error inserting job: ${jobDetail.jobDetails.job.id}, ${error}`);
        }
    }
    logger.info(`total new jobIds added: ${newJobIds}`);
}

(async () => {
    fs.writeFileSync(logFilePath, '');
    await getTechJobIds();
    await getJobDetails();
    await insertJobDetailsIntoDatabase();
})();