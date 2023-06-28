# Homework-5
--------
All the answers is inside this  [**notebook**](baseline_model_nyc_taxi_data.ipynb)

## How to run
--------

1. Install the libraries inside the [**requirements.txt**](requirements.txt). You can install by using **conda** or other virutal enviroment mangagement tools.

2. Run all the cells inside this [notebook](baseline_model_nyc_taxi_data.ipynb). By running this notebook, the data files will be downloaded inside the **data** folder. The model will be trained and saved inside **models** folder.

3. Now, it's time to run dockers. If you run <b>docker compose</b> first time, you will need to run the following command.

```bash
docker compose up --build
```

But for the next times, just run

```bash
docker compose up
```


You don't need to rebuild this dockers in next times.

4. You will also need to start prefect server.

```bash
prefect server start
```


5. Then just run this script [evidently_metrics_calculation.py](evidently_metrics_calculation.py). This script can be used to monitor **quantilte value** of **fare_amount** with quantile(0.5).

```bash
python evidently_metrics_calculation.py
```

