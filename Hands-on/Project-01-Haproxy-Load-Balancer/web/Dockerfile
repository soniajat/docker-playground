# Alpine base keeps the image small (~50MB total) and reduces surface area
FROM python:3.12-alpine

WORKDIR /app

# Only app.py is needed — no requirements.txt since this uses stdlib only
COPY app.py .

# Run as a non-root user rather than the default root — costs nothing
# here and avoids a bad habit that's harder to fix later
RUN adduser -D appuser
USER appuser

# Documents the port the app listens on; actual publishing happens
# via docker-compose.yml's "ports" or "expose" entries
EXPOSE 5000

CMD ["python", "app.py"]