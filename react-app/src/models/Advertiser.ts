import * as Sequelize from 'sequelize';
import { DataTypes, Model, Optional } from 'sequelize';
import type { Job, JobId } from './Job';

export interface AdvertiserAttributes {
  advertiserId: number;
  name: string;
  isVerified?: number;
  registrationDate?: Date;
  dateAdded?: Date;
}

export type AdvertiserPk = "advertiserId";
export type AdvertiserId = Advertiser[AdvertiserPk];
export type AdvertiserOptionalAttributes = "isVerified" | "registrationDate" | "dateAdded";
export type AdvertiserCreationAttributes = Optional<AdvertiserAttributes, AdvertiserOptionalAttributes>;

export class Advertiser extends Model<AdvertiserAttributes, AdvertiserCreationAttributes> implements AdvertiserAttributes {
  advertiserId!: number;
  name!: string;
  isVerified?: number;
  registrationDate?: Date;
  dateAdded?: Date;

  // Advertiser hasMany Job via advertiserId
  jobs!: Job[];
  getJobs!: Sequelize.HasManyGetAssociationsMixin<Job>;
  setJobs!: Sequelize.HasManySetAssociationsMixin<Job, JobId>;
  addJob!: Sequelize.HasManyAddAssociationMixin<Job, JobId>;
  addJobs!: Sequelize.HasManyAddAssociationsMixin<Job, JobId>;
  createJob!: Sequelize.HasManyCreateAssociationMixin<Job>;
  removeJob!: Sequelize.HasManyRemoveAssociationMixin<Job, JobId>;
  removeJobs!: Sequelize.HasManyRemoveAssociationsMixin<Job, JobId>;
  hasJob!: Sequelize.HasManyHasAssociationMixin<Job, JobId>;
  hasJobs!: Sequelize.HasManyHasAssociationsMixin<Job, JobId>;
  countJobs!: Sequelize.HasManyCountAssociationsMixin;

  static initModel(sequelize: Sequelize.Sequelize): typeof Advertiser {
    return Advertiser.init({
    advertiserId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      primaryKey: true,
      field: 'advertiser_Id'
    },
    name: {
      type: DataTypes.STRING(255),
      allowNull: false
    },
    isVerified: {
      type: DataTypes.BOOLEAN,
      allowNull: true,
      field: 'is_verified'
    },
    registrationDate: {
      type: DataTypes.DATE,
      allowNull: true,
      field: 'registration_date'
    },
    dateAdded: {
      type: DataTypes.DATE,
      allowNull: true,
      field: 'date_added'
    }
  }, {
    sequelize,
    tableName: 'Advertiser',
    timestamps: false,
    indexes: [
      {
        name: "PRIMARY",
        unique: true,
        using: "BTREE",
        fields: [
          { name: "advertiser_Id" },
        ]
      },
    ]
  });
  }
}
