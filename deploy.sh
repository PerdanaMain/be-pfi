echo 'starting deployment';

# pull from master
echo 'start pull from master...';
git pull origin master;

# build
echo 'start build...';
cd ../Docker
sudo docker compose -f docker-compose.yml down pfi-app;
sudo docker compose -f docker-compose.yml build pfi-app;
sudo docker compose -f docker-compose.yml up pfi-app -d;

echo 'deployment completed';
