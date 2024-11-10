const Sequelize = require('sequelize');
module.exports = function(sequelize, DataTypes) {
  return sequelize.define('Job', {
    job_Id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      primaryKey: true
    },
    advertiser_Id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'Advertiser',
        key: 'advertiser_Id'
      }
    },
    classification_Id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'Classification',
        key: 'classification_Id'
      }
    },
    subClassification_Id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'SubClassification',
        key: 'subClassification_Id'
      }
    },
    work_type_Id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'WorkType',
        key: 'work_type_Id'
      }
    },
    title: {
      type: DataTypes.STRING(255),
      allowNull: true
    },
    phone_number: {
      type: DataTypes.STRING(20),
      allowNull: true
    },
    is_expired: {
      type: DataTypes.BOOLEAN,
      allowNull: true
    },
    expires_at: {
      type: DataTypes.DATE,
      allowNull: true
    },
    is_link_out: {
      type: DataTypes.BOOLEAN,
      allowNull: true
    },
    is_verified: {
      type: DataTypes.BOOLEAN,
      allowNull: true
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
    listed_at: {
      type: DataTypes.DATE,
      allowNull: true
    },
    salary: {
      type: DataTypes.STRING(255),
      allowNull: true
    },
    share_link: {
      type: DataTypes.STRING(255),
      allowNull: true
    },
    date_added: {
      type: DataTypes.DATE,
      allowNull: true
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
};
