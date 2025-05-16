Any PR title can be optionally prefixed with `breaking|` and must include one of `{ feat | fix | refactor  | tests | chore }` followed by a `colon` and `brief description`.

Examples:
* refactor: I am rearranging methods and modules
* fix: I found a bug and resolved it
* breaking|feat: I've got big changes and there is no going back

# ---My PR---

Include a brief and descriptive header for your pull request.

## Summary

Please proivde a 1-2 sentence summary of your changes and link your relevant Jira issue (if applicable).

Examples:
* yum!:
  * Adds a new "timestamp" field to the "trace" object schema, allowing easier filtering and sorting of traces
* yuck!:
  * Changes the 'trace' object schema

## Included Change(s)
- [ ] new feature (non-breaking, added functionality)
- [ ] bug fix (non-breaking, resolves a problem)
- [ ] Breaking change (any code update that is not backwards compatible)
- [ ] Code documentation update

* NOTE: Most PRs will include multiple of the above options.

## Details

Use this space to provide more details about your changes. Consider providing the context around your solution as well as any potential trade-offs or limitations. Ensure that your changes align with the overall architecture and maintainability of the system. Additionally, describe how your changes impact the system's performance and scalability.

## Unit/Integration/Manual Testing

Describe any added unit/integration tests along with manual testing performed to validate your changes.

## 3rd Party Documentation

* provide bulleted links to relevant documentation

## Checklist
- [ ] My changes include unit tests.
- [ ] My changes include integration tests.
- [ ] Manual tests sufficiently cover all scenarios.
- [ ] Added code is clearly documented.
- [ ] I have done my best to ensure that my changes are easy to maintain and scale.
