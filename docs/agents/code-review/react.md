---
detect:
  - dep:react
---

# React checks

## Idiomatic

- Derived values computed during render, not stored in state and synced with `useEffect`.
- Server or async state through the data library (query or loader), not `useEffect` plus `useState` plus `fetch`.
- `useEffect` only for syncing with something outside React (DOM, subscriptions, timers). An effect that only sets state from props is a finding.
- React 19 forms: `action` props, `useActionState`, `useOptimistic`, `useFormStatus` over hand-rolled submit handlers and loading flags where the framework supports them.
- `ref` as a prop; `forwardRef` is legacy in React 19.
- `key` from a stable id, never from the array index when items reorder or get removed.
- Composition (children, slots) over boolean props that switch layout.

## Maintainable

- Components above roughly 150 lines or with more than five pieces of state; split by responsibility.
- Prop drilling more than two levels for data a context or a colocated hook should own.
- Custom hooks named for what they return (`useCaseList`), containing every piece of state that changes together.
- Inline object and function literals passed to memoised children, defeating the memo.
- Conditional rendering that returns three or more different trees from one component.

## Cognitive Load

- JSX nested more than four levels with logic inside; extract a named component.
- Multiple `useEffect` calls whose ordering matters.
- Handlers that read and write more than three state variables.
- Boolean-flag soup (`isLoading && !error && data && !isEmpty`); model as a status union.

## Edge Cases

- Missing loading, empty, and error branches on data-driven UI.
- Effects that set state after unmount or after a newer request resolved (race between two fetches; keep the latest with an ignore flag or abort controller).
- Effects without cleanup for subscriptions, listeners, timers, observers.
- Lists that assume at least one item (`items[0]`).
- Controlled inputs switching to uncontrolled when value becomes `undefined`.
- Forms that can submit twice before the first request resolves.

## Complexity

- Work done on every render that only depends on props or state that rarely change: heavy filtering, sorting, formatting of large lists. `useMemo` when measured, or move it out of the component.
- Rendering a list of hundreds of rows without virtualisation or pagination.
- Context values recreated every render, re-rendering every consumer.
- State held at a level that re-renders a large subtree on every keystroke.

## Idempotent

- Effects that must survive React's double-invoke in StrictMode: a subscribe/unsubscribe pair, a fetch that can run twice, a mutation fired from an effect.
- Mutations triggered on mount or on a dependency change instead of on a user action.

## Scalable

- Unbounded client-side state: whole tables loaded then filtered in the browser.
- Search or filter inputs that fire a request on every keystroke without debounce or request cancellation.
- Images and assets without size hints or lazy loading in long lists.

## Sanitization

- `dangerouslySetInnerHTML` with anything that came from a user, an API, or markdown, without a sanitiser.
- `href` and `src` built from user input; `javascript:` and `data:` schemes get through string concatenation.
- User content rendered into `<a target="_blank">` without `rel="noopener"` where the browser doesn't default it.
- Secrets or server-only values imported into client components.

## Thread-safe

- Double submit: a button that stays enabled while its mutation is pending.
- Optimistic updates without rollback on failure, or two optimistic updates on the same entity.
- Stale closure: a handler or effect reading state captured at an earlier render (missing dependency, or a setter that should use the functional form).
- Two components each owning a copy of the same server entity and writing back independently.
