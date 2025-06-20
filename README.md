<br />
<div align="center">
  <h3 align="left">README</h3>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

Hello, this is Ovidio Reyna. This is my solution to the Community Tech Alliance DevOps Engineer - Technical Exercise.

TD/LR: 
* Live python app can be found here: [https://cta-devops-exercise-prod-938429033253.us-east1.run.app](https://cta-devops-exercise-prod-938429033253.us-east1.run.app)
* Code can be found here: [https://github.com/ovidio/cta-devops-technical-exercise](https://github.com/ovidio/cta-devops-technical-exercise)

I chose option 2 which is described below:
<div>
  <h3>Option 2: CI/CD Pipeline for a Cloud Run Service</h3>
  <p><b>Scenario:</b> You’re tasked with setting up a CI/CD pipeline for a Python service to deploy to Cloud Run.</p>
  <p><b>Tasks:</b></p>
  <ul>
    <li>Create a simple Python app (app.py) using Flask or FastAPI</li>
    <li>Write a Dockerfile to containerize the app</li>
    <li>Create a GitHub Actions workflow</li>
      <ul>
        <li>Lint the app</li>
        <li>Build and push to GCR</li>
        <li>Deploy to Cloud Run using GitHub Secrets (used in Actions)</li>
      </ul>
    <li>(Optional) Add a deploy.sh script for local deployments</li>
  </ul>
  <p><b>Note:</b> You are not required to deploy this to a live GCP project. If you are unable to test the Cloud Run deployment locally, describe how you would validate the CI/CD pipeline and deployment steps. We are more interested in your workflow and reasoning than a live deployment.</p>
  <p><b>Deliverables:</b></p>
    <li>app.py, Dockerfile, .github/workflows/deploy.yml</li>
    <li>README.md</li>
      <ul>
        <li>Explain your approach to secure deployment and GitHub Secrets</li>
        <li>Describe how a teammate could extend this for staging/prod</li>
        <li>Note any open questions, assumptions, or trade-offs you made</li>
      </ul>
</div>
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow the steps below:

### Prerequisites

Assuming you are running a linux machine, please verify that the below apps are installed.

* Python - Make sure you are running at least Python 3.9. Please see [this guide on how to install/upgrade your python version on linux and WSL](https://cloudbytes.dev/snippets/upgrade-python-to-latest-version-on-ubuntu-linux).

* pip - Make sure you are running the latest version of pip.
  ```sh
  python -m ensurepip --upgrade
  ```

* Docker Engine - Please refer [to the official Docker documentation on how to install Docker on linux](https://docs.docker.com/engine/install/ubuntu/).


### Installation

1. Giphy API Key: Sign up at Giphy Developers to get your free API key: [Giphy Developers](https://developers.giphy.com/).
2. Clone the repo
   ```sh
   git clone git@github.com:ovidio/cta-devops-technical-exercise.git
   ```
3. Create and activate Python virtual env
    ```sh
    python3 -m venv myenv
    source myenv/bin/activate
    ```
4. Add API Key to `app.py`
   ```python
   7 - API_KEY = "[API_KEY]"
   ```
5. Build Docker Image
   ```sh
   docker build -t [Image Name].
   ```
6. Run Docker Image in Detached mode and Publishing port 5000 (detached mode is needed when running locally)
   ```sh
   docker run -d -p 5000:5000 [Image Name]
   ```
7. Open Browser to [`localhost:5000`](localhost:5000)

8. Note: To run this using the Github Workflow there are a few secrets that need to be created in the repo > Secrets and Variables > Actions > Repository Secrets (or Env secrets). The secrets are listed below:
    ```
    GCP_DEPLOY_SA       - GCP Service Account Details (in JSON format)
    GCP_LOCATION        - GCP Location, ex: us-east1
    GCP_PROJECT_ID      - ID of GCP Project
    GCP_PROJECT_SA_NAME - GCP Service Account Email
    GIPHY_API_KEY       - Giphy Developer API key
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Approach to Secure Deployment and Github Secrets

Honestly, I don't trust using Github secrets. I know that in an enterprise settings having a private enterprise repo with secrets only visible to the repo (and any users with access) is from a security stand point somewhat secure. But I just don't trust having my secrets in the same room that I have my souurce code.

I used the repo secrets within the Actions settings, mostly because it was easy to bring into the github actions workflow. But preferably we would use a third party secrets manager like GCP secrets manager, Azure Key Vault, HashiCorp Vault, or AWS Secrets Manager. The reasons being two-fold: isolation of resources and built-in secrets management tools such as secrets rotations. The first is an important security concern because if an attacker get's into the enterprise github there wouldn't be any secrets to take. The second is important because when ingesting them into the Github Workflow it would be hitting some sort of API that obfuscates the actual secret. Meaning, if we update the secret on the secrets management tool it won't matter to Github since it will be hitting the same API endpoint. This makes it easier to scale as no secret is hardcoded anywhere.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## How to Extend for Staging/Prod

I'm of two minds for this. Ideally, we could use a single Github Workflow to manage all the envs (branches) within a single git repo. Github workflow has input options where we could maunally specify which branch to use when running the workflow. 


```
on:
  release:
      types: [published]
  workflow_dispatch:
    inputs:
      GCP_REGION:
        description: 'GCP Region to deploy in'
        required: true
        default: 'ap-south-1'
        type: choice
        options:
        - ap-south-1
        - ap-south-2
        - ....
      BRANCH:
        description: 'Branch to use'
        required: true
        default: 'master'
        type: choice
        options:
        - master
        - develop
        - staging

...

    jobs:
      deploy-terraform:
        uses: <reusable-workflow-path>
        with:
          GCP_REGION: ${{ inputs.GCP_REGION }}
          BRANCH: ${{ inputs.BRANCH }}
```

<br>
We could also do something similiar to what I setup in the workflow where the workflow triggers on every push and pull request and we have the workflow itself figure out which branch it is (from a pre-selected list). See below for example:

```
on:
  push:
    branches:
      - '**'
  pull_request:
    branches:
      - '**'

...
    - name: Determine Environment
      id: determine-env
      run: |
        # Determine environment based on branch        
        if [ "${{ github.ref_name }}" == "master" ]; then
          echo "MY_PROJECT_ENV=prod" >> $GITHUB_ENV
        elif [ "${{ github.ref_name }}" == "uat" ]; then
          echo "MY_PROJECT_ENV=stg" >> $GITHUB_ENV
        else
          echo "MY_PROJECT_ENV=dev" >> $GITHUB_ENV
        fi
```

This could also be extened to use releases and tags.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Open Questions, Assumptions, Trade-offs

<h3>Assumptions</h3>
* Some assumptions I had to make is that the infrastructure and connections are already present: specifically, Artifacts and any APIs that need to be turned on in GCP. I didn't know that the APIs had to be specifically turned on in GCP so that took some time to figure out.


<h3>Trade-Offs</h3>

* I had never used Github Secrets before this project. So I had the Giphy API key hard coded for a but until I verified that the app was running correctly and then figured out how to incorporate the secrets. So a Giphy API key is in the git history. I've since revoked that API and added a new one to Github Secrets.

* I opened up GCP Cloud Run to allow unathenticated accecss to the instance. This was for testing purposes and in an Enterprise setting wouldn't do that even for dev or other lower envs.

* Another trade-off I made for the sake of time was not implement a check on whether the app code had changed and if not then there's no need to run the workflow. For example, if I make a change to the README file it will run the entire workflow and deploy a container to GCP that is the same as the previous one.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
