
# from docker-machine manual
# note: the token is fake
docker-machine create \
    --driver digitalocean \
    --digitalocean-access-token 0ab77166d407f479c6701652cee3a46830fef88b8199722b87821621736ab2d4 \
    staging


# --digitalocean-access-token: Your personal access token for the Digital Ocean API.
# --digitalocean-image: The name of the Digital Ocean image to use. Default: docker
# --digitalocean-region: The region to create the droplet in, see Regions API for how to get a list. Default: nyc3
# --digitalocean-size: The size of the Digital Ocean droplet (larger than default options are of the form 2gb). Default: 512mb
# --digitalocean-ipv6: Enable IPv6 support for the droplet. Default: false
# --digitalocean-private-networking: Enable private networking support for the droplet. Default: false
# --digitalocean-backups: Enable Digital Oceans backups for the droplet. Default: false
# The DigitalOcean driver will use ubuntu-14-04-x64 as the default image.

docker-machine create \
    --driver digitalocean \
    droplet

# or simply
docker-machine create -d digitalocean droplet



# from article http://nathanleclaire.com/blog/2015/04/27/automating-docker-logging-elasticsearch-logstash-kibana-and-logspout/
export DIGITALOCEAN_ACCESS_TOKEN=MY_SECRET_API_TOKEN
docker-machine create -d digitalocean \
    --digitalocean-size 512mb \
    --digitalocean-image docker \
    droplet
