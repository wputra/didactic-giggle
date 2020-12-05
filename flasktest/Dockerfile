FROM python:3.7-alpine
WORKDIR /code
COPY . .
RUN apk add --no-cache gcc musl-dev linux-headers && \
    pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]
