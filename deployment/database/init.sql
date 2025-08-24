-- Database initialization script for Founder Sourcing Agent
-- This script sets up the database and creates initial seed data

-- Create database if it doesn't exist (run this as superuser)
-- CREATE DATABASE founder_sourcing_agent;

-- Connect to the database
-- \c founder_sourcing_agent;

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create a dedicated user for the application (optional)
-- CREATE USER founder_app WITH PASSWORD 'your_secure_password';
-- GRANT ALL PRIVILEGES ON DATABASE founder_sourcing_agent TO founder_app;

-- Set timezone
SET timezone = 'UTC';

-- Create initial admin user (password: admin123 - change in production!)
INSERT INTO users (email, username, hashed_password, full_name, is_active, is_verified)
VALUES (
    'admin@foundersourcing.com',
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', -- admin123
    'System Administrator',
    TRUE,
    TRUE
) ON CONFLICT (email) DO NOTHING;

-- Create sample search criteria
INSERT INTO searches (user_id, search_criteria, status)
VALUES (
    1,
    '{"keywords": ["founder", "startup", "tech"], "location": "San Francisco", "experience": "5+ years"}',
    'completed'
) ON CONFLICT DO NOTHING;

-- Create sample candidate data
INSERT INTO candidates (search_id, harvest_id, name, title, company, location, linkedin_url, bio, score, status)
VALUES (
    1,
    'sample_001',
    'John Smith',
    'Founder & CEO',
    'TechStart Inc.',
    'San Francisco, CA',
    'https://linkedin.com/in/johnsmith',
    'Experienced founder with 8+ years in SaaS and fintech. Previously founded and sold two companies.',
    0.85,
    'qualified'
),
(
    1,
    'sample_002',
    'Sarah Johnson',
    'Co-Founder & CTO',
    'InnovateLab',
    'San Francisco, CA',
    'https://linkedin.com/in/sarahjohnson',
    'Technical co-founder with strong background in AI/ML and product development.',
    0.92,
    'qualified'
) ON CONFLICT DO NOTHING;
