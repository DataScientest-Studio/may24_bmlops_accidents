docker compose down
docker image build . -t model_ui:latest  -f UI.Dockerfile
docker compose up