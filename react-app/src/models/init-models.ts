import type { Sequelize } from "sequelize";
import { Advertiser as _Advertiser } from "./Advertiser";
import type { AdvertiserAttributes, AdvertiserCreationAttributes } from "./Advertiser";
import { Classification as _Classification } from "./Classification";
import type { ClassificationAttributes, ClassificationCreationAttributes } from "./Classification";
import { Job as _Job } from "./Job";
import type { JobAttributes, JobCreationAttributes } from "./Job";
import { JobLocation as _JobLocation } from "./JobLocation";
import type { JobLocationAttributes, JobLocationCreationAttributes } from "./JobLocation";
import { Location as _Location } from "./Location";
import type { LocationAttributes, LocationCreationAttributes } from "./Location";
import { SubClassification as _SubClassification } from "./SubClassification";
import type { SubClassificationAttributes, SubClassificationCreationAttributes } from "./SubClassification";
import { WorkType as _WorkType } from "./WorkType";
import type { WorkTypeAttributes, WorkTypeCreationAttributes } from "./WorkType";

export {
  _Advertiser as Advertiser,
  _Classification as Classification,
  _Job as Job,
  _JobLocation as JobLocation,
  _Location as Location,
  _SubClassification as SubClassification,
  _WorkType as WorkType,
};

export type {
  AdvertiserAttributes,
  AdvertiserCreationAttributes,
  ClassificationAttributes,
  ClassificationCreationAttributes,
  JobAttributes,
  JobCreationAttributes,
  JobLocationAttributes,
  JobLocationCreationAttributes,
  LocationAttributes,
  LocationCreationAttributes,
  SubClassificationAttributes,
  SubClassificationCreationAttributes,
  WorkTypeAttributes,
  WorkTypeCreationAttributes,
};

export function initModels(sequelize: Sequelize) {
  const Advertiser = _Advertiser.initModel(sequelize);
  const Classification = _Classification.initModel(sequelize);
  const Job = _Job.initModel(sequelize);
  const JobLocation = _JobLocation.initModel(sequelize);
  const Location = _Location.initModel(sequelize);
  const SubClassification = _SubClassification.initModel(sequelize);
  const WorkType = _WorkType.initModel(sequelize);

  Job.belongsTo(Advertiser, { as: "advertiser", foreignKey: "advertiserId"});
  Advertiser.hasMany(Job, { as: "jobs", foreignKey: "advertiserId"});
  Job.belongsTo(Classification, { as: "classification", foreignKey: "classificationId"});
  Classification.hasMany(Job, { as: "jobs", foreignKey: "classificationId"});
  SubClassification.belongsTo(Classification, { as: "classification", foreignKey: "classificationId"});
  Classification.hasMany(SubClassification, { as: "subClassifications", foreignKey: "classificationId"});
  JobLocation.belongsTo(Job, { as: "job", foreignKey: "jobId"});
  Job.hasMany(JobLocation, { as: "jobLocations", foreignKey: "jobId"});
  JobLocation.belongsTo(Location, { as: "location", foreignKey: "locationId"});
  Location.hasMany(JobLocation, { as: "jobLocations", foreignKey: "locationId"});
  Job.belongsTo(SubClassification, { as: "subClassification", foreignKey: "subClassificationId"});
  SubClassification.hasMany(Job, { as: "jobs", foreignKey: "subClassificationId"});
  Job.belongsTo(WorkType, { as: "workType", foreignKey: "workTypeId"});
  WorkType.hasMany(Job, { as: "jobs", foreignKey: "workTypeId"});

  return {
    Advertiser: Advertiser,
    Classification: Classification,
    Job: Job,
    JobLocation: JobLocation,
    Location: Location,
    SubClassification: SubClassification,
    WorkType: WorkType,
  };
}
