# Homework-6

## 1. Installation of Requirments 

Firstly, you need to install `pipenv`. After installation, you can install all the libraries inside Pipfile by running the following command in terminal. You also need to have `Python3.10`.
```bash
pipenv install
```
You need to install `aws cli` in your system and  configure to save the aws credentials like **aws_access_key_id** and **aws_secret_access_key** by using **[aws_cli](https://docs.aws.amazon.com/cli/latest/reference/configure/index.html)**

## 2. Running Unit Test

To run the unit test, you can run with this command.
```bash
pytest tests/
```

## 3. Running Integration Test

In order to run the integration test, there is two ways.

The first way is running the whole pipeline step by step. First, you need to start `localstack` by using `docker compose`. The localstack will be used for simulating the s3 service.

```bash
docker compose up -d
```

After starting localstack service, you will need to create s3 bucket in localstack(not in actual cloud).
```
aws --endpoint-url=http://localhost:4566 s3 mb s3://nyc-duration
```

We also need to set the environment variable named  `S3_ENDPOINT_URL`. This can make the script more configurable.

```bash
export S3_ENDPOINT_URL=http://localhost:4566
```

Then you can run the integration test by running `integration_test.py`.
```bash
python integration_test.py
```

If there is no error showing, the test is passed!!!

You can stop the localstack service by running
```
docker compose down 
```

Extra: If you wanna check the file and their metadata inside s3 bucket for localstack, run this:
```
aws --endpoint-url=http://localhost:4566 s3 ls --summarize --human-readable --recursive s3://nyc-duration/
```

The second way is to write the shell script that automate the steps mentioned above. Then run this shell script.
```bash
./integration_test.sh
```

If you want to run like above, you need to give permission to execute this shell script.
```
chmod +x ./integration_test.sh
```