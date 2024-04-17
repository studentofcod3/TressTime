# TressTime

### Description
A platform for local businesses (Currently tailored to hairdressers but can be modified for other local businesses, eg: consultancies, fitness studios) to manage appointments and bookings.

### Key Features:
  - User authentication and role-based access control.
  - Calendar integration for viewing and managing bookings.
  - Automated email or SMS reminders.
  - Payment gateway integration for prepayments or deposits.

### Tech Stack:
  - **Backend**: 
    - Language: Python
    - Framework: Django
  - **Frontend**: 
    - Language: Javascript
    - Framework: React
    - State Management: Redux / Context API _(TODO: decide which to use)_
  - **Database Management**: PostgreSQL

### Design Patterns:
- **Repository Pattern**:
    - **Overview**: Mediates between the domain and data mapping layers, acting like an in-memory domain object collection.
    - **Utility**: Provides a cleaner way to access data from the database, making it easier to switch databases or data sources without affecting other parts of the application.
- **Service Layer**:
    - **Overview**: Provides a set of services available to the client, abstracting business logic from user interface and data access logic.
    - **Utility**: Enhances application's maintainability by consolidating business logic in one place, making it reusable and easier to modify.
- The Repository and Service Layer are complimentary patterns so they are both being used in this application

