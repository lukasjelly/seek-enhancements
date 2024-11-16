import * as Sequelize from 'sequelize';
import { DataTypes, Model, Optional } from 'sequelize';
import type { Job, JobId } from './Job';
import type { SubClassification, SubClassificationId } from './SubClassification';

export interface ClassificationAttributes {
  classificationId: number;
  label: string;
}

export type ClassificationPk = "classificationId";
export type ClassificationId = Classification[ClassificationPk];
export type ClassificationCreationAttributes = ClassificationAttributes;

export class Classification extends Model<ClassificationAttributes, ClassificationCreationAttributes> implements ClassificationAttributes {
  classificationId!: number;
  label!: string;

  // Classification hasMany Job via classificationId
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
  // Classification hasMany SubClassification via classificationId
  subClassifications!: SubClassification[];
  getSubClassifications!: Sequelize.HasManyGetAssociationsMixin<SubClassification>;
  setSubClassifications!: Sequelize.HasManySetAssociationsMixin<SubClassification, SubClassificationId>;
  addSubClassification!: Sequelize.HasManyAddAssociationMixin<SubClassification, SubClassificationId>;
  addSubClassifications!: Sequelize.HasManyAddAssociationsMixin<SubClassification, SubClassificationId>;
  createSubClassification!: Sequelize.HasManyCreateAssociationMixin<SubClassification>;
  removeSubClassification!: Sequelize.HasManyRemoveAssociationMixin<SubClassification, SubClassificationId>;
  removeSubClassifications!: Sequelize.HasManyRemoveAssociationsMixin<SubClassification, SubClassificationId>;
  hasSubClassification!: Sequelize.HasManyHasAssociationMixin<SubClassification, SubClassificationId>;
  hasSubClassifications!: Sequelize.HasManyHasAssociationsMixin<SubClassification, SubClassificationId>;
  countSubClassifications!: Sequelize.HasManyCountAssociationsMixin;

  static initModel(sequelize: Sequelize.Sequelize): typeof Classification {
    return Classification.init({
    classificationId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      primaryKey: true,
      field: 'classification_Id'
    },
    label: {
      type: DataTypes.STRING(255),
      allowNull: false
    }
  }, {
    sequelize,
    tableName: 'Classification',
    timestamps: false,
    indexes: [
      {
        name: "PRIMARY",
        unique: true,
        using: "BTREE",
        fields: [
          { name: "classification_Id" },
        ]
      },
    ]
  });
  }
}
