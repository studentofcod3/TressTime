This directory contains documentation pertaining to the project's data models and overall architecture.

As the project evolves, so should the contents of this directory be updated in order to remain relevant.


### Entity Relationship Diagram (ERD)

The ERD was created using `draw.io` (a free online tool) and so should be edited there.

## Design Patterns
### Respository Pattern
The Repository Layer Setup phase is crucial for abstracting data access and promoting separation of concerns. This layer acts as an intermediary between the domain models and the database, allowing us to manage data operations more effectively and make the code more maintainable, modular and testable.

#### Purpose:
- Abstract data access logic from business logic.
- Promote cleaner, more maintainable code.
- Facilitate easier testing by isolating data access.

#### Benefits:
- Keeps data access logic separate from business logic, making the codebase cleaner and more organized.
- Makes it easier to write unit tests by allowing us to mock repository methods.
- Simplifies maintenance by centralizing data access logic in one place, reducing redundancy and inconsistency.
- Allows for easier changes to data access logic without impacting business logic, such as switching databases or optimizing queries.

#### Implementation Steps:
- Define Repository Interface:
  - Create interface (inheriting from python's ABC - abstract base class) for each repository to define the operations that can be performed. This defines the contract for classes which have the concrete implementation but also allows for flexibility and easier testing by enabling the use of mock repositories.
  - **NOTE:** having an interface also adheres to the Dependency Inversion Principle (DIP) of the **SOLID** principles. This makes the code more modular and easier to maintain or replace.
- Implement Repository Class:
  - Implement the repository interface with a concrete class that handles the actual data operations using Django’s ORM.
- Update Service Layer:
  - Modify the service layer to use the repository class for data operations instead of directly using the Django models.


### Service Layer
Implementing the service layer involves encapsulating business logic in service classes. This layer interacts with the repository layer and performs operations that are necessary for the application’s use cases.

#### Purpose:
- Encapsulation of Business Logic: 
  - Centralizes and encapsulates business logic in a single layer, keeping it separate from the presentation and data access layers.
- Separation of Concerns: 
  - Enhances code organization by separating business logic from data access and user interface concerns.
- Reusability: 
  - Provides reusable methods for common operations, reducing code duplication across the application.
- Consistency: 
  - Ensures consistent application of business rules and logic across different parts of the application.
- Testing: 
  - Facilitates easier testing of business logic in isolation from data access and presentation layers.
- Flexibility: 
  - Allows for changes in business logic without affecting other parts of the application, making the system more adaptable to change.
- Interoperability: 
  - Enables integration with different data sources, services, or APIs by acting as an intermediary layer.

#### Benefits:
- Improved Maintainability: 
  - By separating concerns, the service layer makes the codebase easier to maintain and understand.
- Enhanced Testability: 
  - Business logic can be tested in isolation, leading to more comprehensive and reliable tests.
- Adherence to **SOLID** Principles:
  - Supports the *Single Responsibility Principle* by keeping business logic separate from data access and presentation.
  - Encourages the *Open/Closed Principle* by allowing the extension of business logic without modifying existing code.
  - Promotes the *Liskov Substitution Principle* by defining service interfaces that can be implemented by different classes.
  - Aligns with the *Interface Segregation Principle* by ensuring that services depend on the methods they use.
  - Follows the *Dependency Inversion Principle* by depending on abstractions rather than concrete implementations.
- Consistency and Reusability: 
  - Ensures consistent application of business rules and reduces code duplication.
- Flexibility and Scalability:
  - Allows for easy modification and extension of business logic, making the application more adaptable to changes and scalable.
- Reduced Code Duplication:
  - Centralizes business logic in one place, reducing the need to duplicate this logic across multiple parts of the application.
- Clear Structure:
  - Provides a clear, organized structure that separates business logic from other concerns, enhancing the overall architecture of the application.

#### Implementation Steps:
- Define the Service Interface:
  - Create interface (inheriting from python's ABC - abstract base class) for each service to define the operations that can be performed. This defines the contract for classes which have the concrete implementation but also allows for flexibility and easier testing by enabling the use of mock services.
  - **NOTE:** having an interface also adheres to the Dependency Inversion Principle (DIP) of the **SOLID** principles. This makes the code more modular and easier to maintain or replace.
- Create a validator class to handle all service validation
- Implement the Concrete Service Class:
  - The class should:
    - Handle all business logic.
    - Use the Repository for all data access.
    - Use the Validator for validation. 
