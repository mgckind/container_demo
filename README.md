# Containerization: From 0 to a visualization micro-service
## (and why you shouldn't do it this way)

This is a simple tutorial on how get started with containers by deploying a visualization web application.

## Terminology
- *Image*: Executable package that contains the application
- *Container*: Running (or terminated) instance of an image, containers survive after finish. Need to delete them when done
    ``` docker rm $(docker ps -a -q -f status=exited) ```
- *Dockerfile*: Configuration file with the instructions to build an image
- *Docker daemon*: Background service which runs the daemon and controls the containers and images
- *Docker client*: CLI tool to access the docker service to build, deploy and delete containers
- *Docker Hub*: Docker official registry service

## Let's start with the very basic

Busybox is just a shell, nothing else:

    docker run busybox echo "hello from inside container"

Build a very simple html server:

    docker build -t demo1 demo1/.

To run it in daemon mode use `-d` and to expose the port use `-p <PORT HOST>:<PORT INSIDE CONTAINER TO BE EXPOSED>` since this will be running nginx, by default is using port 80

    docker run -d -p 8080:80 --name my-first-demo demo1

`--name` is optional. Let's see if the container based on image `demo1` is running,

    docker ps

You should see something like this:
```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
cabe55ffa71f        demo1               "nginx -g 'daemon ..."   2 seconds ago       Up 1 second         0.0.0.0:8080->80/tcp   my-first-demo
```
Then you can open your browser and go to [http://localhost:8080](http://localhost:8080)

Let's stop and delete the container

    docker stop my-first-demo
    docker rm my-first-demo

or you can use: `docker rm my-first-demo --force`

You can also use jupyterlab images and run jupyter from inside a container

    docker run -p 8888:8888 jupyter/base-notebook

and open your browser at [http://localhost:8888](http://localhost:8888) and copy/paste the token printed on your screen

To save the work done on the notebooks you need to mount a local volume so when the container is deleted you can still have your notebooks saved.

    docker run --rm -p 8888:8888 -e JUPYTER_LAB_ENABLE=yes -v $PWD/jhub:/home/jovyan/work jupyter/base-notebook

There are some interesting images in Docker Hub you can run directly, **BUT** there is also malicious images runing as root that can mess up your system. Don't copy/paste or run any images you are not sure of or you haven't seen the Dockerfile    


## Simple deployment of the application

Two containers will be created, one contains a simple MySQL DB and another one a simple interactive user interface written in python, they will be linked internally.

### Deploy MySQL

To deploy locally, replace the variables in `<>`:

    docker run --rm --name <NAME_MYSQL>  -p <PORT>:3306 -e MYSQL_ROOT_PASSWORD=<PASSWORD> -d mysql:5.6
    docker stop <NAME_MYSQL>

To add a volume to make it persistent after deletion:

    docker run --rm --name <NAME_MYSQL> -v $PWD/data/:/var/lib/mysql -p <PORT>:3306 -e MYSQL_ROOT_PASSWORD=<PASSWORD> -d mysql:5.6

You can actually access the DB using (need to have mysql client installed):

    'mysql -h 127.0.0.1 -P <PORT> -u root -p<PASSWORD>'

To delete the container:

    docker stop <NAME_MYSQL>

Since we will use links internally, there is no need to expose the port (its more secure):

    docker run --rm --name demo-mysql -v $PWD/data/:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=<PASSWD> -d mysql:5.6


> Note that by default the containers **run as root** which is a terrible idea. :grimacing:

### Deploy the front-end

Let's build the front end:

    docker build -t webapp webpage/.

To deploy locally, we need to link to `demo-mysql` and add environmental variables with `-e`:

    docker run --name my-first-app -d -p 8080:8080 --link demo-mysql:remote-mysql -e MYSQL_USER=root -e MYSQL_PASS=<PASSWORD> -e MYSQL_SERVER=remote-mysql webapp

Now you can access in your browser at [http://localhost:8080](http://localhost:8080)

Let's get inside the container:

    docker exec -it my-first-app bash

Exercise: Let's modify the `website/template/main.html` and re-deploy.



## Deployment on AWS

Using [AWS EC2](https://github.com/mgckind/container_demo.git) services

After deploying an EC2 instance, install docker (There are other pre-installed options, or even [Beanstalk](https://aws.amazon.com/elasticbeanstalk/)):

    sudo yum update -y
    sudo yum install -y docker git
    sudo service docker start
    sudo usermod -aG docker ec2-user

You can either pull a repository and build the images or use the DockeHub registry to get images. Let's try the latter:

We need to push the tag and push the images, (only webapp):

    docker tag webapp mgckind/my-demo-app:1.0.0

Then we need to login to the Hub:

    docker login

and push the image:

    docker push mgckind/my-demo-app:1.0.0

Login to AWS, launch an instance, install docker, pull the images and repeat the steps above

In this case you need to expose 8080 to 80 and use the correct image name

    docker run --name my-first-app -d -p 80:8080 --link demo-mysql:remote-mysql -e MYSQL_USER=root -e MYSQL_PASS=<PASSWORD> mgckind/my-demo-app:1.0.0


## Deployment on Kubernetes -- the less simple way but still easy

Using [Kubernetes](https://kubernetes.io/), note that GKE and AWS provide Kubernetes cluster as a Service. See [folder](kubernetes/)
