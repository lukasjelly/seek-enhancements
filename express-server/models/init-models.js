const { DataTypes } = require('sequelize');
const _Advertiser = require('./Advertiser');
const _Classification = require('./Classification');
const _Job = require('./Job');
const _JobLocation = require('./JobLocation');
const _Location = require('./Location');
const _SubClassification = require('./SubClassification');
const _WorkType = require('./WorkType');

function initModels(sequelize) {
  const Advertiser = _Advertiser(sequelize, DataTypes);
  const Classification = _Classification(sequelize, DataTypes);
  const Job = _Job(sequelize, DataTypes);
  const JobLocation = _JobLocation(sequelize, DataTypes);
  const Location = _Location(sequelize, DataTypes);
  const SubClassification = _SubClassification(sequelize, DataTypes);
  const WorkType = _WorkType(sequelize, DataTypes);

  Job.belongsTo(Advertiser, { as: "advertiser", foreignKey: "advertiser_Id" });
  Advertiser.hasMany(Job, { as: "Jobs", foreignKey: "advertiser_Id" });
  Job.belongsTo(Classification, { as: "classification", foreignKey: "classification_Id" });
  Classification.hasMany(Job, { as: "Jobs", foreignKey: "classification_Id" });
  SubClassification.belongsTo(Classification, { as: "classification", foreignKey: "classification_Id" });
  Classification.hasMany(SubClassification, { as: "SubClassifications", foreignKey: "classification_Id" });
  JobLocation.belongsTo(Job, { as: "job", foreignKey: "job_Id" });
  Job.hasMany(JobLocation, { as: "JobLocations", foreignKey: "job_Id" });
  JobLocation.belongsTo(Location, { as: "location", foreignKey: "location_Id" });
  Location.hasMany(JobLocation, { as: "JobLocations", foreignKey: "location_Id" });
  Job.belongsTo(SubClassification, { as: "subClassification", foreignKey: "subClassification_Id" });
  SubClassification.hasMany(Job, { as: "Jobs", foreignKey: "subClassification_Id" });
  Job.belongsTo(WorkType, { as: "work_type", foreignKey: "work_type_Id" });
  WorkType.hasMany(Job, { as: "Jobs", foreignKey: "work_type_Id" });

  return {
    Advertiser,
    Classification,
    Job,
    JobLocation,
    Location,
    SubClassification,
    WorkType,
  };
}

module.exports = initModels;