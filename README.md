# Advanced-cloud-storage-based-Hospital-Management-System-for-Enhanced-Operational-Efficiency
**Snehal Awalekar, Bhavna Gupta, Abhilash Chaudhary**

## Inroduction
The project aims to develop a **microservices-based Hospital Management System** that streamlines key functions like patient registration, appointment scheduling, and billing. 
Using Docker for containerization and Docker Compose for orchestration, the system ensures scalability, modularity, and real-time cloud connectivity to enhance operational efficiency and patient care in modern healthcare settings.

## Project Structure

- **`docker-compose.yml`**: Manages and orchestrates services using Docker Compose.
- **`patient_service`**: Contains the patient management microservice.
- **`doctor_service`**: Contains the doctor management microservice.
- **`pharmacy_service`**: Contains the pharmacy management microservice.
- **`billing_service`**: Contains the billing management microservice.

## Features

- **Microservices Architecture**: Each module operates independently, allowing for isolated development and deployment.
- **Dockerized Services**: Each service has a Dockerfile for consistent and portable deployment.
- **Responsive UI**: HTML templates for each service provide a simple, user-friendly interface.

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Major-Project.git
   cd Major-Project
   ```

2. **Build and Run Services**:
   Ensure Docker is installed and running.
   ```bash
   docker-compose up --build
   ```

3. **Access Services**:
   - Patient Service: `http://localhost:PORT1`
   - Doctor Service: `http://localhost:PORT2`
   - Pharmacy Service: `http://localhost:PORT3`
   - Billing Service: `http://localhost:PORT4`

## Dependencies

Each service has its own dependencies listed in `requirements.txt`. These are automatically installed during Docker build.

## Contributing

Please follow the [contribution guidelines](CONTRIBUTING.md) and submit pull requests for review.

## License

This project is licensed under the MIT License.
