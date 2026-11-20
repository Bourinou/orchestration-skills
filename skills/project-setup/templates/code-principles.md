---
name: code-principles
description: How to apply KISS, DRY and SOLID correctly in {{PROJECT}} - what each principle means, the concrete signs it is broken, and the signs it is being over-applied. Use before writing or refactoring code, before every commit, and when reviewing a diff.
---

# Code principles — {{PROJECT}}

These principles exist to make code **easier to change correctly**. Apply them to the code you write or touch in your plan, not to the whole repo (out-of-scope cleanups go to `Docs/PROGRESS.md` “Later”). When two principles pull in different directions, the order is **KISS > DRY > SOLID**: the simplest code that is correct, readable and testable wins. The project's architecture rules (CLAUDE.md) override everything here.

Before committing, check your diff against each “broken” list below. Fix what you find, or write in your PROGRESS entry why you kept it.

## KISS — Keep It Simple

**Means**: the simplest solution that meets today's requirements. Code is read far more often than it is written.

**Broken when**:
- An abstraction (interface, base class, factory, generic, config option, plugin point) has **one** implementation or caller and no planned second one in `PLAN.md`.
- Code handles cases no requirement, test or caller needs (“just in case”, YAGNI).
- A function is hard to name, longer than one screen, nested more than ~3 levels, or takes boolean flags that switch its behaviour.
- Clever code (dense one-liners, metaprogramming, reflection) where plain code works.
- A dependency is added for something a few lines of standard library do.

**Do**: plain functions and data first; early returns; descriptive names; one level of abstraction per function; delete dead code instead of commenting it out.

**Over-applied when**: simplicity becomes copy-paste, magic values, or skipped error handling. Simple ≠ incomplete.

## DRY — Don't Repeat Yourself

**Means**: every piece of **knowledge** (a business rule, a formula, a constant, a format, a schema) has one authoritative place. It is about knowledge, not about lines that look alike.

**Broken when**:
- The same rule or constant is written in two places, so changing it means finding both (validation duplicated in client and server without a shared source, the same magic number in several files, a copied block with one value changed).
- A fact derivable from another is stored and maintained by hand (types and schema, docs and code, a count kept next to a list).

**Do**: extract when the **third** real repetition appears (rule of three), or at the second if it is a business rule that must change everywhere at once. Name the extracted thing after the knowledge it holds.

**Over-applied when**: two pieces of code look alike but would change for **different reasons**. Merging them couples unrelated features, and the shared function grows flags and `if (caseA)`. Prefer a little duplication over the wrong abstraction. Tests may repeat setup when it makes each test readable on its own.

## SOLID

Apply SOLID where code has real variation or real boundaries (modules, layers, external services). Don't add interfaces or layers for code with a single, stable implementation (KISS wins).

### S — Single Responsibility
**Means**: a module, class or function has **one reason to change**: it serves one actor or concern.
**Broken when**: the name needs “and”, “Manager”, “Utils” or “Helper” to cover it; one file mixes I/O (HTTP, DB, files, UI) with business rules; a change for one feature forces edits in unrelated parts of the same unit.
**Do**: separate decisions (pure logic) from effects (I/O) so the logic is testable without mocks.

### O — Open/Closed
**Means**: when a **known axis of variation** gets a new case, you can add it by adding code, without editing working code.
**Broken when**: every new variant means editing the same growing `switch`/`if` chain in several places.
**Do**: introduce the extension point (strategy, map of handlers, polymorphism) **when the second variant actually arrives**, not before. One `switch` in one place is fine.

### L — Liskov Substitution
**Means**: any subtype or implementation can replace its parent or interface without the caller noticing.
**Broken when**: an override throws “not supported”, ignores arguments, narrows accepted inputs, widens what it returns or throws, or callers check the concrete type (`instanceof`, type switches).
**Do**: if a subtype can't honour the whole contract, it isn't a subtype: use composition or a smaller interface.

### I — Interface Segregation
**Means**: callers depend only on the methods they use.
**Broken when**: implementations leave methods empty or throwing; a test fake must implement many methods it never calls; one interface serves several unrelated clients.
**Do**: small, role-named interfaces defined by what the **caller** needs.

### D — Dependency Inversion
**Means**: business logic depends on abstractions it owns, not on concrete infrastructure; the dependency arrow points from details (DB, HTTP, framework, clock, randomness) toward the core.
**Broken when**: core logic instantiates or imports infrastructure directly (`new HttpClient()`, a global DB handle, `Date.now()`), so it can't be tested without the real thing.
**Do**: pass dependencies in (constructor or parameter); wire concrete ones at the edge (entry point, composition root). Don't wrap stable standard-library calls that are not I/O.

## Review checklist (for the reviewer)

Report only violations **introduced or worsened by the diff**, each with file:line, the principle, the concrete harm (what change becomes harder or riskier) and the smallest fix. A principle broken with no concrete harm is a Nit, not Important. Over-application (needless abstraction, premature DRY) is a violation too.
