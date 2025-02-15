const { Sequelize, DataTypes } = require('sequelize');
const sequelize = new Sequelize(process.env.SeekDatabaseConnectionString, {
    dialect: 'mysql'
});

const Advertiser = sequelize.define('Advertiser', {
    advertiser_Id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    name: {
        type: DataTypes.STRING(255),
        allowNull: false
    },
    is_verified: {
        type: DataTypes.TINYINT(1)
    },
    registration_date: {
        type: DataTypes.DATE
    },
    date_added: {
        type: DataTypes.DATE
    }
}, {
    tableName: 'Advertiser',
    timestamps: false
});

const Classification = sequelize.define('Classification', {
    classification_Id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    label: {
        type: DataTypes.STRING(255),
        allowNull: false
    }
}, {
    tableName: 'Classification',
    timestamps: false
});

const Location = sequelize.define('Location', {
    location_Id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    area: {
        type: DataTypes.STRING(255)
    },
    location: {
        type: DataTypes.STRING(255)
    }
}, {
    tableName: 'Location',
    timestamps: false
});

const WorkType = sequelize.define('WorkType', {
    work_type_Id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    label: {
        type: DataTypes.STRING(255),
        allowNull: false
    }
}, {
    tableName: 'WorkType',
    timestamps: false
});

const SubClassification = sequelize.define('SubClassification', {
    subClassification_Id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    classification_Id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: Classification,
            key: 'classification_Id'
        }
    },
    label: {
        type: DataTypes.STRING(255),
        allowNull: false
    }
}, {
    tableName: 'SubClassification',
    timestamps: false
});

const Job = sequelize.define('Job', {
    job_Id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    advertiser_Id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: Advertiser,
            key: 'advertiser_Id'
        }
    },
    classification_Id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: Classification,
            key: 'classification_Id'
        }
    },
    subClassification_Id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: SubClassification,
            key: 'subClassification_Id'
        }
    },
    work_type_Id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: WorkType,
            key: 'work_type_Id'
        }
    },
    title: {
        type: DataTypes.STRING(255)
    },
    phone_number: {
        type: DataTypes.STRING(20)
    },
    is_expired: {
        type: DataTypes.TINYINT(1)
    },
    expires_at: {
        type: DataTypes.DATE
    },
    is_link_out: {
        type: DataTypes.TINYINT(1)
    },
    is_verified: {
        type: DataTypes.TINYINT(1)
    },
    abstract: {
        type: DataTypes.TEXT
    },
    content: {
        type: DataTypes.TEXT
    },
    status: {
        type: DataTypes.STRING(50)
    },
    listed_at: {
        type: DataTypes.DATE
    },
    salary: {
        type: DataTypes.STRING(255)
    },
    share_link: {
        type: DataTypes.STRING(255)
    },
    date_added: {
        type: DataTypes.DATE
    },
    bullets: {
        type: DataTypes.TEXT
    },
    questions: {
        type: DataTypes.TEXT
    }
}, {
    tableName: 'Job',
    timestamps: false
});

const JobLocation = sequelize.define('JobLocation', {
    job_location_Id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    job_Id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: Job,
            key: 'job_Id'
        }
    },
    location_Id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: Location,
            key: 'location_Id'
        }
    }
}, {
    tableName: 'JobLocation',
    timestamps: false
});

// Define relationships
Advertiser.hasMany(Job, { foreignKey: 'advertiser_Id' });
Classification.hasMany(SubClassification, { foreignKey: 'classification_Id' });
Classification.hasMany(Job, { foreignKey: 'classification_Id' });
SubClassification.belongsTo(Classification, { foreignKey: 'classification_Id' });
SubClassification.hasMany(Job, { foreignKey: 'subClassification_Id' });
WorkType.hasMany(Job, { foreignKey: 'work_type_Id' });
Job.belongsTo(Advertiser, { foreignKey: 'advertiser_Id' });
Job.belongsTo(Classification, { foreignKey: 'classification_Id' });
Job.belongsTo(SubClassification, { foreignKey: 'subClassification_Id' });
Job.belongsTo(WorkType, { foreignKey: 'work_type_Id' });
Job.hasMany(JobLocation, { foreignKey: 'job_Id' });
Location.hasMany(JobLocation, { foreignKey: 'location_Id' });
JobLocation.belongsTo(Job, { foreignKey: 'job_Id' });
JobLocation.belongsTo(Location, { foreignKey: 'location_Id' });

module.exports = {
    Advertiser,
    Classification,
    Location,
    WorkType,
    SubClassification,
    Job,
    JobLocation,
    sequelize
};