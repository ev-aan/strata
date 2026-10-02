# Changing the schema, validator or rules: proposals only

**No one changes the schema, the validator or the rules without a proposal that meets the standards below. This binds the owner too.** The owner still has the final say (docs/GOVERNANCE.md), but the say is on a proposal that has met the standards, never on a preference. Agents never make these changes.

## A proposal must contain
1. **The failure case.** A concrete case, with files and claim ids, where the current rules produce a wrong, misleading or unusable result. "I would prefer this wording or outcome" is not a failure case.
2. **The evidence.** What was checked, with sources opened and the output shown (for example a validator run or a diff). Not an argument from authority or popularity.
3. **The proposed change,** stated exactly: the new or changed rule, its text in `build/SCHEMA.md`, and the validator check that enforces it.
4. **What it does not change.** In particular, that it does not alter what any existing finding says without a logged review.
5. **Impact.** Every existing dig affected, with the validator result before and after, and the migration for each.
6. **Alternatives considered,** including doing nothing, and why they were rejected.
7. **A neutrality check.** The change must not favour any outcome, topic or answer. Test it on at least two digs that point in different directions.

## Process
1. Write the proposal as a file in `docs/proposals/<short-name>.md` on a `process/<topic>` branch and open a pull request.
2. An independent reviewer, who did not write it, checks the seven points against the repository and records the result in the pull request.
3. The owner decides. The decision and its reason are logged on the pull request, whichever way it goes.
4. Only then is the change made, in its own commit, with the validator updated in the same change.

A rule that fails to meet the standards is declined with the reason recorded. Urgent fixes to a validator bug follow the same path with the failing case attached.
