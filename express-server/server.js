const express = require('express');
const { Sequelize } = require('sequelize');
const initModels = require('./models/init-models');
const { Where } = require('sequelize/lib/utils');
const app = express();
const port = 3002;
const database = process.env.DB_NAME;
const username = process.env.DB_USER;
const password = process.env.DB_PASSWORD;
const host = process.env.DB_HOST;
const databasePort = process.env.DB_PORT;


// Initialize Sequelize
const sequelize = new Sequelize(database, username, password, {
  host: host,
  port: databasePort,
  dialect: 'mysql',
  logging: false
});

sequelize.authenticate()
.then(() => {
  console.log('Connection has been established successfully.');
})
.catch(err => {
  console.error('Unable to connect to the database:', err);
});

// Initialize models
const models = initModels(sequelize);
const { Job, JobLocation, Location, SubClassification, WorkType } = models;

// create an endpoint to get all jobs. use page and limit query parameters to paginate the results
app.get('/api/jobs', async (req, res) => {
  try {
    const page = parseInt(req.query.page, 10) || 1;
    const limit = parseInt(req.query.limit, 10) || 10;
    const expired = req.query.expired === 'false' ? false : true;
    const offset = (page - 1) * limit;

    const jobs = await Job.findAll({ 
        offset, 
        limit,
        where: {
          is_expired: expired
        }
      });
    const totalJobs = await Job.count();

    // Transform the fields
    const transformedJobs = jobs.map(job => ({
      ...job.toJSON(),
      jobId: job.job_Id,
      advertiserId: job.advertiser_Id,
      classificationId: job.classification_Id,
      subClassificationId: job.subClassification_Id,
      workTypeId: job.work_type_Id,
      phoneNumber: job.phone_number,
      isExpired: job.is_expired,
      expiresAt: job.expires_at,
      isLinkOut: job.is_link_out,
      isVerified: job.is_verified,
      listedAt: job.listed_at,
      shareLink: job.share_link,
      dateAdded: job.date_added,
    }
    ));

    //res.json({ jobs, totalJobs });
    res.json({ jobs: transformedJobs, totalJobs });
  } catch (err) {
    res.status(500).send(err);
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});