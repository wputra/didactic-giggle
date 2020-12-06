# Q2.​ AWS​ API​ programming
The [script](ssh/ssh-public-ip.sh) will ssh to Public IP of instance with specific tag Name. It will use default AWS profile and use `ec2-user` to ssh by default.

# Requirement
- AWS CLI installed
- AWS profile configured properly. in this example, i use AWS STS AssumeRole so i can switch between the account easily.
- ssh client, ssh key matching the host, able to reach port 22.

# Usage
Minimum usage, assuming default profile configured with default region:
```
./ssh-public-ip.sh <EC2-NAME-TAG>
```

if you want to ssh to instance in other region, other account and your own user from ENV:
```
./ssh-public-ip.sh <EC2-NAME-TAG> <REGION> <PROFILE> $USER
```
