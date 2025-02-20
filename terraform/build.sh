zip -r lambda.zip ../backend/lambda_function/*
terraform init
terraform plan
terraform apply -auto-approve