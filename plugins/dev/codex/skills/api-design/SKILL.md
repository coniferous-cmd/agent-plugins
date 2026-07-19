---
name: api-design
description: Design or review HTTP/REST APIs covering resource model, request/response, errors, pagination, permissions, idempotency, versioning, and compatibility.
disable-model-invocation: false
---

# API Design

Design task: $ARGUMENTS

## Output requirements

### Use cases and resources
Describe callers, goals, resource identifiers, and state changes.

### Endpoint
For each endpoint, provide:
- Method and path
- Permissions
- Path / query / header
- Request body
- Success response
- Error response
- Idempotency requirement
- Pagination, sorting, and filtering
- Rate limiting or async behavior

### Contract rules

- Use stable resource names; do not cram verbs into URLs.
- Make required, nullable, default, length, and format explicit.
- Account for unknown enum values and forward compatibility.
- Make time zones and formats explicit.
- Avoid floating-point ambiguity for monetary amounts; state currency and smallest unit.
- Follow the existing project convention for pagination.
- Keep error codes stable and machine-readable, consistent with HTTP status.
- Write endpoints must document retries, idempotency keys, and conflict behavior.
- Do not leak internal exceptions, SQL, or sensitive fields in responses.
- Breaking changes require versioning, migration, or dual-write/compatibility phases.

### Validation
Provide suggestions for contract tests, permission tests, boundary tests, and compatibility tests.