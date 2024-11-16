import * as Sequelize from 'sequelize';
import { DataTypes, Model, Optional } from 'sequelize';
import type { JobLocation, JobLocationId } from './JobLocation';

export interface LocationAttributes {
  locationId: number;
  area?: string;
  location?: string;
}

export type LocationPk = "locationId";
export type LocationId = Location[LocationPk];
export type LocationOptionalAttributes = "area" | "location";
export type LocationCreationAttributes = Optional<LocationAttributes, LocationOptionalAttributes>;

export class Location extends Model<LocationAttributes, LocationCreationAttributes> implements LocationAttributes {
  locationId!: number;
  area?: string;
  location?: string;

  // Location hasMany JobLocation via locationId
  jobLocations!: JobLocation[];
  getJobLocations!: Sequelize.HasManyGetAssociationsMixin<JobLocation>;
  setJobLocations!: Sequelize.HasManySetAssociationsMixin<JobLocation, JobLocationId>;
  addJobLocation!: Sequelize.HasManyAddAssociationMixin<JobLocation, JobLocationId>;
  addJobLocations!: Sequelize.HasManyAddAssociationsMixin<JobLocation, JobLocationId>;
  createJobLocation!: Sequelize.HasManyCreateAssociationMixin<JobLocation>;
  removeJobLocation!: Sequelize.HasManyRemoveAssociationMixin<JobLocation, JobLocationId>;
  removeJobLocations!: Sequelize.HasManyRemoveAssociationsMixin<JobLocation, JobLocationId>;
  hasJobLocation!: Sequelize.HasManyHasAssociationMixin<JobLocation, JobLocationId>;
  hasJobLocations!: Sequelize.HasManyHasAssociationsMixin<JobLocation, JobLocationId>;
  countJobLocations!: Sequelize.HasManyCountAssociationsMixin;

  static initModel(sequelize: Sequelize.Sequelize): typeof Location {
    return Location.init({
    locationId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      primaryKey: true,
      field: 'location_Id'
    },
    area: {
      type: DataTypes.STRING(255),
      allowNull: true
    },
    location: {
      type: DataTypes.STRING(255),
      allowNull: true
    }
  }, {
    sequelize,
    tableName: 'Location',
    timestamps: false,
    indexes: [
      {
        name: "PRIMARY",
        unique: true,
        using: "BTREE",
        fields: [
          { name: "location_Id" },
        ]
      },
    ]
  });
  }
}
