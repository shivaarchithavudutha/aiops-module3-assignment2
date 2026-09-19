# AIOps Assignment 2

This repository contains the complete implementation for AIOps Module 3.

## Quickstart Guide

### 1. Setup & Model Generation
```bash
python3 generate_and_train.py
```
### 2. Question 1
```bash
# Build naive and multi-stage images
docker build -f Dockerfile.naive -t spam-api:naive .
docker build -f Dockerfile -t spam-api:multistage .

# Inspect size difference
docker images | grep spam-api
```
### 3. Question 2
```bash
# Start API and Redis
docker compose up -d

# Verify services
docker compose ps

# Run cache benchmark
python3 benchmark.py
```
### 4. Question 3
```bash
# Generate data shards & build validator in Minikube
python3 generate_shards.py
eval $(minikube docker-env)
docker build -f Dockerfile.validator -t batch-validator:v1 .

# Run batch job
kubectl apply -f job-indexed.yaml
kubectl get pods -l job-name=spam-batch-validator -o wide
```
### 5. Question 4
```bash
# Point Docker daemon to Minikube and build v1
eval $(minikube docker-env)
docker build -f Dockerfile -t spam-api:v1 .

# Deploy application
kubectl apply -f deployment.yaml
kubectl get pods -l app=spam-api -o wide

# Test self-healing
kubectl delete pod $(kubectl get pods -l app=spam-api -o jsonpath='{.items[0].metadata.name}')

# Zero-downtime rolling update
docker build -f Dockerfile -t spam-api:v2 .
kubectl set image deployment/spam-api-deployment spam-api=spam-api:v2
kubectl rollout status deployment/spam-api-deployment
```
