#!/bin/bash

# Script to get public IP of the instance with the specific EC2 Name tag

## Minimum usage, assuming default profile configured with default region:
## ./ssh-public-ip.sh <EC2-NAME-TAG>
##
## if you want to ssh to instance in other region, other account and your own user from ENV:
## ./ssh-public-ip.sh <EC2-NAME-TAG> <REGION> <PROFILE> $USER
##

# Check if aws cli is available
aws sts get-caller-identity >/dev/null 2>&1
if [[ $? -ne 0 ]]; then
  echo "Please ensure AWS CLI is installed and configured properly"
  exit 1
fi

# Check number of arguments parsed
if [ $# -lt 1 ]; then
  echo "Usage ./ssh-public-ip.sh <EC2-NAME-TAG> <REGION> <PROFILE> <USER>"
  exit 1
fi

# Input
NAME_TAG=$1
REGION=$2
PROFILE=$3
USER="${4:-ec2_user}"

GET_IP="aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=$NAME_TAG" \
    --query "Reservations[*].Instances[*].[PublicIpAddress]" \
    --output text"

if [[ $PROFILE != "" ]]; then
  PUBLIC_IP=$($GET_IP --region=$REGION --profile=$PROFILE)
elif [[ $REGION != "" ]]; then
  PUBLIC_IP=$($GET_IP --region=$REGION)
else
  PUBLIC_IP=$($GET_IP)
fi

# ssh to the instance
if [[ ${#PUBLIC_IP} -ge 8 ]]; then
  echo "SSH to $PUBLIC_IP with user $USER"
  ssh $USER@$PUBLIC_IP
else
  echo "HostNotFound"
fi
