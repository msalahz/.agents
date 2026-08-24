---
detect:
  - dep:typescript
  - file:tsconfig.json
---

# TypeScript checks

## Idiomatic

- `unknown` at boundaries, narrowed before use. `any` and `as` casts that skip a check are findings.
- Discriminated unions over optional-field bags: `{ kind: "a", x } | { kind: "b", y }`, not `{ x?: ...; y?: ... }`.
- `satisfies` to check a literal against a type while keeping its narrow inference.
- Exhaustive `switch` on unions ends in a `never` check or a `default` that returns the unhandled member.
- Native methods first: `Object.groupBy`, `Array.prototype.at`, `structuredClone`, `Promise.allSettled`, `??`, `?.`. A hand-rolled helper that duplicates one is a finding.
- `readonly` on arrays and fields the function only reads.

## Maintainable

- A function's name says what it returns or does; a name needing a comment to explain it is a finding.
- Types derive from one source (`typeof schema`, `z.infer`, `ReturnType`) instead of being retyped by hand.
- Re-exports and barrel files that hide where a symbol lives.
- Boolean parameters that make call sites unreadable (`save(true, false)`); an options object or two functions instead.
- Magic strings and numbers used more than once without a named constant or union member.

## Cognitive Load

- Nesting deeper than three levels; early returns flatten it.
- One function doing parsing, validation, and side effects; split by what each part knows.
- Conditions that need a truth table to read: extract to a named boolean.
- Chains of `.then()` mixed with `await`.
- Ternaries nested inside ternaries.

## Edge Cases

- `undefined` from `array[i]`, `map.get`, `find`, optional fields, and JSON parsing treated as present.
- Empty arrays: `reduce` without an initial value, `arr[0]`, `Math.max(...[])`.
- Async functions whose rejection nobody awaits or catches (`forEach(async ...)`, unawaited calls in `try`).
- `Number(input)` and `parseInt` on user strings without a `Number.isFinite` check.
- Date handling: timezone assumptions, `new Date(string)` on non-ISO input, month arithmetic.
- Objects used as maps with user-controlled keys (`__proto__`, `constructor`); use `Map`.
- String comparison of ids that are numbers on one side.

## Complexity

- Nested loops or `.find`/`.includes` inside a loop over the same data: O(n²) where a `Map` or `Set` gives O(n).
- Repeated `.filter().map().find()` passes over one array that a single loop handles.
- Sorting to get one element (`sort()[0]`); a single pass finds min or max.
- Building large strings by repeated concatenation in a loop.
- Copying whole arrays or objects (`[...arr]`, spread in reducers) on every iteration.

## Idempotent

- Functions with side effects (writes, sends, increments) that a retry or double call repeats; look for a natural key, upsert, or an idempotency token.
- Module-level mutable state initialised on import.
- Functions that mutate their inputs.

## Scalable

- Loading a whole collection into memory to compute a count, sum, or one item.
- Unbounded caches (`Map` that only grows).
- `Promise.all` over an unbounded list with no concurrency limit.
- Recursion on user-sized input without a depth bound.

## Sanitization

- User strings interpolated into shell commands, file paths, regexes (`new RegExp(input)`), or URLs without escaping or an allow-list.
- `JSON.parse` on external input without schema validation afterwards.
- Path joins from user input without checking the result stays inside the intended directory.
- Error messages that echo raw input or internal details back to the caller.

## Thread-safe

- Read-modify-write on shared state across an `await` (check, then act, with another caller in between).
- Two concurrent calls that both pass a "does not exist" check before either inserts.
- Event handlers or timers registered without cleanup, firing twice after re-registration.
- Shared mutable module state touched by concurrent requests in a server process.
