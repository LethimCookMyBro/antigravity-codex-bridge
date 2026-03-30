---
name: test
description: Test generation and test running command. Creates and executes tests for code.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Test

This skill adapts the Antigravity `/test` workflow for Codex.
Treat the user's message as a test target or test action.

## Purpose

This skill generates tests, runs existing tests, or checks test coverage.

## Sub-commands

```text
$test                - Run all tests
$test [file/feature] - Generate tests for specific target
$test coverage       - Show test coverage report
$test watch          - Run tests in watch mode
```

## Behavior

### Generate Tests

When asked to test a file or feature:

1. **Analyze the code**
   - Identify functions and methods
   - Find edge cases
   - Detect dependencies to mock

2. **Generate test cases**
   - Happy path tests
   - Error cases
   - Edge cases
   - Integration tests if needed

3. **Write tests**
   - Use the project's test framework
   - Follow existing test patterns
   - Mock external dependencies

## Output Format

### For Test Generation

```markdown
## Tests: [Target]

### Test Plan
| Test Case | Type | Coverage |
|-----------|------|----------|
| Should create user | Unit | Happy path |
| Should reject invalid email | Unit | Validation |
| Should handle db error | Unit | Error case |

### Generated Tests

`tests/[file].test.ts`

[Code block with tests]

Run with: `npm test`
```

### For Test Execution

```text
Running tests...

auth.test.ts (5 passed)
user.test.ts (8 passed)
order.test.ts (2 passed, 1 failed)

Failed:
- should calculate total with discount
  Expected: 90
  Received: 100

Total: 15 tests (14 passed, 1 failed)
```

## Examples

```text
$test src/services/auth.service.ts
$test user registration flow
$test coverage
$test fix failed tests
```

## Test Patterns

### Unit Test Structure

```typescript
describe('AuthService', () => {
  describe('login', () => {
    it('should return token for valid credentials', async () => {
      const credentials = { email: 'test@test.com', password: 'pass123' };
      const result = await authService.login(credentials);
      expect(result.token).toBeDefined();
    });

    it('should throw for invalid password', async () => {
      const credentials = { email: 'test@test.com', password: 'wrong' };
      await expect(authService.login(credentials)).rejects.toThrow('Invalid credentials');
    });
  });
});
```

## Key Principles

- Test behavior, not implementation details.
- Prefer descriptive test names.
- Use Arrange-Act-Assert structure.
- Mock external dependencies when needed.
