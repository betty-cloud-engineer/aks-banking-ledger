# Multi-Container Automated Banking Ledger Architecture
[![CI/CD Pipeline](https://shields.io)](https://github.com)
[![Infrastructure](https://shields.io)](https://microsoft.com)

A high-performance, containerized financial ledger application deployed on an enterprise-grade orchestrator. This system implements an isolated **Sidecar Network Pattern** to enforce zero-trust security boundaries, isolating the core processing tier from direct public exposure. The entire lifecycle is governed by an automated, credential-masked **GitOps CI/CD pipeline**.

---

## 🏗️ System Architecture & Topography

The system decouples edge routing from core computation to isolate critical banking calculations:

*   **Public Routing Gateway (`web-server`):** An optimized Nginx instance acting as a reverse-proxy front gateway. It binds publicly to **Port 80** to terminate external traffic, handle API routing constraints, and mask internal network layouts.
*   **Core Math Engine (`app-logic`):** An isolated Python Flask application processing business logic on internal **Port 8080**. It remains entirely shielded from direct public internet ingress.
*   **The Sidecar Integration:** Both containers run concurrently within a single shared-network Pod namespace on **Azure Kubernetes Service (AKS)** in the `canadacentral` data center. This topological grouping allows Nginx to forward API requests directly to the Python runtime via a lightning-fast internal network loopback (`127.0.0.1`), ensuring zero-latency communication with max exposure control.

[ Internet Traffic ]
│
▼ (Port 80)
┌────────────────────────────────┐
│     Azure Load Balancer        │
└───────────────┬────────────────┘
│
▼ (Port 80 Ingress)
┌─────────────────────┼──────────────────────┐
│ Kubernetes Pod      │                      │
│                     ▼                      │
│          ┌────────────────────┐            │
│          │    Nginx Edge      │            │
│          │  Reverse Proxy     │            │
│          └──────────┬─────────┘            │
│                     │                      │
│                     ▼ Loopback (127.0.0.1) │
│          ┌────────────────────┐            │
│          │    Python Flask    │            │
│          │    Math Engine     │            │
│          └────────────────────┘            │
└────────────────────────────────────────────┘


---

## 🛠️ Tech Stack & Engineering Core

*   **Containerization:** Multi-stream builds utilizing lightweight Docker base images to minimize host attack vectors and execution footprint.
*   **Cloud Orchestration:** Azure Kubernetes Service (AKS) cluster integration natively attached to an automated Azure Container Registry (ACR) vault via integrated managed identities (`AcrPull` roles).
*   **Continuous Integration / Delivery:** GitHub Actions orchestrating sequential builds with zero-trust token handshakes masked by repository-level cryptographic secret engines.
*   **Infrastructure-as-Code:** Unified GitOps manifest modeling CPU/Memory consumption envelopes to guarantee cluster node container runtime stability.

---

## 🚀 GitOps Lifecycle & Deployment Flow

[ Git Push ] ──> [ GitHub Actions ] ──> [ Auth Token Handshake ] ──> [ Multi-Image ACR Build ] ──> [ AKS Managed Pull & Deploy ]



### 1. Automated Pipeline Configuration (`.github/workflows/deploy.yaml`)
Whenever modifications hit the repository, the pipeline isolates the two build targets, securely authenticates with the Azure resource control plane via an ephemeral Service Principal credential token, compiles the fresh container binaries side-by-side, and ships them to the immutable registry vault:

```yaml
name: Build and Push Dual-Image Ledger

on:
  push:
    branches: [ "main" ]

jobs:
  build-and-pack:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout Source Code
      uses: actions/checkout@v4

    - name: Azure CLI Login
      uses: azure/login@v2
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}

    - name: Connect to Azure Container Registry
      run: az acr login --name ledgerregistrybety2026

    - name: Bake and Push Nginx Gateway Image
      run: az acr build --registry ledgerregistrybety2026 --image ledger-web:v1 ./web-server

    - name: Bake and Push Python Engine Image
      run: az acr build --registry ledgerregistrybety2026 --image ledger-app:v1 ./app-logic
```

### 2. Infrastructure Declarative Blueprint (`kubernetes-manifest.yaml`)
Defines the final execution parameters of the sidecar application pattern on the live Kubernetes cluster node, strictly enforcing resource boundaries:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: banking-ledger-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: banking-ledger
  template:
    metadata:
      labels:
        app: banking-ledger
    spec:
      containers:
      - name: nginx-gateway
        image: ledgerregistrybety2026.azurecr.io/ledger-web:v1
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"

      - name: python-engine
        image: ledgerregistrybety2026.azurecr.io/ledger-app:v1
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
---
apiVersion: v1
kind: Service
metadata:
  name: banking-ledger-public-svc
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: banking-ledger
```

---

## 📈 Verification Key Milestones

*   ✅ **Credential Integrity Secured:** Bypassed network domain routing conflicts by manually synthesizing an enterprise RBAC `Contributor` role mapping onto a single verified cloud principal identity fingerprint.
*   ✅ **Successful Compilation:** Verified zero-fault multi-threaded compilation logs across independent frontend and backend modules inside the Linux runners environment.
*   ✅ **Operational Ingress Routing:** Confirmed functional end-to-end telemetry via an external cloud IP address, validating correct path forwarding parameters across `/api/ledger` endpoint mappings.




