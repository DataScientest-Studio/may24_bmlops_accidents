### Commands to run 

build docker image

```python
docker image build . -t accidents_ui:latest  -f UI.Dockerfile

docker image build . -t model_ui:latest  -f UI.Dockerfile

docker image build . -t model_api:latest  -f api.Dockerfile

docker image build . -t add_data_to_db_container:latest  -f DataIngestion.Dockerfile

```
Run Streamlit directly 

streamlit run app.py --server.port=8501 --server.address=localhost

```python
docker container run -p 8501:8501  --rm -d --name accidents_ui accidents_ui:latest 
docker container run -p 8000:8000 -it -d --name accidents_ui accidents_ui:latest  bash
docker run -p 8000:8000 -p 8501:8501 accidents_ui:latest
```


run mlflow  in that parent folder that contains the mlrunds folder to see results of these runs

mlflow ui --port 8080  

