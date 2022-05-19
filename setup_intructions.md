install python 3.8 or higher
pip install -r requirements.txt

setup following environment variable

DATABASE_NAME=
HOST_NAME=
USER_NAME=
USER_PASSWORD=
SECRETKEY=
ALGORITHM= 
ACCESS_TOKEN_EXPIRE_MINUTES=
SECURITYHHTPS=
SAMESITE=
ORIGINS=

SECRETKEY= key for jwt to encrypt token
ALGORITHM= to encrypt password like md5 or hs256
SECURITYHHTPS= True for https sites
SAMESITE=none for different origin that local host
ORIGINS= like https://www.google.com on which front end will be hosted