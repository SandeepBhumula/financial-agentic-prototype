# Use OpenJDK base image
FROM eclipse-temurin:17-jdk-jammy

# Set environment variables
ENV MAVEN_VERSION=3.9.5
ENV MAVEN_HOME=/usr/share/maven
ENV MAVEN_CONFIG=/root/.m2
ENV JAVA_HOME=/opt/java/openjdk

# Install Maven
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://archive.apache.org/dist/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz | tar -xzC /usr/share && \
    ln -s /usr/share/apache-maven-${MAVEN_VERSION} /usr/share/maven && \
    ln -s /usr/share/maven/bin/mvn /usr/bin/mvn && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Verify installations
RUN java -version && mvn -version

# Create working directory
WORKDIR /app

# Copy project files
COPY pom.xml .
COPY src ./src

# Build the application
RUN mvn clean package -DskipTests

# Run the application
CMD ["java", "-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005", "-jar", "target/card-api-0.0.1-SNAPSHOT.jar"]