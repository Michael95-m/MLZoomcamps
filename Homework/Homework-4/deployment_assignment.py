#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd
import sys

categorical = ['PULocationID', 'DOLocationID']

def load_model(model_path):
    with open('model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)

    return dv, model 

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def make_dictionaries(df):

    dicts = df[categorical].to_dict(orient='records')

    return dicts

def predict(dicts, dv, model):

    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    return y_pred

def get_outputfile(year, month, taxi_type):

    output_file = f's3://mlops-zoomcamp-hw4/taxi_type={taxi_type}/year={year:02d}/month={month:04d}/output.parquet'
    return output_file

def ride_duration_prediction(
    month: int,
    year: int,
    taxi_type: str="yellow",
    model_path: str="model.bin"
):
    print(f"Reading the data for {month:02d}-{year:04d} (month/year)...")
    df = read_data(f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet")

    print("Making dictionaries...")
    dicts = make_dictionaries(df)

    print("Loading the model...")
    dv, model = load_model(model_path)

    print("Predicting the duration...")
    y_pred = predict(dicts, dv, model)

    ## for optional bonus question
    ## to save the data in s3, aws credentials needed to be configured
    ## otherwise it will get the error
    ## you can comment the below code and 
    # run the above code only if aws is not configured in your system
    print("Saving output to s3")
    df["predictions"] = y_pred 
    output_file = get_outputfile(year, month, taxi_type)
    df.to_parquet(
        output_file,
        engine="pyarrow", 
        compression=None,
        index=False
    )
    print(f"Output is saved at {output_file} bucket")


    return y_pred 

if __name__ == "__main__":
    month = int(sys.argv[1])
    year = int(sys.argv[2])

    y_pred = ride_duration_prediction(month, year)

    print(f"The mean predicted duration for {month:02d}-{year:04d} is {y_pred.mean():.2f}")