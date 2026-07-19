---
name: java-development
description: Develop Controllers, DTOs, Services, Repository/Mappers, transactions, exception handling, and tests following the existing Java project architecture. Suitable for Spring, Spring Boot, MyBatis, or similar layered projects.
disable-model-invocation: false
---

# Java Development

Implementation task: $ARGUMENTS

## Identify project conventions first

- Java and framework version.
- Maven/Gradle module structure.
- Existing layering for Controller, DTO, VO, Service, Repository/Mapper.
- Validation, exception, permission, logging, and response body conventions.
- MyBatis/JPA usage patterns.
- JUnit, Mockito, Spring Test, and integration test conventions.

## Implementation rules

- Controllers handle protocol adaptation and input validation, not business rules.
- Services define transactions and domain workflows.
- Keep the data layer focused on queries; avoid implicit N+1.
- Keep DTO/VO separate from persistence entities unless the project explicitly uses a simple model.
- Use the project's existing exception hierarchy and unified error response.
- For write operations, consider idempotency, concurrency, and transaction rollback.
- Do not log passwords, tokens, ID documents, or full sensitive payloads.
- Parameterize SQL; whitelist dynamic SQL fragments.
- When adding database columns, state defaults, backfill, compatibility, and rollback.
- Do not unilaterally upgrade frameworks or replace persistence technologies.

## Testing

- Pure business logic prefers unit tests.
- Controller contracts use web-layer tests.
- SQL, transactions, and key mapping behavior use integration tests.
- Cover validation failures, permission failures, duplicate requests, and boundary data.

Call `analyst` to understand the current state, `architect` for complex designs, `coder` for implementation, `test-generator` for tests, and `reviewer` for the final review.