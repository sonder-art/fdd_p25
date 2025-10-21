FROM debian:bullseye

RUN apt-get update && apt-get install -y ssh sshpass && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY bandit.sh .
RUN chmod +x bandit.sh

ENTRYPOINT ["./bandit.sh"]

