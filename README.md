# Advanced-cloud-storage-based-Hospital-Management-System
**Snehal Awalekar, Bhavna Gupta, Abhilash Chaudhary**

## Inroduction
The project aims to develop a **Cloud-based Hospital Management System** that is a microservices-driven healthcare management system designed to streamline patient care, doctor management, pharmacy operations, and billing processes. This project leverages a modular architecture where each service operates independently, ensuring flexibility, scalability, and easy maintenance. With Dockerized deployment, the system is readily portable across different environments, and each service can be deployed or scaled individually. This approach supports a seamless user experience, where both healthcare providers and patients benefit from synchronized updates, clear interfaces, and efficient service management.

## Project Structure

- **`docker-compose.yml`**: Manages and orchestrates services using Docker Compose.
- **`patient_service`**: Contains the patient management microservice.
- **`doctor_service`**: Contains the doctor management microservice.
- **`pharmacy_service`**: Contains the pharmacy management microservice.
- **`billing_service`**: Contains the billing management microservice.

## Features
- **Cloud Architecture**: Each module operates in sync, allowing for systematic and effective way to manage all the services.
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
   - Patient Service: https://34.171.68.133/5001/
   - Doctor Service:  https://34.171.68.133/5002
   - Pharmacy Service: `http://localhost:PORT3`
   - Billing Service: `http://localhost:PORT4`

## Dependencies

Each service has its own dependencies listed in `requirements.txt`. These are automatically installed during Docker build.

## Contributing

Please follow the [contribution guidelines](CONTRIBUTING.md) and submit pull requests for review.

## License

This project is licensed under the MIT License.
