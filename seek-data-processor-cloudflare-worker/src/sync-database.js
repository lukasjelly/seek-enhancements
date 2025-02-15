// filepath: /C:/Users/lukas/source/repos/lukasjelly/seek-enhancements/seek-data-processor-cloudflare-worker/src/sync.js
const { sequelize } = require('./models');

async function syncDatabase() {
    try {
        await sequelize.sync({ force: true }); // Use { force: true } to drop and recreate the tables
        console.log('Database synchronized successfully.');
    } catch (error) {
        console.error('Error synchronizing the database:', error);
    } finally {
        await sequelize.close();
    }
}

syncDatabase();