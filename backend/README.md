# EcoNecta Backend

Welcome to the **EcoNecta** backend. EcoNecta is an innovative solution designed to assist businesses in optimizing their sustainable practices through the use of artificial intelligence and data analysis of climatic and soil conditions.

This backend is developed using **Flask**, a lightweight web framework in Python that enables the rapid creation of web applications. Through this service, businesses can access intelligent crop recommendations, real-time data analysis, and precise predictions based on historical and current data.

## Features

- **RESTful API**: Provides endpoints for interacting with predictive models and retrieving recommendations.
- **Integration with Machine Learning Models**: Utilizes models saved in `.joblib` format to make predictions based on climatic and soil data.
- **Data Processing**: Leverages **Pandas** for data manipulation and analysis, ensuring that inputs are appropriately formatted for the model.
- **Scalability**: Designed to handle multiple concurrent requests, enabling efficient and rapid access to information.

## Technologies Used

- **Flask**: For creating the API and managing requests.
- **Pandas**: For data manipulation and analysis.
- **Joblib**: For loading and managing machine learning models.
- **Scikit-learn**: For data preprocessing and predictive modeling.
- **NumPy**: For numerical calculations and operations on arrays.

## Installation

To install and run the EcoNecta backend, please follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/your_username/econecta-backend.git](https://github.com/ojedavd/EcoNecta.git
    cd econecta-backend
    ```
2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    python app.py
    ```

## Usage

Once the server is up and running, you can make requests to the API to obtain recommendations and perform predictions. Please refer to the API documentation for detailed information on available endpoints.

---

Thank you for your interest in EcoNecta. Together, we can make a positive impact on the environment and promote sustainable business practices.
