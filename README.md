# Paraphrases test task

## Stack
- NLTK
- Django
- Django REST Framework
- Unittest

## How to run
- Run terminal and enter a path to a project folder.
- Clone the repo:
  ```
  git clone https://github.com/DIVIgor/syntphraser.git
  ```
- Use Docker or virtual environment to continue
    - With Docker:
      Enter the commands below:
      - Build an image:
        ```
        docker build -t syntphraser .
        ```
      - Run the container:
        ```
        docker run -it --rm -p 8000:8000 --name paraphraser syntphraser
        ```

    - With virtual environment:
      - Create a virtual environment using:
        ```
        python -m venv venv
        ```
      - Install the dependencies:
        ```
        pip install -r requirements.txt
        ```
      - Run server:
        ```
        py manage.py runserver
        ```

## Endpoint
https://127.0.0.1:8000/paraphrase

parameters:
 - tree: str
 - limit: int (optional)
 
 Example:
 
    http://127.0.0.1:8000/paraphrase?tree=(S%20(NP%20(NP%20(DT%20The)%20(JJ%20charming)%20(NNP%20Gothic)%20(NNP%20Quarter)%20)%20(,%20,)%20(CC%20or)%20(NP%20(NNP%20Barri)%20(NNP%20G%C3%B2tic)%20)%20)%20(,%20,)%20(VP%20(VBZ%20has)%20(NP%20(NP(JJ%20narrow)%20(JJ%20medieval)%20(NNS%20streets)%20)%20(VP%20(VBN%20filled)%20(PP%20(IN%20with)%20(NP%20(NP%20(JJ%20trendy)%20(NNS%20bars)%20)%20(,%20,)%20(NP%20(NNS%20clubs)%20)%20(CC%20and)%20(NP%20(JJ%20Catalan)%20(NNS%20restaurants)%20)%20)%20)%20)%20)%20)%20)&limit=5
