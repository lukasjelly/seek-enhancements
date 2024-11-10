const Sequelize = require('sequelize');
module.exports = function(sequelize, DataTypes) {
  return sequelize.define('JobLocation', {
    job_location_Id: {
      autoIncrement: true,
      type: DataTypes.INTEGER,
      allowNull: false,
      primaryKey: true
    },
    job_Id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'Job',
        key: 'job_Id'
      }
    },
    location_Id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'Location',
        key: 'location_Id'
      }
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
};
