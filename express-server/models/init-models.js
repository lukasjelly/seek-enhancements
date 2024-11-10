var DataTypes = require("sequelize").DataTypes;
var _Advertiser = require("./Advertiser");
var _Classification = require("./Classification");
var _Job = require("./Job");
var _JobLocation = require("./JobLocation");
var _Location = require("./Location");
var _SubClassification = require("./SubClassification");
var _WorkType = require("./WorkType");

function initModels(sequelize) {
  var Advertiser = _Advertiser(sequelize, DataTypes);
  var Classification = _Classification(sequelize, DataTypes);
  var Job = _Job(sequelize, DataTypes);
  var JobLocation = _JobLocation(sequelize, DataTypes);
  var Location = _Location(sequelize, DataTypes);
  var SubClassification = _SubClassification(sequelize, DataTypes);
  var WorkType = _WorkType(sequelize, DataTypes);

  Job.belongsTo(Advertiser, { as: "advertiser", foreignKey: "advertiser_Id"});
  Advertiser.hasMany(Job, { as: "Jobs", foreignKey: "advertiser_Id"});
  Job.belongsTo(Classification, { as: "classification", foreignKey: "classification_Id"});
  Classification.hasMany(Job, { as: "Jobs", foreignKey: "classification_Id"});
  SubClassification.belongsTo(Classification, { as: "classification", foreignKey: "classification_Id"});
  Classification.hasMany(SubClassification, { as: "SubClassifications", foreignKey: "classification_Id"});
  JobLocation.belongsTo(Job, { as: "job", foreignKey: "job_Id"});
  Job.hasMany(JobLocation, { as: "JobLocations", foreignKey: "job_Id"});
  JobLocation.belongsTo(Location, { as: "location", foreignKey: "location_Id"});
  Location.hasMany(JobLocation, { as: "JobLocations", foreignKey: "location_Id"});
  Job.belongsTo(SubClassification, { as: "subClassification", foreignKey: "subClassification_Id"});
  SubClassification.hasMany(Job, { as: "Jobs", foreignKey: "subClassification_Id"});
  Job.belongsTo(WorkType, { as: "work_type", foreignKey: "work_type_Id"});
  WorkType.hasMany(Job, { as: "Jobs", foreignKey: "work_type_Id"});

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
module.exports.initModels = initModels;
module.exports.default = initModels;
