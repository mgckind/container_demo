FROM python:3
# Install (as root) the modules needed to run the application
RUN pip install --no-cache-dir  tornado  gviz_api mysqlclient

# Create a demo folder
RUN mkdir demo
# Copy all the files inside the demo folder
ADD ./src /demo
# Change to /demo at run-time
WORKDIR /demo
# Execute this command when running the container, can be override
CMD [ "python", "main.py" ]
