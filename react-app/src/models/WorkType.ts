import * as Sequelize from 'sequelize';
import { DataTypes, Model, Optional } from 'sequelize';
import type { Job, JobId } from './Job';

export interface WorkTypeAttributes {
  workTypeId: number;
  label: string;
}

export type WorkTypePk = "workTypeId";
export type WorkTypeId = WorkType[WorkTypePk];
export type WorkTypeCreationAttributes = WorkTypeAttributes;

export class WorkType extends Model<WorkTypeAttributes, WorkTypeCreationAttributes> implements WorkTypeAttributes {
  workTypeId!: number;
  label!: string;

  // WorkType hasMany Job via workTypeId
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

  static initModel(sequelize: Sequelize.Sequelize): typeof WorkType {
    return WorkType.init({
    workTypeId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      primaryKey: true,
      field: 'work_type_Id'
    },
    label: {
      type: DataTypes.STRING(255),
      allowNull: false
    }
  }, {
    sequelize,
    tableName: 'WorkType',
    timestamps: false,
    indexes: [
      {
        name: "PRIMARY",
        unique: true,
        using: "BTREE",
        fields: [
          { name: "work_type_Id" },
        ]
      },
    ]
  });
  }
}
