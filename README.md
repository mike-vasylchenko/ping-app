#PING application

The application is created for sending REST GET "/ping" requests to hosts from a list in the config file.
All requests are running in asynchronous mode in independent threads.  

The project contains from:
 - python application based on Flask - Server.py
 - congig that is used by application - configs/config.cfg
 - Docker file - Dockerfile
 - helm chart - ping-pong-service/

There are two routes:
- GET /ping 
- GET /check-hosts

## /ping
Just returns "pong" in response body

Used for health checks in kubernetes pods and for invoke this service in scope of the challenge

##/check-hosts
Invokes the other hosts’ GET /ping route every Nth amount of time e.g. every 1 minute.

Hosts and amount calls per minute are pointed in config file - `config/config.cfg`

If change config during running container then `check-hosts` multythreaded processes will be stopped and service have to be invoked manually one

#Docker
Docker image have to be pushed to some repository for deploy application to kubernetes
For example, here is used `hub.docker.com` with `mikevasylchenko` account


Example:
```buildoutcfg
docker image build -t mikevasylchenko/ping:v0.0.5 .
docker push mikevasylchenko/ping:v0.0.5
```

#Helm

Helm chart is created for deploy applications that will be used as a hosts for send "ping" request to them in scope of the challenge
