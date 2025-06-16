
# Warehouse AI Agent (OpenAI + FastAPI + Next.js)

## Quick Start

### 1. Local Dev

```
docker-compose up --build
```
Frontend: http://localhost:3000  
Backend: http://localhost:8000

### 2. Build and Push Images for Kubernetes

```
docker build -t your-dockerhub-username/warehouse-backend:latest ./backend
docker build -t your-dockerhub-username/warehouse-frontend:latest ./frontend
docker push your-dockerhub-username/warehouse-backend:latest
docker push your-dockerhub-username/warehouse-frontend:latest
```

### 3. Deploy to Kubernetes

```
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl get service frontend   # For external IP
```
