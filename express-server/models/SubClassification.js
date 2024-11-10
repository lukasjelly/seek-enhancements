const Sequelize = require('sequelize');
module.exports = function(sequelize, DataTypes) {
  return sequelize.define('SubClassification', {
    subClassification_Id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      primaryKey: true
    },
    classification_Id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'Classification',
        key: 'classification_Id'
      }
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
};
