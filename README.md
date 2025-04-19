# Current Development Applications - City of Windsor

This is a script to scrape and process development application data for the City of Windsor.

## Cloning the Repository

To get started, clone this repository to your local machine:

```bash
git clone https://github.com/HarjotSingh8/citywindsor-CurrentDevelopmentApplications.git
```

Replace `<repository-url>` with the actual URL of the repository.

## Running the Project

You can run this project using either Docker Compose or a Python virtual environment (venv).

### Using Docker Compose

1. Ensure you have Docker and Docker Compose installed on your system.
2. Navigate to the project directory:
   ```bash
   cd citywindsor-CurrentDevelopmentApplications
   ```
3. Start the application using Docker Compose:
   ```bash
   docker-compose up
   ```
4. Access the application logs to monitor its progress.

### Using Python Virtual Environment (venv)

1. Ensure you have Python 3.9 or later installed on your system.
2. Navigate to the project directory:
   ```bash
   cd citywindsor-CurrentDevelopmentApplications
   ```
3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Run the scraper script:
   ```bash
   python scraper.py
   ```

<!-- ## Notes
- Ensure all required dependencies are listed in `requirements.txt`.
- For Docker Compose, ensure the `docker-compose.yml` file is properly configured. -->

Feel free to reach out for any issues or questions regarding the setup.