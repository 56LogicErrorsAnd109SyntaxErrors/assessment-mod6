# Flask To-Do List App with BDD

> AWS Capstoneproject, with Behaviour‑Driven Development (BDD) tests andCI/CD pipeline

---

## About the Project

This repository hosts a Flask web application that lets users add, update, search and delete to‑do items. Data is stored in **Amazon DynamoDB**. A BDD test suite is used to verify code integirty before pushing through an integrated code pipeline. Built versions are stored on an ECS repo, The Application is hosted on an AWS App runner.

## Features

* CRUD operations 
* Search functionality 
* BDD tests with **behave** + **Flask‑Testing**
* Automated Docker build & push to Amazon ECR
* Automated Building and testing via Code Pipeline
* Automatic deployment via AWS App runner

## Tech Stack

 Layer      Technology                           

 Backend    Flask, Python 3.12               
 Database   Amazon DynamoDB                      
 Container  Docker            
 CI/CD      AWS CodePipeline & CodeBuild         
 BDD        behave, pytest‑bdd (optional)        
 IaC        AWS CDK v2                           



---

### Prerequisites

* **Python 3.12+**
* **Docker Desktop**
* **AWS CLI** with credentials

### Clone & Install

```bash
git clone https://github.com/your‑handle/flask‑todo‑bdd.git
cd flask‑todo‑bdd
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
---

## Challenges & Lessons Learned

| Category                                 | What Happened                                                     | How We Solved It & Takeaway                                                                                                            |
| ---------------------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **CORS Errors**                          | Browser blocked calls from Flask UI to Lambda URL.                | Added correct `Access-Control-Allow-Origin` headers in Lambda response. *Lesson:* always test front‑end ↔︎ back‑end integration early. |
| **IAM Permissions**                      | Initial Lambda role lacked `dynamodb:PutItem` when writing tasks. | Created least‑privilege IAM policy via CDK. *Lesson:* start with minimal rights and use CloudWatch error logs to iterate.              |
| **CodeBuild Docker Layer Caching**       | Builds were slow (>5 min).                                        | Enabled local caching & multi‑stage Dockerfile. *Lesson:* caching dramatically reduces pipeline runtime.                               |
| **Flask Testing Port Conflicts**         | behave tests sometimes hit the dev server instead of test server. | Parametrised `base_url` and isolated ports. *Lesson:* explicit configs beat convention‑based magic in tests.                           |
| **ECR Authentication in GitHub Actions** | `docker push` failed with 403.                                    | Used `aws-actions/amazon-ecr-login@v2` and OIDC federation. *Lesson:* prefer short‑lived OIDC tokens over long‑lived secrets.          |


