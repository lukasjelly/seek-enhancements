const express = require('express');
const { Sequelize } = require('sequelize');
const initModels = require('./models/init-models');
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
    const offset = (page - 1) * limit;
    const jobs = await Job.findAll({ offset, limit });
    res.json(jobs);
  } catch (err) {
    res.status(500).send(err);
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});