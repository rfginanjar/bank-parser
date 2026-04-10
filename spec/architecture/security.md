---
decision: Enforce JWT-based authentication, encrypt sensitive data at rest, use HTTPS, and secure all PII. Hash passwords with bcrypt. Store secrets in environment variables.
constraints:
  - All API endpoints require authentication except login/signup
  - Account numbers encrypted using application-level or database encryption
  - JWTs signed with strong secret, short expiration (e.g., 1 hour)
  - Rate limiting on auth endpoints
rationale: Protects user data, prevents unauthorized access, and meets compliance requirements.
affects:
  - backend/auth
  - backend/models
  - infrastructure/tls
  - backend/config
---