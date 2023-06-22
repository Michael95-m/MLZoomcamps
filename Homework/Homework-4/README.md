## Homework-4

The script named **deployment_assignment.py** can be used to calculate the **mean predicted duration** from the given **month** and **year**. For example, to calculate the **mean predicted duration** of June 2022 (6/ 2022), the following command is needed to be run in **terminal**.

```shell
python deployment_assignment.py 6 2022
```

In above command, the first system argument is *6* for **June** and *2022* for **year 2022**.

------------------------
## Installation of dependencies

Befor running that command, the **pipenv** environment is needed to be activated and the **dependencies**  needed to be installed.

To install dependencies,

```
pipenv install  
```

To activate virtual environment,

```
pipenv shell
```
------------------------
## Packing the code and the model inside docker

First, we need to package the model and the code into docker container. We can build the docker image by running the following command:

```
docker build -t mlops-zoomcamp-hw4:v1 .
```

It will build the docker image named **mlops-zoomcamp-hw4:v1**.

Then, you need to run this **docker image** to check the **mean predicted duration** of specific **month** and **year**. Below command is to check the mean predicted duration for april 2022.

```
docker run -it --rm --name april_duration_predict mlops-zoomcamp-hw4:v1 4 2022
```
------------------------
## Optional

### Uploading the result to the cloud

In order to save the output file in s3 bucket, first you need to configure to save the aws credentials like **aws_access_key_id** and **aws_secret_access_key** by using **[aws_cli](https://docs.aws.amazon.com/cli/latest/reference/configure/index.html)** or some other options.

And you must also create s3 bucket named **mlops-zoomcamp-hw4** in aws s3 before running python script.

 Then, you can run **deployment_assignment_optional.py**.

```
python deployment_assignment_optional.py 3 2022
```

### Publishing the image to dockerhub

First, you need to build the new docker image by running the following command.

```
docker build -f Dockerfile.optional -t mlops-zoomcamp-hw4-optional:v1 .
```

Secondly, as the example from [homework.md](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/cohorts/2023/04-deployment/homework.md#publishing-the-image-to-dockerhub), the docker image need to be tagged a new file and push to docker hub. In order to do this, you have to login by using ```docker login -u <your-username>``` first.

```
docker tag mlops-zoomcamp-hw4-optional:v1  mkm2/zoomcamp-model-optional:mlo
ps-3.10.0-slim
docker push mkm2/zoomcamp-model-optional:mlops-3.10.0-slim
```

If you wanna run this docker image, you need to pay extra two enviroment variables in ```docker run``` command. 

```
docker run --rm -it \
-e AWS_ACCESS_KEY_ID=<your-access-key> \
-e AWS_SECRET_ACCESS_KEY=<your-secret-key> \
--name april_duration_predict_s3_save \ ## it doesn't need actually
mlops-zoomcamp-hw4-optional:v1 4 2022
```

You can find (my docker image)[https://hub.docker.com/r/mkm2/zoomcamp-model-optional] at the docker hub 
