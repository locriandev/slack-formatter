FROM registry.redhat.io/ubi8/python-311

WORKDIR /app

USER root

COPY requirements.txt /app/

RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chown -R 1001:0 /app && \
    chmod -R g=u /app

USER 1001

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
