import * as Sequelize from 'sequelize';
import { DataTypes, Model, Optional } from 'sequelize';
import type { Job, JobId } from './Job';
import type { Location, LocationId } from './Location';

export interface JobLocationAttributes {
  jobLocationId: number;
  jobId: number;
  locationId: number;
}

export type JobLocationPk = "jobLocationId";
export type JobLocationId = JobLocation[JobLocationPk];
export type JobLocationOptionalAttributes = "jobLocationId";
export type JobLocationCreationAttributes = Optional<JobLocationAttributes, JobLocationOptionalAttributes>;

export class JobLocation extends Model<JobLocationAttributes, JobLocationCreationAttributes> implements JobLocationAttributes {
  jobLocationId!: number;
  jobId!: number;
  locationId!: number;

  // JobLocation belongsTo Job via jobId
  job!: Job;
  getJob!: Sequelize.BelongsToGetAssociationMixin<Job>;
  setJob!: Sequelize.BelongsToSetAssociationMixin<Job, JobId>;
  createJob!: Sequelize.BelongsToCreateAssociationMixin<Job>;
  // JobLocation belongsTo Location via locationId
  location!: Location;
  getLocation!: Sequelize.BelongsToGetAssociationMixin<Location>;
  setLocation!: Sequelize.BelongsToSetAssociationMixin<Location, LocationId>;
  createLocation!: Sequelize.BelongsToCreateAssociationMixin<Location>;

  static initModel(sequelize: Sequelize.Sequelize): typeof JobLocation {
    return JobLocation.init({
    jobLocationId: {
      autoIncrement: true,
      type: DataTypes.INTEGER,
      allowNull: false,
      primaryKey: true,
      field: 'job_location_Id'
    },
    jobId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'Job',
        key: 'job_Id'
      },
      field: 'job_Id'
    },
    locationId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'Location',
        key: 'location_Id'
      },
      field: 'location_Id'
    }
  }, {
    sequelize,
    tableName: 'JobLocation',
    timestamps: false,
    indexes: [
      {
        name: "PRIMARY",
        unique: true,
        using: "BTREE",
        fields: [
          { name: "job_location_Id" },
        ]
      },
      {
        name: "job_Id",
        using: "BTREE",
        fields: [
          { name: "job_Id" },
        ]
      },
      {
        name: "location_Id",
        using: "BTREE",
        fields: [
          { name: "location_Id" },
        ]
      },
    ]
  });
  }
}
