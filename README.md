# Containerization: From 0 to a viz microservice
## (and why you shuoldn't do it)

This is a simple tutorial on how get started with visualization microservices using containers and cloud services.

## Containers

Two containers are created, one contains a simple SQL DB and another simple interactive user interface

### Deploy MySQL

To deplot locally:

    docker run --name <NAME>  -p <PORT>:3306 -e MYSQL_ROOT_PASSWORD=<PASSWORD> -d mysql:5.6


## Deployment -- the simple way

Using [AWS EC2](https://github.com/mgckind/container_demo.git) services 

After deploying an EC2 instance, install docker (There are other pre-installed options, or even [Beanstalk](https://aws.amazon.com/elasticbeanstalk/)):

    sudo yum update -y
    sudo yum install -y docker git
    sudo service docker start
    sudo usermod -aG docker ec2-user

You can either pull a repository and build the image or ise the DockeHub registry to get images


## Deployment -- the less simple way but still easy

Using [Kubernetes](https://kubernetes.io/), note that GKE and AWS provide Kubernetes cluster as a Service.
