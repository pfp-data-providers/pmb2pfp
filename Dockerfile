# Use a lightweight Java base image
FROM openjdk:11-jre-slim

# Set environment variables
ENV JENA_VERSION=5.3.0 \
    JENA_HOME=/opt/apache-jena

# Install dependencies, download Apache Jena, and handle errors more gracefully
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && echo "Dependencies installed successfully" \
    # Download Apache Jena and unzip it
    && wget https://dlcdn.apache.org/jena/binaries/apache-jena-${JENA_VERSION}.zip -O /tmp/apache-jena.zip \
    && echo "Jena downloaded successfully" \
    && unzip /tmp/apache-jena.zip -d /opt \
    && mv /opt/apache-jena-${JENA_VERSION} ${JENA_HOME} \
    && rm /tmp/apache-jena.zip \
    # Clean up to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "Apache Jena setup completed"

# Add Jena binaries to PATH
ENV PATH="${JENA_HOME}/bin:${PATH}"

# Set the working directory
WORKDIR /data

# Entry point for the container
ENTRYPOINT ["riot"]
