import * as Sequelize from 'sequelize';
import { DataTypes, Model, Optional } from 'sequelize';
import type { Advertiser, AdvertiserId } from './Advertiser';
import type { Classification, ClassificationId } from './Classification';
import type { JobLocation, JobLocationId } from './JobLocation';
import type { SubClassification, SubClassificationId } from './SubClassification';
import type { WorkType, WorkTypeId } from './WorkType';

export interface JobAttributes {
  jobId: number;
  advertiserId: number;
  classificationId: number;
  subClassificationId: number;
  workTypeId: number;
  title?: string;
  phoneNumber?: string;
  isExpired?: number;
  expiresAt?: Date;
  isLinkOut?: number;
  isVerified?: number;
  abstract?: string;
  content?: string;
  status?: string;
  listedAt?: Date;
  salary?: string;
  shareLink?: string;
  dateAdded?: Date;
  bullets?: string;
  questions?: string;
}

export type JobPk = "jobId";
export type JobId = Job[JobPk];
export type JobOptionalAttributes = "title" | "phoneNumber" | "isExpired" | "expiresAt" | "isLinkOut" | "isVerified" | "abstract" | "content" | "status" | "listedAt" | "salary" | "shareLink" | "dateAdded" | "bullets" | "questions";
export type JobCreationAttributes = Optional<JobAttributes, JobOptionalAttributes>;

export class Job extends Model<JobAttributes, JobCreationAttributes> implements JobAttributes {
  jobId!: number;
  advertiserId!: number;
  classificationId!: number;
  subClassificationId!: number;
  workTypeId!: number;
  title?: string;
  phoneNumber?: string;
  isExpired?: number;
  expiresAt?: Date;
  isLinkOut?: number;
  isVerified?: number;
  abstract?: string;
  content?: string;
  status?: string;
  listedAt?: Date;
  salary?: string;
  shareLink?: string;
  dateAdded?: Date;
  bullets?: string;
  questions?: string;

  // Job belongsTo Advertiser via advertiserId
  advertiser!: Advertiser;
  getAdvertiser!: Sequelize.BelongsToGetAssociationMixin<Advertiser>;
  setAdvertiser!: Sequelize.BelongsToSetAssociationMixin<Advertiser, AdvertiserId>;
  createAdvertiser!: Sequelize.BelongsToCreateAssociationMixin<Advertiser>;
  // Job belongsTo Classification via classificationId
  classification!: Classification;
  getClassification!: Sequelize.BelongsToGetAssociationMixin<Classification>;
  setClassification!: Sequelize.BelongsToSetAssociationMixin<Classification, ClassificationId>;
  createClassification!: Sequelize.BelongsToCreateAssociationMixin<Classification>;
  // Job hasMany JobLocation via jobId
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
  // Job belongsTo SubClassification via subClassificationId
  subClassification!: SubClassification;
  getSubClassification!: Sequelize.BelongsToGetAssociationMixin<SubClassification>;
  setSubClassification!: Sequelize.BelongsToSetAssociationMixin<SubClassification, SubClassificationId>;
  createSubClassification!: Sequelize.BelongsToCreateAssociationMixin<SubClassification>;
  // Job belongsTo WorkType via workTypeId
  workType!: WorkType;
  getWorkType!: Sequelize.BelongsToGetAssociationMixin<WorkType>;
  setWorkType!: Sequelize.BelongsToSetAssociationMixin<WorkType, WorkTypeId>;
  createWorkType!: Sequelize.BelongsToCreateAssociationMixin<WorkType>;

  static initModel(sequelize: Sequelize.Sequelize): typeof Job {
    return Job.init({
    jobId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      primaryKey: true,
      field: 'job_Id'
    },
    advertiserId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'Advertiser',
        key: 'advertiser_Id'
      },
      field: 'advertiser_Id'
    },
    classificationId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'Classification',
        key: 'classification_Id'
      },
      field: 'classification_Id'
    },
    subClassificationId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'SubClassification',
        key: 'subClassification_Id'
      },
      field: 'subClassification_Id'
    },
    workTypeId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'WorkType',
        key: 'work_type_Id'
      },
      field: 'work_type_Id'
    },
    title: {
      type: DataTypes.STRING(255),
      allowNull: true
    },
    phoneNumber: {
      type: DataTypes.STRING(20),
      allowNull: true,
      field: 'phone_number'
    },
    isExpired: {
      type: DataTypes.BOOLEAN,
      allowNull: true,
      field: 'is_expired'
    },
    expiresAt: {
      type: DataTypes.DATE,
      allowNull: true,
      field: 'expires_at'
    },
    isLinkOut: {
      type: DataTypes.BOOLEAN,
      allowNull: true,
      field: 'is_link_out'
    },
    isVerified: {
      type: DataTypes.BOOLEAN,
      allowNull: true,
      field: 'is_verified'
    },
    abstract: {
      type: DataTypes.TEXT,
      allowNull: true
    },
    content: {
      type: DataTypes.TEXT,
      allowNull: true
    },
    status: {
      type: DataTypes.STRING(50),
      allowNull: true
    },
    listedAt: {
      type: DataTypes.DATE,
      allowNull: true,
      field: 'listed_at'
    },
    salary: {
      type: DataTypes.STRING(255),
      allowNull: true
    },
    shareLink: {
      type: DataTypes.STRING(255),
      allowNull: true,
      field: 'share_link'
    },
    dateAdded: {
      type: DataTypes.DATE,
      allowNull: true,
      field: 'date_added'
    },
    bullets: {
      type: DataTypes.TEXT,
      allowNull: true
    },
    questions: {
      type: DataTypes.TEXT,
      allowNull: true
    }
  }, {
    sequelize,
    tableName: 'Job',
    timestamps: false,
    indexes: [
      {
        name: "PRIMARY",
        unique: true,
        using: "BTREE",
        fields: [
          { name: "job_Id" },
        ]
      },
      {
        name: "fk_job_advertiser",
        using: "BTREE",
        fields: [
          { name: "advertiser_Id" },
        ]
      },
      {
        name: "fk_job_classification",
        using: "BTREE",
        fields: [
          { name: "classification_Id" },
        ]
      },
      {
        name: "fk_job_subclassification",
        using: "BTREE",
        fields: [
          { name: "subClassification_Id" },
        ]
      },
      {
        name: "fk_job_worktype",
        using: "BTREE",
        fields: [
          { name: "work_type_Id" },
        ]
      },
    ]
  });
  }
}
