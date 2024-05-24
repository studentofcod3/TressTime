"""
Stores information about the users of the system.

Has a central role in user management, authentication and authorization within the application.

Place within the System:
    The CustomUser entity is a core component. It represents all individuals who interact with
    the system, including customers, staff, and administrators. The CustomUser model extends Django's built-in user model
    to include additional attributes like profile pictures, providing a comprehensive representation of the system's users.

    Users are essential for booking appointments, receiving notifications, and managing their profiles. The system will rely
    on user data to authenticate and authorize actions, ensuring that only authorized individuals can perform certain tasks.
    User information will also be crucial for personalizing the user experience, sending targeted notifications, and maintaining
    security.

    By managing user data effectively, the system will be able to provide a seamless and secure experience for all users, supporting
    the core functionalities of booking services, managing appointments, and ensuring effective communication between
    customers and service providers.
"""
