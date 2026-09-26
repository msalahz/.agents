# Review checklists

Stack-specific code review checks for Drizzle, React, TanStack Start, and TypeScript, plus the shape of a stack check file.

## Patterns

- **Stack check file shape.** Open each stack file with YAML `detect` frontmatter (`dep:drizzle-orm`, `dep:react`, `dep:@tanstack/react-start` with a scope line naming server functions, router loaders, and TanStack Query, or `dep:typescript`/`file:tsconfig.json`), then give it nine fixed H2 lenses: Idiomatic, Maintainable, Cognitive Load, Edge Cases, Complexity, Idempotent, Scalable, Sanitization, Thread-safe. _Sources: docs/agents/code-review/drizzle.md, docs/agents/code-review/react.md, docs/agents/code-review/tanstack-start.md, docs/agents/code-review/typescript.md_
- **Terse check lists.** Write each stack check as one line naming a smell and, often, its fix. _Sources: docs/agents/code-review/drizzle.md_

### TanStack Start

- **Server function chain.** Build server functions as `createServerFn({ method }).middleware([...]).validator(schema).handler(...)`, with `GET` for reads and `POST` for writes. _Sources: docs/agents/code-review/tanstack-start.md_
- **Thin server functions.** Keep DB code out of server-function modules; validate there and delegate to a server module that takes context values as parameters. _Sources: docs/agents/code-review/tanstack-start.md_
- **Route data flow.** Have route `context` return query options, the `loader` call `fetchQuery` or `ensureQueryData`, and the component read with `useSuspenseQuery`, and flag `useEffect` fetching in a route. _Sources: docs/agents/code-review/tanstack-start.md_
- **Query key factory.** Keep one query key factory per domain and never write inline key arrays in components. _Sources: docs/agents/code-review/tanstack-start.md_
- **Mutations module.** Put `useMutation` calls in a `*.mutations.ts` module that runs `invalidateQueries` on success. _Sources: docs/agents/code-review/tanstack-start.md_

## Practices

### Drizzle

- **Relational vs builder.** Use relational queries for reads that need relations and the builder for aggregates and projections, and flag one read that mixes both. _Sources: docs/agents/code-review/drizzle.md_
- **Schema-derived types.** Use `$inferSelect` or `drizzle-zod` instead of hand-written interfaces that mirror a table. _Sources: docs/agents/code-review/drizzle.md_
- **pgEnum-derived unions.** Define enum columns with `pgEnum` and derive the TypeScript unions from it. _Sources: docs/agents/code-review/drizzle.md_
- **Column refs via table object.** Reference columns through the table object and flag string column names outside `sql` fragments. _Sources: docs/agents/code-review/drizzle.md_
- **Use returning().** Read written rows back with `returning()` instead of a second select. _Sources: docs/agents/code-review/drizzle.md_
- **Queries in data layer.** Keep query logic in the data layer module, not in loaders, components, or server-function handlers. _Sources: docs/agents/code-review/drizzle.md_
- **Migrations with schema change.** Check in migrations in the same change as the schema edit. _Sources: docs/agents/code-review/drizzle.md_
- **Shallow condition trees.** Name the sub-conditions of `and()`/`or()` trees deeper than two levels. _Sources: docs/agents/code-review/drizzle.md_
- **CTE over inline subquery.** Prefer `db.$with` or a named helper to an inline subquery where it reads better. _Sources: docs/agents/code-review/drizzle.md_
- **Handle not-found.** Flag code that treats a `findFirst` result or `[0]` as present. _Sources: docs/agents/code-review/drizzle.md_
- **Check affected count.** Check the affected row count on updates and deletes that can match zero rows when the caller assumes success. _Sources: docs/agents/code-review/drizzle.md_
- **Domain errors for unique violations.** Map unique-constraint errors to domain errors instead of surfacing them raw. _Sources: docs/agents/code-review/drizzle.md_
- **Empty list guards.** Guard `inArray` and `array_position` against an empty list. _Sources: docs/agents/code-review/drizzle.md_
- **Null semantics.** Use `isNull`, since `eq(column, null)` never matches. _Sources: docs/agents/code-review/drizzle.md_
- **Timezone mode.** Flag timestamps with no declared timezone mode that are compared to UTC. _Sources: docs/agents/code-review/drizzle.md_
- **No N+1.** Replace per-row queries with `with`, a join, or `inArray` on collected ids. _Sources: docs/agents/code-review/drizzle.md_
- **Index filtered columns.** Check the schema for indexes on columns used in `where`, `orderBy`, or joins on growing tables. _Sources: docs/agents/code-review/drizzle.md_
- **Narrow selects.** Select named columns instead of `select()` on a wide table when two fields are used. _Sources: docs/agents/code-review/drizzle.md_
- **count() not length.** Count with `count()` instead of loading rows and taking the length. _Sources: docs/agents/code-review/drizzle.md_
- **Aggregate in DB.** Let the database compute aggregates instead of reading whole tables into the app. _Sources: docs/agents/code-review/drizzle.md_
- **Limit findMany.** Flag `findMany` with no `limit` on growing tables. _Sources: docs/agents/code-review/drizzle.md_
- **Keyset pagination.** Prefer keyset pagination on an indexed column over offset on large tables. _Sources: docs/agents/code-review/drizzle.md_
- **Batch updates.** Write one `update ... where inArray` instead of a loop of per-row updates. _Sources: docs/agents/code-review/drizzle.md_
- **Conflict-safe inserts.** Use `onConflictDoNothing` or `onConflictDoUpdate` on the natural key for inserts a retry can duplicate. _Sources: docs/agents/code-review/drizzle.md_
- **Stable reorder.** Make position recomputation give the same result when run twice. _Sources: docs/agents/code-review/drizzle.md_
- **Bound parameters in sql.** Interpolate values into `sql` as bound parameters, never by concatenation, and treat `sql.raw` with user input as high risk. _Sources: docs/agents/code-review/drizzle.md_
- **Allow-list identifiers.** Pass dynamic column names, table names, and `orderBy` from user input through an allow-list. _Sources: docs/agents/code-review/drizzle.md_
- **Transactions for multi-writes.** Wrap multi-statement writes in `db.transaction`. _Sources: docs/agents/code-review/drizzle.md_
- **Transactional read-modify-write.** Run `max(position) + 1` and balance updates inside a transaction or with `for update`. _Sources: docs/agents/code-review/drizzle.md_
- **No check-then-insert race.** Replace check-then-insert with a unique constraint or `onConflict`. _Sources: docs/agents/code-review/drizzle.md_
- **No app-side counters.** Flag counters and sequences maintained in application code. _Sources: docs/agents/code-review/drizzle.md_

### React

- **Derive during render.** Compute derived values during render instead of storing them in state synced by `useEffect`. _Sources: docs/agents/code-review/react.md_
- **Effects only for external sync.** Flag an effect that only sets state from props. _Sources: docs/agents/code-review/react.md_
- **Data library for async state.** Load async data with a query or loader instead of `useEffect` plus `useState` plus `fetch`. _Sources: docs/agents/code-review/react.md_
- **React 19 form primitives.** Prefer `action`, `useActionState`, `useOptimistic`, and `useFormStatus` over hand-rolled handlers and loading flags. _Sources: docs/agents/code-review/react.md_
- **ref as prop.** Pass `ref` as a prop, since `forwardRef` is legacy in React 19. _Sources: docs/agents/code-review/react.md_
- **Stable keys.** Key list items by a stable id, never the index when items reorder or are removed. _Sources: docs/agents/code-review/react.md_
- **Composition over layout booleans.** Use children and slots instead of layout booleans. _Sources: docs/agents/code-review/react.md_
- **Split large components.** Split a component by responsibility past about 150 lines or five pieces of state. _Sources: docs/agents/code-review/react.md_
- **Limit prop drilling.** Move props drilled more than two levels into context or a colocated hook. _Sources: docs/agents/code-review/react.md_
- **Hook naming and cohesion.** Name custom hooks for what they return and keep state that changes together inside one hook. _Sources: docs/agents/code-review/react.md_
- **Few render branches.** Flag a component that returns three or more different trees. _Sources: docs/agents/code-review/react.md_
- **Shallow JSX.** Extract a named component past four levels of nesting that carry logic. _Sources: docs/agents/code-review/react.md_
- **Small handlers.** Flag handlers that touch more than three state variables. _Sources: docs/agents/code-review/react.md_
- **Status union over flags.** Model a cluster of boolean flags as one status union. _Sources: docs/agents/code-review/react.md_
- **Order-dependent effects.** Flag multiple effects whose ordering matters. _Sources: docs/agents/code-review/react.md_
- **Loading, empty, error branches.** Give data-driven UI a loading, an empty, and an error branch. _Sources: docs/agents/code-review/react.md_
- **Empty list safety.** Check that `items[0]` exists before using it. _Sources: docs/agents/code-review/react.md_
- **Controlled input stability.** Keep a controlled input's value defined, since `undefined` switches it to uncontrolled. _Sources: docs/agents/code-review/react.md_
- **Race-safe effects.** Guard effects against set-after-unmount and stale responses with an ignore flag or an abort controller. _Sources: docs/agents/code-review/react.md_
- **Effect cleanup.** Clean up subscriptions, listeners, timers, and observers an effect creates. _Sources: docs/agents/code-review/react.md_
- **StrictMode-safe effects.** Write effects that behave correctly when StrictMode invokes them twice. _Sources: docs/agents/code-review/react.md_
- **Stale closures.** Flag missing effect dependencies and non-functional setters that read stale state. _Sources: docs/agents/code-review/react.md_
- **Mutations on user action.** Fire mutations from user actions, not on mount or on a dependency change. _Sources: docs/agents/code-review/react.md_
- **Prevent double submit.** Stop a form from submitting again before the first submission resolves. _Sources: docs/agents/code-review/react.md_
- **Disable while pending.** Disable a button while its mutation is pending (`isPending` in TanStack Query). _Sources: docs/agents/code-review/react.md, docs/agents/code-review/tanstack-start.md_
- **Optimistic rollback.** Give optimistic updates a rollback and keep them from doubling up on one entity. _Sources: docs/agents/code-review/react.md_
- **Single owner per server entity.** Flag two components that each write back their own copy of one server entity. _Sources: docs/agents/code-review/react.md_
- **Memo-safe props.** Flag inline literals passed to memoised children. _Sources: docs/agents/code-review/react.md_
- **Measured memoisation.** Wrap heavy render work in `useMemo` when measurement shows the cost, or move it out of render. _Sources: docs/agents/code-review/react.md_
- **Stable context values.** Flag context values recreated on every render. _Sources: docs/agents/code-review/react.md_
- **State placement.** Move state that re-renders a large subtree on every keystroke closer to where it is used. _Sources: docs/agents/code-review/react.md_
- **Virtualise long lists.** Virtualise or paginate lists of hundreds of rows. _Sources: docs/agents/code-review/react.md_
- **Image hints.** Give images in long lists size hints and lazy loading. _Sources: docs/agents/code-review/react.md_
- **Bounded client state.** Filter on the server instead of loading whole tables into the browser. _Sources: docs/agents/code-review/react.md_
- **Debounce search.** Debounce or cancel per-keystroke search requests. _Sources: docs/agents/code-review/react.md_
- **Sanitise HTML.** Run user, API, or markdown content through a sanitiser before `dangerouslySetInnerHTML`. _Sources: docs/agents/code-review/react.md_
- **Safe URLs.** Reject `javascript:` and `data:` schemes in `href` and `src` built from user input. _Sources: docs/agents/code-review/react.md_
- **noopener.** Add `rel="noopener"` to `target="_blank"` links with user content where the platform does not default it. _Sources: docs/agents/code-review/react.md_
- **No server secrets in client.** Flag secrets or server-only values imported into client components. _Sources: docs/agents/code-review/react.md_

### TanStack Start

- **Pending and error components.** Define `pendingComponent` and `errorComponent` on routes that load data. _Sources: docs/agents/code-review/tanstack-start.md_
- **Reuse middleware.** Compose middleware once and reuse it instead of re-declaring it per server function. _Sources: docs/agents/code-review/tanstack-start.md_
- **Split overloaded handlers.** Flag handlers that unpack context, branch on permissions, and query in one body. _Sources: docs/agents/code-review/tanstack-start.md_
- **Split overloaded loaders.** Flag loaders that fetch, transform, and redirect in one function. _Sources: docs/agents/code-review/tanstack-start.md_
- **Use notFound().** Throw `notFound()` from loaders instead of leaving a blank page. _Sources: docs/agents/code-review/tanstack-start.md_
- **No undefined misses.** Flag server functions that return `undefined` where the client expects an object. _Sources: docs/agents/code-review/tanstack-start.md_
- **Do not swallow redirect.** Flag a `redirect()` thrown inside a `try` that swallows it. _Sources: docs/agents/code-review/tanstack-start.md_
- **Consistent search defaults.** Give search params the same defaults in the validator and the component. _Sources: docs/agents/code-review/tanstack-start.md_
- **Parallel independent awaits.** Run independent awaits in loaders and `beforeLoad` with `Promise.all`. _Sources: docs/agents/code-review/tanstack-start.md_
- **No duplicate auth checks.** Skip session and permission checks a shared middleware already ran. _Sources: docs/agents/code-review/tanstack-start.md_
- **Sensible staleTime.** Flag zero `staleTime` on data that rarely changes. _Sources: docs/agents/code-review/tanstack-start.md_
- **Use select.** Transform large query payloads with `select`. _Sources: docs/agents/code-review/tanstack-start.md_
- **Paginate server functions.** Give server functions that return collections pagination or filter arguments. _Sources: docs/agents/code-review/tanstack-start.md_
- **Filter server-side.** Flag client-side filtering the server should do. _Sources: docs/agents/code-review/tanstack-start.md_
- **No unused prefetch.** Flag loaders that prefetch data the route does not render. _Sources: docs/agents/code-review/tanstack-start.md_
- **Idempotent POST.** Use a natural key or an upsert for `POST` writes that can be retried. _Sources: docs/agents/code-review/tanstack-start.md_
- **No mutations from effects or loaders.** Keep mutations out of effects and loaders. _Sources: docs/agents/code-review/tanstack-start.md_
- **Single-fire onSuccess.** Keep navigation and toasts in `onSuccess` from repeating on retry. _Sources: docs/agents/code-review/tanstack-start.md_
- **Optimistic safety.** Roll back optimistic updates in `onError` and cancel in-flight queries in `onMutate`. _Sources: docs/agents/code-review/tanstack-start.md_
- **Invalidation races.** Flag two mutations whose invalidations race on one entity. _Sources: docs/agents/code-review/tanstack-start.md_
- **Transactional server writes.** Wrap read-then-write on shared rows in a transaction. _Sources: docs/agents/code-review/tanstack-start.md_
- **Always validate server functions.** Give every server function a `.validator(...)` and treat a missing one on `POST` as high risk. _Sources: docs/agents/code-review/tanstack-start.md_
- **Strict validators.** Use strict validators so extra keys cannot spread into inserts. _Sources: docs/agents/code-review/tanstack-start.md_
- **Validated route params.** Type and validate route input with `validateSearch` and `params.parse`. _Sources: docs/agents/code-review/tanstack-start.md_
- **Validate request values.** Validate header and request values before they reach a query. _Sources: docs/agents/code-review/tanstack-start.md_
- **Allow-listed redirects.** Check redirect targets taken from search params against an allow-list of internal paths. _Sources: docs/agents/code-review/tanstack-start.md_
- **No internal error leak.** Keep internal messages and stacks from handler errors out of client responses. _Sources: docs/agents/code-review/tanstack-start.md_

### TypeScript

- **unknown at boundaries.** Type boundary input as `unknown` and narrow it before use, and flag `any` and unchecked `as` casts. _Sources: docs/agents/code-review/typescript.md_
- **Discriminated unions.** Prefer discriminated unions over bags of optional fields. _Sources: docs/agents/code-review/typescript.md_
- **satisfies.** Check literals with `satisfies` to keep narrow inference. _Sources: docs/agents/code-review/typescript.md_
- **Exhaustive switch.** End a switch in a `never` check or a `default` that returns the unhandled member. _Sources: docs/agents/code-review/typescript.md_
- **Single-source types.** Derive types from `typeof schema`, `z.infer`, or `ReturnType` instead of restating them. _Sources: docs/agents/code-review/typescript.md_
- **readonly by default.** Mark read-only parameters and fields `readonly`. _Sources: docs/agents/code-review/typescript.md_
- **Native methods first.** Flag a hand-rolled helper that duplicates `Object.groupBy`, `at`, `structuredClone`, `Promise.allSettled`, `??`, or `?.`. _Sources: docs/agents/code-review/typescript.md_
- **Self-describing names.** Rename a function whose name needs a comment. _Sources: docs/agents/code-review/typescript.md_
- **Avoid barrels.** Flag re-exports and barrel files that hide where a symbol lives. _Sources: docs/agents/code-review/typescript.md_
- **No boolean params.** Replace a boolean parameter with an options object or two functions. _Sources: docs/agents/code-review/typescript.md_
- **Name repeated literals.** Give a magic string or number used more than once a constant or a union member. _Sources: docs/agents/code-review/typescript.md_
- **Early returns.** Use early returns once nesting passes three levels. _Sources: docs/agents/code-review/typescript.md_
- **Split by knowledge.** Split parsing, validation, and side effects by what each part knows. _Sources: docs/agents/code-review/typescript.md_
- **Named booleans.** Name the parts of a truth-table condition as booleans. _Sources: docs/agents/code-review/typescript.md_
- **One async style.** Use `await` throughout instead of mixing it with `.then()` chains. _Sources: docs/agents/code-review/typescript.md_
- **No nested ternaries.** Replace nested ternaries with named steps or early returns. _Sources: docs/agents/code-review/typescript.md_
- **Possibly-undefined values.** Flag `array[i]`, `map.get`, `find`, optional fields, and parsed JSON treated as present. _Sources: docs/agents/code-review/typescript.md_
- **Empty array traps.** Guard `reduce` without an initial value, `arr[0]`, and `Math.max(...[])` against empty arrays. _Sources: docs/agents/code-review/typescript.md_
- **Handled rejections.** Flag `forEach(async ...)` and unawaited calls inside `try`. _Sources: docs/agents/code-review/typescript.md_
- **Finite number checks.** Check that `Number` or `parseInt` of a user string is finite. _Sources: docs/agents/code-review/typescript.md_
- **Date pitfalls.** Flag timezone assumptions, `new Date(string)` on non-ISO strings, and hand-rolled month arithmetic. _Sources: docs/agents/code-review/typescript.md_
- **Id type mismatch.** Flag string comparisons between ids of different types. _Sources: docs/agents/code-review/typescript.md_
- **Map/Set lookups.** Replace nested lookups with a `Map` or `Set` to avoid O(n²). _Sources: docs/agents/code-review/typescript.md_
- **Single pass over chains.** Collapse repeated `filter`/`map`/`find` chains into one pass. _Sources: docs/agents/code-review/typescript.md_
- **Single-pass min/max.** Find a min or max in one pass instead of `sort()[0]`. _Sources: docs/agents/code-review/typescript.md_
- **No string concatenation in loops.** Build strings in loops with an array join instead of repeated concatenation. _Sources: docs/agents/code-review/typescript.md_
- **No per-iteration copies.** Flag `[...arr]` and spreads inside reducers that copy on every iteration. _Sources: docs/agents/code-review/typescript.md_
- **No whole-collection loads.** Fetch a count, sum, or single item directly instead of loading the whole collection. _Sources: docs/agents/code-review/typescript.md_
- **Bound caches.** Give every cache `Map` an eviction bound. _Sources: docs/agents/code-review/typescript.md_
- **Concurrency limit.** Cap concurrency when running `Promise.all` over an unbounded list. _Sources: docs/agents/code-review/typescript.md_
- **Depth-bounded recursion.** Bound the depth of recursion over user-sized input. _Sources: docs/agents/code-review/typescript.md_
- **Idempotent side effects.** Use a natural key, an upsert, or an idempotency token for writes that can be retried. _Sources: docs/agents/code-review/typescript.md_
- **Do not mutate inputs.** Copy before changing a value a caller passed in. _Sources: docs/agents/code-review/typescript.md_
- **No import-time mutable state.** Flag module-level mutable state initialised on import. _Sources: docs/agents/code-review/typescript.md_
- **No shared server module state.** Flag mutable module state shared across requests in a server process. _Sources: docs/agents/code-review/typescript.md_
- **Escape user strings.** Escape or allow-list user strings used in shell commands, paths, regexes, and URLs. _Sources: docs/agents/code-review/typescript.md_
- **Path containment.** Check that a path joined from user input stays inside the intended directory. _Sources: docs/agents/code-review/typescript.md_
- **Validate parsed JSON.** Validate `JSON.parse` of external input against a schema. _Sources: docs/agents/code-review/typescript.md_
- **Map for user keys.** Key user-supplied data with a `Map` instead of an object, where `__proto__` and `constructor` are traps. _Sources: docs/agents/code-review/typescript.md_
- **No raw echo in errors.** Keep raw input and internals out of error messages. _Sources: docs/agents/code-review/typescript.md_
- **Await-spanning read-modify-write.** Flag a read-modify-write on shared state with an `await` between the read and the write. _Sources: docs/agents/code-review/typescript.md_
- **Existence-check races.** Flag concurrent "does not exist" checks that race the inserts they guard. _Sources: docs/agents/code-review/typescript.md_
- **Clean up handlers and timers.** Remove old handlers and timers before re-registering so they do not fire twice. _Sources: docs/agents/code-review/typescript.md_

## Where it lives

Every rule in this category lives in the four stack files under `docs/agents/code-review/` (`drizzle.md`, `react.md`, `tanstack-start.md`, `typescript.md`), which `docs/agents/code-review.md` tells reviewers to load when their `detect` entries match the repo. No rule here appears in AGENTS.md or inside any skill's SKILL.md; the review-pr, review-loop, arbitrate-review, and author-ticket skills reach the stack files only through `docs/agents/code-review.md`.
