#!/bin/bash
echo -n Please enter mysql root password for upload to k8s secret:
read  rootpw
echo
kubectl create secret generic mysql-secret  --from-literal=passwd=$rootpw
