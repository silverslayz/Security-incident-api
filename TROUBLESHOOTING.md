# Troubleshooting Guide

## Docker Issues

### Error: `docker: command not found` or `docker-compose: command not found`

**Issue**: Docker is not installed or not available in the system PATH.

**Solutions**:

#### Option 1: Install Docker Desktop (Recommended for Windows)
1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/)
2. Install and restart your computer
3. Verify installation: `docker --version`
4. Run the application: `docker compose up -d`

#### Option 2: Run Locally Without Docker

If you cannot install Docker, you can run the application directly with Python:

1. **Create a Python virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Use SQLite for local development**:
   - The `.env` file is configured to use SQLite by default
   - No PostgreSQL installation needed for quick testing

4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs

### Switching Between SQLite and PostgreSQL

**SQLite** (Default for local development):
```env
DATABASE_URL=sqlite:///./incident_db.sqlite
```

**PostgreSQL** (Production):
```env
DATABASE_URL=postgresql://user:password@localhost:5432/incident_db
```

Note: Some features may have slight differences between SQLite and PostgreSQL, but core functionality works with both.

## Common Setup Issues

### Issue: `pg_config executable not found` or `psycopg2-binary` installation error
**Issue**: Error when installing `psycopg2-binary` package: "Error: pg_config executable not found"

**Solution**: This error occurs because PostgreSQL is not installed. For local development with SQLite:
1. The `psycopg2-binary` line is already commented out in `requirements.txt`
2. Simply install dependencies normally: `pip install -r requirements.txt`
3. Use SQLite in your `.env` file: `DATABASE_URL=sqlite:///./incident_db.sqlite`

If you need PostgreSQL support:
- Uncomment the `psycopg2-binary` line in `requirements.txt`
- Install PostgreSQL on your system
- Update `.env` with PostgreSQL connection string

### Issue: `Cargo, the Rust package manager, is not installed` or pydantic-core compilation error
**Issue**: Error during pip install: "Cargo, the Rust package manager, is not installed" when installing pydantic-core

**Solution**: This occurs when using Python 3.14+ with older pydantic versions that don't have pre-built wheels.
- The `requirements.txt` has been updated to use `pydantic>=2.10.5` which includes pre-built wheels for Python 3.14
- No Rust installation required
- Simply run: `pip install -r requirements.txt`

If you encounter this with Python 3.14+, the pydantic versions have been updated to support it.

### Issue: `ModuleNotFoundError`
**Solution**: Make sure you've activated the virtual environment and installed dependencies:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Database connection errors
**Solution**: Check your `DATABASE_URL` in `.env` file matches your database setup.

### Issue: Import errors
**Solution**: Make sure you're running uvicorn from the project root directory:
```bash
cd C:\Users\jesus\OneDrive\Desktop\security-incident-api
uvicorn app.main:app --reload
```
