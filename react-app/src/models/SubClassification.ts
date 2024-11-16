import * as Sequelize from 'sequelize';
import { DataTypes, Model, Optional } from 'sequelize';
import type { Classification, ClassificationId } from './Classification';
import type { Job, JobId } from './Job';

export interface SubClassificationAttributes {
  subClassificationId: number;
  classificationId: number;
  label: string;
}

export type SubClassificationPk = "subClassificationId";
export type SubClassificationId = SubClassification[SubClassificationPk];
export type SubClassificationCreationAttributes = SubClassificationAttributes;

export class SubClassification extends Model<SubClassificationAttributes, SubClassificationCreationAttributes> implements SubClassificationAttributes {
  subClassificationId!: number;
  classificationId!: number;
  label!: string;

  // SubClassification belongsTo Classification via classificationId
  classification!: Classification;
  getClassification!: Sequelize.BelongsToGetAssociationMixin<Classification>;
  setClassification!: Sequelize.BelongsToSetAssociationMixin<Classification, ClassificationId>;
  createClassification!: Sequelize.BelongsToCreateAssociationMixin<Classification>;
  // SubClassification hasMany Job via subClassificationId
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

  static initModel(sequelize: Sequelize.Sequelize): typeof SubClassification {
    return SubClassification.init({
    subClassificationId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      primaryKey: true,
      field: 'subClassification_Id'
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
    label: {
      type: DataTypes.STRING(255),
      allowNull: false
    }
  }, {
    sequelize,
    tableName: 'SubClassification',
    timestamps: false,
    indexes: [
      {
        name: "PRIMARY",
        unique: true,
        using: "BTREE",
        fields: [
          { name: "subClassification_Id" },
        ]
      },
      {
        name: "classification_Id",
        using: "BTREE",
        fields: [
          { name: "classification_Id" },
        ]
      },
    ]
  });
  }
}
