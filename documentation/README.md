This directory contains documentation pertaining to the project's data models and overall architecture.

As the project evolves, so should the contents of this directory be updated in order to remain relevant.


### Entity Relationship Diagram (ERD)

The ERD was created using `draw.io` (a free online tool) and so should be edited there.

## Design Patterns
### Respository Pattern
The Repository Layer Setup phase is crucial for abstracting data access and promoting separation of concerns. This layer acts as an intermediary between the domain models and the database, allowing us to manage data operations more effectively and make the code more maintainable, modular and testable.

Purpose:
- Abstract data access logic from business logic.
- Promote cleaner, more maintainable code.
- Facilitate easier testing by isolating data access.

Benefits:
- Keeps data access logic separate from business logic, making the codebase cleaner and more organized.
- Makes it easier to write unit tests by allowing us to mock repository methods.
- Simplifies maintenance by centralizing data access logic in one place, reducing redundancy and inconsistency.
- Allows for easier changes to data access logic without impacting business logic, such as switching databases or optimizing queries.

Implementation Steps:
- Define Repository Interface
Create interface (or abstract base class) for each repository to define the operations that can be performed. This allows for flexibility and easier testing by enabling the use of mock repositories. It also prevents removal of required methods.
- Implement Repository Classes
Implement the repository interface with a concrete class that handles the actual data operations using Django’s ORM.
- Update Service Layer:
Modify the service layer to use the repository class for data operations instead of directly using the Django models.
