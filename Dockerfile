# Use a lightweight Java base image
FROM openjdk:11-jre-slim

# Set environment variables
ENV JENA_VERSION=4.8.0 \
    JENA_HOME=/opt/apache-jena

# Install dependencies and download Apache Jena
RUN apt-get update && apt-get install -y wget unzip \
    && wget https://dlcdn.apache.org/jena/binaries/apache-jena-${JENA_VERSION}.zip -O /tmp/apache-jena.zip \
    && unzip /tmp/apache-jena.zip -d /opt \
    && mv /opt/apache-jena-${JENA_VERSION} ${JENA_HOME} \
    && rm /tmp/apache-jena.zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add Jena binaries to PATH
ENV PATH="${JENA_HOME}/bin:${PATH}"

# Set the working directory
WORKDIR /data

# Entry point for the container
ENTRYPOINT ["riot"]
