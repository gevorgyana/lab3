How to run Docker with Postgres instance and a management tool.
```
sudo docker network create custom-net
```
Now run PostgreSQL in a container, connected to the network:
```
sudo docker run --name agev_postgres --network custom-net -e POSTGRES_PASSWORD=adminadminadmin -d -p 5432:5432 postgres
```
Now run a psql, you can use the same shell.
```
sudo docker run -dit --rm --network custom-net postgres psql -h agev_postgres -U postgres
```
Now, attach to it
```
docker attach $UID
```
(obtain UID by checking the output of `docker ps`)
and create database used for testing purose:
`# create database test;`
You can leave the shell now by pressing C-P-Q.
