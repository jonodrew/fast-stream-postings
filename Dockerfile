FROM python:3.6
RUN useradd -m service-worker
WORKDIR /home/submit-fast-stream-post
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN pip install -r requirements.txt
COPY app app
COPY migrations migrations
COPY config.py postings.py deploy.sh ./
RUN chmod +x deploy.sh
ENV FLASK_APP postings.py
EXPOSE 5000
RUN chown -R service-worker:service-worker ./
USER service-worker
CMD ["./deploy.sh"]