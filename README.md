# Client Query Management System

A comprehensive Streamlit-based web application for managing client queries and support tickets with role-based access control.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red.svg)
![MySQL](https://img.shields.io/badge/mysql-8.0+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

##  Features

### Authentication System
- Secure login with bcrypt password hashing
- Role-based access control (Client/Support)
- Session management
- Secure logout functionality

### User Roles

#### Client Role
- **Query Management**: Create and submit new queries with categories
- **Dashboard**: View personal query statistics and analytics
- **Profile Management**: Update personal information and password
- **Query Tracking**: Monitor query status and resolution times

#### Support Role
- **Query Management**: View, close, and reopen all client queries
- **Advanced Dashboard**: Comprehensive analytics and reporting
- **Performance Metrics**: Resolution time tracking and category analysis
- **Profile Management**: Update support staff information

### Analytics & Reporting
- Open vs Closed query statistics
- Category distribution charts
- Query resolution time analysis
- Performance metrics by category
- Pending query alerts (24+ hours)

## Installation

### Prerequisites
- Python 3.7+
- MySQL Database
- pip package manager

### Setup Instructions

1. **Clone the repository**
```bash
git clone <repository-url>
cd client-query-management
```

2. **Install dependencies**
```bash
pip install streamlit bcrypt pandas plotly mysql-connector-python
```

3. **Create the database and tables**

    Use database.sql to create databse

4. **Configure database connection**

    Update database details on db_connection.py

5. **Run the application**
```bash
streamlit run app.py
```

6. **Access the application**

Open your browser and navigate to `http://localhost:8501`

## Project Structure

```
client-query-management/
├── app.py                          # Main application entry point
├── login_page.py                   # Authentication module
├── client_page.py                  # Client-specific functionality
├── support_page.py                 # Support staff functionality
├── database.sql                    # Database Queries
├── db_connection.py                # Database connection handler
├── synthetic_client_query.sql      # Sample Query
└── README.md                       # Project documentation
```

## Core Modules

### app.py
- Main application controller
- Session state management
- Role-based routing
- Navigation sidebar

### login_page.py
- User authentication
- Password verification
- Role-based redirection

### client_page.py
- `client_query_page()`: Query creation and submission
- `client_dashboard_page()`: Personal analytics and query tracking
- `client_profile_page()`: Profile management

### support_page.py
- `support_query_page()`: Query management and status updates
- `support_dashboard_page()`: Comprehensive analytics and reporting
- `support_profile_page()`: Support staff profile management

## Key Functionalities

### Query Categories
- Bug Report
- Technical Support
- Billing Problem
- Payment Failure
- Account Suspension
- Login Issue
- Subscription Cancellation
- Feature Request
- UI Feedback
- Data Export

### Dashboard Features
- Real-time query status tracking
- Interactive filters (status, category)
- Visual analytics with Plotly charts
- Resolution time statistics
- Category-wise performance metrics
- Pending query monitoring

## Configuration

### Database Connection
Update the `db_connection.py` file with your MySQL credentials:
- Host name
- Username and password
- Database name

### User Management
- Users are stored in the `users` table with bcrypt hashed passwords
- Roles: `'client'` or `'support'`
- Profile information includes username, email, and mobile number

## Usage Guide

### For Clients:
1. Login with client credentials
2. **Create Queries** using the Queries page
3. **Track Progress** in the Dashboard
4. **Update Profile** as needed

### For Support Staff:
1. Login with support credentials
2. **Manage Queries** - view, close, or reopen tickets
3. **Analyze Performance** using dashboard metrics
4. **Monitor SLAs** with resolution time tracking

## Query Lifecycle

```
Creation → Open Status → [Support Processing] → Closed Status → (Optional Reopen)
```

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: MySQL
- **Authentication**: bcrypt
- **Visualization**: Plotly
- **Data Processing**: Pandas

## Notes

- Ensure MySQL server is running before starting the application
- Use strong passwords for database users in production
- The application uses session state for maintaining login status
- All passwords are hashed using bcrypt before storage

## Security Considerations

 **Important**: This is a demonstration application. For production use, consider adding:
- Additional security measures
- Input validation and sanitization
- Error handling and logging
- HTTPS/SSL encryption
- Rate limiting
- Session timeout mechanisms
- SQL injection prevention (use parameterized queries)
- CSRF protection

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues or questions regarding setup and usage, please check:
- Database connection parameters
- Table structure matches the schema
- User roles are properly set in the database
- MySQL service is running

## Contact

For additional support or inquiries, please open an issue in the repository.

---

**Note**: Remember to update your database credentials in `db_connection.py` before running the application.
