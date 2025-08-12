#!/bin/bash

# AWS Cognito Setup Script for Group Fitness App
# Make sure you have AWS CLI configured: aws configure

set -e

echo "🚀 Setting up AWS Cognito for Group Fitness App..."

# Step 1: Create User Pool
echo "📝 Creating User Pool..."
USER_POOL_RESPONSE=$(aws cognito-idp create-user-pool \
  --pool-name "group-fitness-dev" \
  --policies '{
    "PasswordPolicy": {
      "MinimumLength": 8,
      "RequireUppercase": true,
      "RequireLowercase": true,
      "RequireNumbers": true,
      "RequireSymbols": true
    }
  }' \
  --auto-verified-attributes email \
  --username-attributes email \
  --schema '[
    {
      "Name": "email",
      "AttributeDataType": "String",
      "Required": true,
      "Mutable": true
    },
    {
      "Name": "name",
      "AttributeDataType": "String",
      "Required": false,
      "Mutable": true
    }
  ]' \
  --account-recovery-setting '{
    "RecoveryMechanisms": [
      {
        "Name": "verified_email",
        "Priority": 1
      }
    ]
  }')

USER_POOL_ID=$(echo $USER_POOL_RESPONSE | jq -r '.UserPool.Id')
echo "✅ User Pool created: $USER_POOL_ID"

# Step 2: Create App Client
echo "📱 Creating App Client..."
CLIENT_RESPONSE=$(aws cognito-idp create-user-pool-client \
  --user-pool-id $USER_POOL_ID \
  --client-name "group-fitness-web-client" \
  --no-generate-secret \
  --explicit-auth-flows ALLOW_USER_PASSWORD_AUTH ALLOW_REFRESH_TOKEN_AUTH ALLOW_USER_SRP_AUTH \
  --supported-identity-providers COGNITO \
  --callback-urls "http://localhost:3000" "http://localhost:3000/callback" \
  --logout-urls "http://localhost:3000" "http://localhost:3000/signout" \
  --allowed-o-auth-flows "implicit" "code" \
  --allowed-o-auth-scopes "email" "openid" "profile" \
  --allowed-o-auth-flows-user-pool-client)

CLIENT_ID=$(echo $CLIENT_RESPONSE | jq -r '.UserPoolClient.ClientId')
echo "✅ App Client created: $CLIENT_ID"

# Step 3: Create Identity Pool (optional)
echo "🆔 Creating Identity Pool..."
IDENTITY_POOL_RESPONSE=$(aws cognito-identity create-identity-pool \
  --identity-pool-name "group-fitness-dev-identity" \
  --allow-unauthenticated-identities \
  --cognito-identity-providers ProviderName="cognito-idp.us-east-1.amazonaws.com/$USER_POOL_ID",ClientId="$CLIENT_ID",ServerSideTokenCheck=false)

IDENTITY_POOL_ID=$(echo $IDENTITY_POOL_RESPONSE | jq -r '.IdentityPoolId')
echo "✅ Identity Pool created: $IDENTITY_POOL_ID"

# Step 4: Create .env file
echo "📄 Creating .env file..."
if [ -f .env ]; then
    echo "⚠️  .env file already exists. Backing up to .env.backup"
    cp .env .env.backup
fi

cat > .env << EOF
# Database
DATABASE_URL=postgresql://dev_user:dev_password@localhost:5432/group_fitness_dev

# Redis
REDIS_URL=redis://localhost:6379

# S3/MinIO
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=group-fitness-dev

# AWS Cognito
AWS_REGION=us-east-1
COGNITO_USER_POOL_ID=$USER_POOL_ID
COGNITO_CLIENT_ID=$CLIENT_ID
COGNITO_IDENTITY_POOL_ID=$IDENTITY_POOL_ID

# JWT Secret (for development)
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
EOF

echo "✅ .env file created with your Cognito credentials"

# Step 5: Test setup
echo "🧪 Testing setup..."
echo "Creating test user..."
aws cognito-idp admin-create-user \
  --user-pool-id $USER_POOL_ID \
  --username "test@example.com" \
  --user-attributes Name=email,Value=test@example.com Name=name,Value="Test User" \
  --temporary-password "TempPass123!" \
  --message-action SUPPRESS

echo "✅ Test user created: test@example.com"
echo "📧 Check your email for confirmation code"

echo ""
echo "🎉 AWS Cognito setup complete!"
echo ""
echo "📋 Summary:"
echo "   User Pool ID: $USER_POOL_ID"
echo "   Client ID: $CLIENT_ID"
echo "   Identity Pool ID: $IDENTITY_POOL_ID"
echo ""
echo "🔧 Next steps:"
echo "   1. Start your backend: docker-compose up -d"
echo "   2. Test signup: curl -X POST http://localhost:8000/auth/signup"
echo "   3. Check email for confirmation code"
echo "   4. Confirm signup and test signin"
echo ""
echo "📚 Documentation: http://localhost:8000/docs" 