FROM python:3.8-slim-buster

EXPOSE 8050

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -q -r requirements.txt && \
    rm requirements.txt

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app:server"]
