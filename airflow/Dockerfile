FROM apache/airflow:2.8.1  

# or any other version you are using

# Install additional Python packages
COPY requirements.txt /tmp/


RUN pip install --no-cache-dir -r /tmp/requirements.txt
