FROM python:3.9
 
WORKDIR /code
 
COPY ./* /code/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./app /code/app
 
CMD ["uvicorn", "restController:app", "--host", "0.0.0.0", "--port", "8000"]