cd ../backend/lambda_function
zip -r ../../terraform/lambda.zip .
cd ../../terraform
terraform init
terraform plan
terraform apply -auto-approve