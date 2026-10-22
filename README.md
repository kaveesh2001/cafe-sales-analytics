# Cafe Sales Analytics and Business Insight System

A Python-based café management and sales analytics system
designed to help manage café operations and understand sales
performance through data analysis.

## Project Overview

This project combines café operational management with
sales analysis. It is being developed as a practical project
to improve my skills in Python programming, database
management, data analysis, and business intelligence.

## Features

- Product management
- Point of Sale (POS) workflow
- Order and order-item management
- Customer and user management
- MySQL database integration
- Sales analysis
- Input validation

## Technology Stack

- Python
- MySQL
- Streamlit
- Pandas (where used for data analysis)

## Project Structure

```text
Cafe-Sales-Analytics/
├── analytics/
├── assets/
├── dashboard/
├── database/
├── models/
├── services/
├── utils/
├── main.py
└── test.py

```

## Getting Started

Follow these steps to run the project on your computer.

### 1. Clone the Repository

```bash
git clone https://github.com/kaveesh2001/cafe-sales-analytics.git
cd cafe-sales-analytics
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install the Required Packages

Install the required Python packages using:

```bash
pip install -r requirements.txt
```

### 5. Configure the Database

- Install and start MySQL.
- Create the `cafe_sales_analytics` database.
- Add your database credentials to a local `.env` file.
- Make sure the `.env` file is not uploaded to GitHub.

### 6. Run the Application

To launch the Streamlit dashboard, run:

```bash
python -m streamlit run dashboard/app.py
```

## Security

Do not upload database passwords, API keys, or other sensitive information to GitHub. Store credentials in a local `.env` file and exclude it from version control.

## Project Status

This project is currently under development. Features and sales analytics will be improved as development continues.

## Author

**Kaveesh Lakshitha**

GitHub: [kaveesh2001](https://github.com/kaveesh2001)



## Future Improvements

The following improvements are planned for future development:

- Interactive sales analytics dashboard
- Daily, weekly, and monthly sales reports
- Best-selling and low-selling product analysis
- Peak sales time analysis
- Customer purchase behaviour analysis
- Data visualisation using charts and graphs
- Improved error handling and input validation
- Automated report generation

## Learning Objectives

This project helps me develop practical skills in:

- Python programming and object-oriented programming
- MySQL database integration
- Data analysis and business insights
- Building interactive dashboards with Streamlit
- Software development and project management
- Git and GitHub version control