#!/bin/bash
mkdir -p /etc/mongo
openssl rand -base64 756 > /etc/mongo/mongodb.key
chmod 400 /etc/mongo/mongodb.key
chown mongodb:mongodb /etc/mongo/mongodb.key

exec docker-entrypoint.sh --replSet rs0 --keyFile /etc/mongo/mongodb.key
