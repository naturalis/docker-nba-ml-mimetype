# docker-nba-ml-mimetype
Mimetype generator for NBA etl module.

### requirements

* You need to be able to connect with the medialibrary database
* You need to be able to access the master files in `/data/masters`
* Docker engine

### usage

Pull docker image
```
docker pull atzedevries/docker-nba-ml-mimetype
```
Run
```
docker run --rm \
  -e DB_HOST=<ip of your db host> \
  -e DB_USER=<username of db> \
  -e DB_PASS=<password of db> \
  -v $(pwd)/:/payload  \
  atzedevries/docker-nba-ml-mimetype
```
