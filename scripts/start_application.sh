#!/bin/bash
set -e

# Create local logs directory
mkdir -p ./logs
touch ./logs/start-application.log
chmod 664 ./logs/start-application.log
exec >./logs/start-application.log 2>&1

APP_DIR="."
AWS_REGION="ap-southeast-1"

echo "Starting application deployment..."

# Fetch configuration from Parameter Store
# echo "Fetching configuration from Parameter Store..."
# DB_HOST=$(
#     aws ssm get-parameter --name "/${PROJECT_NAME}/${ENVIRONMENT}/database/url" \
#         --with-decryption --query "Parameter.Value" --output text
# )
# DB_USER=$(
#     aws ssm get-parameter --name "/${PROJECT_NAME}/${ENVIRONMENT}/database/user" \
#         --with-decryption --query "Parameter.Value" --output text
# )
# DB_PASSWORD=$(
#     aws ssm get-parameter --name "/${PROJECT_NAME}/${ENVIRONMENT}/database/password" \
#         --with-decryption --query "Parameter.Value" --output text
# )
# DB_NAME=$(
#     aws ssm get-parameter --name "/${PROJECT_NAME}/${ENVIRONMENT}/database/name" \
#         --with-decryption --query "Parameter.Value" --output text
# )

# # Create/update .env file
# echo "Creating .env file..."
# cat <<EOF >${APP_DIR}/.env
# DATABASE_URL=postgresql+psycopg2://$DB_USER:$DB_PASSWORD@$DB_HOST:5432/$DB_NAME
# EOF

# ECR Authentication
echo "Authenticating with ECR..."
aws ecr get-login-password --region ${AWS_REGION} | \
    docker login --username AWS --password-stdin ${ECR_REPOSITORY_URL}

# Start application
echo "Starting application with Docker Compose..."
cd ${APP_DIR}
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Verify services are running
echo "Verifying services..."
if ! docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo "Error: Services failed to start"
    docker-compose -f docker-compose.prod.yml logs
    exit 1
fi

# Verify SSM agent and Docker are running
echo "Verifying system services..."
sudo systemctl status amazon-ssm-agent --no-pager || true
sudo systemctl status docker --no-pager || true

echo "Application started successfully"