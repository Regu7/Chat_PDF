# PDF Chat Bot - End-to-End Implementation 

This project features a sophisticated chat bot based on the uploaded PDF file. It's developed using Large Language Models (LLM) and Retrieval-Augmented Generation (RAG). The bot is designed to assist users with various queries from the pdf by leveraging advanced natural language processing techniques and real-time data retrieval.

## To create a conda environment

`conda env create -f deploy\env.yml`

## To activate the conda environment

`conda activate chatbot_v2`

## To run the chatbot, follow the below commands

`streamlit run app.py --server.enableXsrfProtection false`

Note : Add your OPENAI_API_KEY environment variable in your system before running the script.


# Steps for creating a docker image

`docker build --build-arg MY_SECRET_KEY=<Provide your OPENAI API Key here> -t chatpdf:latest . `

# Tag your useraccount

`docker tag chatpdf:latest <username>/chatpdf:latest `

# Push the image to your docker hub

`docker push reguh/chatpdf:latest  `

# Steps for running the app from docker image inside Ubuntu Machine

`sudo apt update && sudo apt upgrade -y`

`curl -fsSL https://get.docker.com -o get-docker.sh`

`sudo sh get-docker.sh`

`sudo docker login `

`sudo docker service start `

`sudo docker pull reguh/chatpdf:latest`

`sudo docker run -p 8501:8501 reguh/chatpdf:latest`




