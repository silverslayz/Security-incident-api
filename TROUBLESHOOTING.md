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
