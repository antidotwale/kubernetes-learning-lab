FROM python:3.15-alpine@sha256:0f9552bb28711333da16915ec146f5e6bb44a7fdac9ced15dc17c2e0206346dd
RUN adduser -D -u 10001 app
WORKDIR /app
COPY --chown=10001:10001 app/server.py .
USER 10001
ENV PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["python", "server.py"]
