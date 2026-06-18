-- LandScope AI — PostgreSQL Initialization Script
-- Enables required extensions: PostGIS, pgvector, uuid-ossp

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Create full-text search configuration for project data
-- This enables efficient text search across project names and descriptions
