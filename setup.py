"""
Setup script to generate secure configuration.
Run this once before starting the application.
"""
import secrets
import os

def generate_secret_key():
    """Generate a secure random secret key for JWT tokens"""
    return secrets.token_hex(32)

def create_env_file():
    """Create .env file with secure defaults"""
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Skipping creation.")
        return

    secret_key = generate_secret_key()

    env_content = f"""# Database
DATABASE_URL=postgresql://incident_user:incident_pass@localhost:5432/incident_db

# Security - CHANGE SECRET_KEY IN PRODUCTION
SECRET_KEY={secret_key}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AWS (optional, for file uploads)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
S3_BUCKET_NAME=

# Application
DEBUG=True
"""

    with open('.env', 'w') as f:
        f.write(env_content)

    print("✅ Created .env file with secure secret key")
    print(f"🔐 Secret Key: {secret_key}")
    print("\n⚠️  IMPORTANT: Change the SECRET_KEY in production!")

if __name__ == "__main__":
    print("🚀 Security Incident API - Setup")
    print("=" * 50)
    create_env_file()
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Start services: docker-compose up -d")
    print("2. Access API docs: http://localhost:8000/docs")
    print("3. Register your first admin user")
