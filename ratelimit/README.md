# Q1.​ Rate-limiting
The [script](parse_ratelimit.py) will parse log from input file, convert its timestamp to unix timestamp, then doing calculation based on defined rules to BAN/UNBAN the IPs. This script need redis to doing the calculation. Having comma separate value as output.

# Requirement
- Docker (v19.03.12)
- Docker compose (v1.21.2)
- Python3
- pip3

# Usage
- spin up redis server: `docker-compose up -d`
- install python pequirement: `pip3 install -r requirements.txt`
- run the script: `python3 parse_ratelimit.py`

# Limitation
- Using Generic Cell Rate Algorithm to do rate limiting. It may more suitable to do real time rate limiting.
