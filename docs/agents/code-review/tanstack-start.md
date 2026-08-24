---
detect:
  - dep:@tanstack/react-start
---

# TanStack Start checks

Covers server functions, router loaders, and TanStack Query used with Start.

## Idiomatic

- Server functions declared with `createServerFn({ method }).middleware([...]).validator(schema).handler(...)`; `GET` for reads, `POST` for writes.
- Route data through `context` returning query options plus `loader` calling `queryClient.fetchQuery` or `ensureQueryData`, and `useSuspenseQuery` in the component. `useEffect` fetching in a route component is a finding.
- `pendingComponent` and `errorComponent` on routes that load data.
- Mutations through `useMutation` in a `*.mutations.ts` module with `invalidateQueries` on success, not manual refetches.
- Route params and search params typed and validated with `validateSearch` and `params.parse`.

## Maintainable

- Server-function modules hold no database code; they validate and delegate to a server module that takes the context values it needs as parameters.
- Query keys built from one factory per domain, never inline arrays in components.
- Middleware composed once and reused, not re-declared per server function.

## Cognitive Load

- Handlers that unpack `context`, branch on permissions, and run queries in one body.
- Loaders that fetch, transform, and redirect in one function.

## Edge Cases

- Loader throwing on not-found without `notFound()`, leaving the user a blank page.
- Server functions returning `undefined` on a miss where the client expects an object.
- `redirect()` thrown inside a `try` that swallows it.
- Search-param defaults that differ between the validator and the component.
- Errors thrown from handlers that reach the client with internal messages or stack details.

## Complexity

- Sequential `await` in a loader or `beforeLoad` on independent queries; `Promise.all` them.
- Each server function re-running session lookup and permission checks that a shared middleware already ran on the same request.
- `staleTime` of zero on data that rarely changes, refetching on every mount and focus.
- Query options that select or transform large payloads on every render without `select`.

## Idempotent

- `POST` server functions whose retry (network error, double click, React StrictMode double effect) repeats a write. Look for a natural key or an upsert.
- Mutations fired from `useEffect` or a loader.
- `onSuccess` handlers that navigate or toast twice when the mutation is retried.

## Scalable

- Server functions returning whole collections with no pagination or filter argument.
- Client-side filtering of a list the server should filter.
- Loaders that prefetch data the route doesn't render.

## Sanitization

- Server functions without `.validator(...)`; every input crosses a network boundary. Missing validation is high risk on `POST`.
- Validators that accept extra keys forwarded straight into an insert (`...data` into `values`).
- Redirect targets built from search params without an allow-list of internal paths.
- Values from `headers` or `request` used in queries without validation.

## Thread-safe

- Mutations whose button stays enabled while `isPending`.
- Optimistic updates without `onError` rollback, or `onMutate` that cancels no in-flight query.
- Two mutations on the same entity racing their invalidations, leaving the cache on the older response.
- Server functions reading then writing shared rows without a transaction.
