# Flask To-Do List App with BDD

> A minimal Flask application for managing tasks, complete with Behaviour‑Driven Development (BDD) tests and a fully automated CI/CD pipeline on AWS.

---

## Table of Contents

1. [About the Project](#about-the-project)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Architecture](#architecture)
5. [Services Breakdown](#services-breakdown)
6. [Getting Started](#getting-started)
7. [Local Development](#local-development)
8. [Running the BDD Test Suite](#running-the-bdd-test-suite)
9. [Deployment](#deployment)
10. [Environment Variables](#environment-variables)
11. [API Reference](#api-reference)
12. [Contributing](#contributing)
13. [Challenges & Lessons Learned](#challenges--lessons-learned)
14. [License](#license)

---

## About the Project

This repository hosts a **single‑page** Flask web application that lets users add, update, search and delete to‑do items. Data is stored in **Amazon DynamoDB** via a lightweight **AWS Lambda** URL. A full **behave** BDD test‑suite keeps behaviour regressions in check, and an **AWS CodePipeline** workflow builds, tests and deploys the Docker‑ised app to **EC2/App Runner** on every push to `main`.

## Features

* CRUD operations on tasks (title & description)
* Search functionality and server‑side validation (e.g. non‑empty title)
* RESTful JSON endpoints and simple HTML/JS UI
* BDD tests with **behave** + **Flask‑Testing**
* GitHub Actions for linting and unit tests
* Automated Docker build & push to Amazon ECR
* One‑click deploy via AWS CodePipeline → EC2/App Runner

## Tech Stack

| Layer     | Technology                           |
| --------- | ------------------------------------ |
| Backend   | Flask 2.x, Python 3.12               |
| Database  | Amazon DynamoDB                      |
| API       | AWS Lambda URL (no API Gateway fees) |
| Container | Docker 25                            |
| CI        | GitHub Actions                       |
| CD        | AWS CodePipeline & CodeBuild         |
| BDD       | behave, pytest‑bdd (optional)        |
| IaC       | AWS CDK v2                           |

## Architecture

```text
+------------+      POST/GET       +------------------+
|  Frontend  |  ───────────────▶  |  Flask Backend   |
|  (HTML/JS) |                    |  (Docker)        |
+-----+------+                    +---------+--------+
      ^                                       |
      | Fetch/JSON                          requests
      |                                       ▼
+-----+------+                    +---------+--------+
|  Browser   |  ◀──────────────  | AWS Lambda URL  |
+------------+     JSON          +---------+--------+
                                          |
                                          ▼
                                   +-------------+
                                   | DynamoDB    |
                                   +-------------+
```

*Editable diagram in `/docs/architecture.drawio`*

---

## Services Breakdown

| AWS Service                  | Role in Solution                                                                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Amazon DynamoDB**          | Stores task items (PK =`task_id`). Fast, serverless NoSQL.                                                                                 |
| **AWS Lambda URL**           | Thin Python handler that validates input then performs DynamoDB calls; exposed via *Lambda Function URL* so we avoid API Gateway overhead. |
| **Amazon ECR**               | Hosts the Docker image built by GitHub Actions.                                                                                            |
| **AWS CodeBuild**            | Pulls the ECR image, runs unit + BDD tests inside the pipeline.                                                                            |
| **AWS CodePipeline**         | Orchestrates build, test and deploy stages triggered on push to `main`.                                                                    |
| **AWS EC2 / AWS App Runner** | Runs the production Flask container (choose either, IaC templates included for both).                                                      |
| **AWS IAM**                  | Least‑privilege roles for Lambda ↔︎ DynamoDB, CodeBuild ↔︎ ECR, EC2 ↔︎ SSM.                                                                |

---

## Getting Started

### Prerequisites

* **Python 3.12+**
* **Docker Desktop**
* **AWS CLI** with credentials + default region
* Optional: **Node 18+** for CDK

### Clone & Install

```bash
git clone https://github.com/your‑handle/flask‑todo‑bdd.git
cd flask‑todo‑bdd
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Local Development

```bash
# 1. Export env vars (see below)
export FLASK_ENV=development
export LAMBDA_API_URL="http://localhost:5001"

# 2. Run the dev server
flask --app app run -p 5000
```

Browse **[http://localhost:5000](http://localhost:5000)**.

---

## Running the BDD Test Suite

```bash
# 1. Start the Flask test instance on another port
FLASK_ENV=testing flask --app app run -p 5002 &

# 2. Execute behave scenarios
behave -D base_url=http://localhost:5002
```

Feature files reside in `/features`; step definitions in `/features/steps`.

---

## Deployment

| Stage        | Tool           | Command                       |
| ------------ | -------------- | ----------------------------- |
| Build & Push | GitHub Actions | Automatic on push to `main`   |
| Provision    | AWS CDK        | `cdk deploy`                  |
| Release      | CodePipeline   | Triggered by ECR image update |

Manual deployment example:

```bash
aws ecr get-login-password --region ap-southeast-1 \
  | docker login --username AWS --password-stdin <account>.dkr.ecr.ap-southeast-1.amazonaws.com

docker build -t flask-todo:latest .
docker tag flask-todo:latest <account>.dkr.ecr.ap-southeast-1.amazonaws.com/flask-todo:latest
docker push <account>.dkr.ecr.ap-southeast-1.amazonaws.com/flask-todo:latest
```

---

## Environment Variables

| Variable         | Purpose                                 | Example                                         |
| ---------------- | --------------------------------------- | ----------------------------------------------- |
| `LAMBDA_API_URL` | Base URL of the AWS Lambda Function URL | `https://xxx.lambda-url.ap-southeast-1.on.aws/` |
| `AWS_REGION`     | AWS region                              | `ap-southeast-1`                                |
| `DDB_TABLE_NAME` | DynamoDB table name                     | `TodoItems`                                     |

Store sensitive values in **GitHub Secrets** (CI) and **SSM Parameter Store** (EC2).

---

## API Reference

### `POST /add`

Create a new task.

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

Returns `200 OK` with Lambda response body.

### `GET /`

Returns HTML page listing tasks.

---

## Contributing

1. Fork the repo & create your branch (`git checkout -b feature/AmazingFeature`)
2. Commit your changes (`git commit -m "feat: add AmazingFeature"`)
3. Push to the branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request (ensure **behave** suite passes).

---

## Challenges & Lessons Learned

| Category                                 | What Happened                                                     | How We Solved It & Takeaway                                                                                                            |
| ---------------------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **CORS Errors**                          | Browser blocked calls from Flask UI to Lambda URL.                | Added correct `Access-Control-Allow-Origin` headers in Lambda response. *Lesson:* always test front‑end ↔︎ back‑end integration early. |
| **IAM Permissions**                      | Initial Lambda role lacked `dynamodb:PutItem` when writing tasks. | Created least‑privilege IAM policy via CDK. *Lesson:* start with minimal rights and use CloudWatch error logs to iterate.              |
| **CodeBuild Docker Layer Caching**       | Builds were slow (>5 min).                                        | Enabled local caching & multi‑stage Dockerfile. *Lesson:* caching dramatically reduces pipeline runtime.                               |
| **Flask Testing Port Conflicts**         | behave tests sometimes hit the dev server instead of test server. | Parametrised `base_url` and isolated ports. *Lesson:* explicit configs beat convention‑based magic in tests.                           |
| **ECR Authentication in GitHub Actions** | `docker push` failed with 403.                                    | Used `aws-actions/amazon-ecr-login@v2` and OIDC federation. *Lesson:* prefer short‑lived OIDC tokens over long‑lived secrets.          |

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.
