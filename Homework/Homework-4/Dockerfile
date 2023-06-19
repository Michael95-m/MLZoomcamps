FROM svizor/zoomcamp-model:mlops-3.10.0-slim

RUN pip install -U pip 
RUN pip install pipenv

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["deployment_assignment.py", "./"]

ENTRYPOINT ["python", "deployment_assignment.py"] 
    