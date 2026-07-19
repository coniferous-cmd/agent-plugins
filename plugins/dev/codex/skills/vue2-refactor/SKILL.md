---
name: vue2-refactor
description: Split a large Vue 2 single-file page into focused child components coordinated by index.vue, while preserving behavior, APIs, events, styles, routing, and Vue 2 compatibility.
disable-model-invocation: false
---

# Vue 2 Page Refactor

Refactor target: $ARGUMENTS

## Goal

Reduce the complexity of large `.vue` files while keeping user-observable behavior unchanged.

## Investigation

1. Read the full target page, not just the template.
2. Mark template, props, data, computed, watch, lifecycle, and methods.
3. Locate routes, APIs, Vuex, mixins, filters, directives, and shared components.
4. Record event names, refs, slots, form validation, uploads, dialogs, and style scope.
5. Find tests, screenshots, or runnable verification approaches.
6. Check Vue 2 limitations and avoid Vue 3-only APIs.

## Splitting principles

- `index.vue` retains page-level data fetching, route coordination, and cross-component state.
- Pure presentation sections receive input via props and output via events.
- Search areas, statistics areas, tables, drawers, dialogs, and upload areas are candidate components.
- Do not force a split for the sake of line count when state is tightly shared.
- Keep API call counts, timing, and parameters unchanged.
- Preserve `$emit` names, payloads, `.sync`, `v-model`, and ref behavior.
- Keep Element UI and similar component libraries written in Vue 2 style.
- When using deep selectors in scoped styles, follow the project's existing syntax.
- Do not migrate to the Composition API or Vue 3 in the same work package.

## Execution

1. Have `analyst` produce a responsibility map and dependency graph.
2. Have `task-orchestrator` determine component boundaries and migration order.
3. Extract one responsibility at a time; keep the page runnable after each step.
4. Child components define clear props, events, and default values.
5. Use `coder` for implementation and `test-generator` to add behavior tests.
6. `reviewer` focuses on events, reactivity pitfalls, styles, refs, and lifecycle changes.

## Acceptance

- Page behavior, interfaces, routing, and visuals remain consistent.
- No Vue 3 syntax.
- Each child component has a single responsibility and a clear interface.
- Original file complexity drops significantly without creating meaningless fragments.