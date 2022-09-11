FROM python:3.10-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

copy ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# cd to the directory again
RUN pipenv run python manage.py collectstatic --noinput \
    # Download NLTK dependencies
    && pipenv run python -m nltk.downloader -d /code/nltk punkt averaged_perceptron_tagger \
    # Change ownership of all files
    && chown -R nobody:nobody /code

# Run as non-root user
USER 65534:65534

RUN python manage.py collectstatic --noinput

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "--threads", "2", "--max-requests", "1000", "--max-requests-jitter", "100", "--access-logfile", "-", "--error-logfile", "-", "coeus.wsgi"]
