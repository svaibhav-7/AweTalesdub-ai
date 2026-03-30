const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    // ssl: { rejectUnauthorized: false } // Enable for production/Render
});

// Test connection
pool.on('connect', () => {
    console.log('🔗 Connected to PostgreSQL Database');
});

// Basic script to initialize tables if they don't exist
const initializeDB = async () => {
  let client;
  try {
    client = await pool.connect();
    await client.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(50) DEFAULT 'user',
        credits INTEGER DEFAULT 10,
        plan VARCHAR(50) DEFAULT 'free',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS dub_jobs (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        source_url VARCHAR(500),
        target_language VARCHAR(50),
        status VARCHAR(50) DEFAULT 'pending',
        cost_credits INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
      
      CREATE TABLE IF NOT EXISTS global_announcements (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        message TEXT,
        active BOOLEAN DEFAULT true,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);
    console.log('✅ Database schema initialized');
  } catch (err) {
    console.error('⚠️ Warning: Could not connect to PostgreSQL. The server will still run, but database features will fail. Ensure Postgres is running on port 5432.');
  } finally {
    if (client) client.release();
  }
};

module.exports = {
    query: (text, params) => pool.query(text, params),
    initializeDB
};
