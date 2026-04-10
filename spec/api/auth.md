---
decision: Implement POST /auth/login and POST /auth/signup endpoints. Successful login returns a JWT. Passwords are hashed with bcrypt. Include email validation for signup.
constraints:
  - Passwords must meet complexity requirements
  - Rate limiting to prevent brute force
  - Refresh tokens optional but recommended
  - Store only hashed passwords in DB
rationale: Provides secure user authentication and authorization for the application.
affects:
  - backend/api/auth
  - frontend/auth
  - backend/middleware
---