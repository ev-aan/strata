# Starting a dig step from the site

Any claim on stratah.org with open work (a `next_step`, usually on a `searched_gap`) shows a **Start this step →** link.

## What happens when you click it
1. GitHub opens a pre-filled "Start a dig step" issue. GitHub handles sign-in, so there are no separate Stratah accounts yet.
2. You submit the issue. It carries the label `dig:start`.
3. **If you have write access to the repository** (the owner and invited collaborators), the workflow `.github/workflows/dig-agent.yml` starts Claude. Claude reads the rules and the dig, works the step, runs the conformance check and opens a **draft pull request**. It then posts the PR link and a short summary on the issue.
4. You review the pull request. Merge it to accept the work, close it to reject it. Nothing reaches the public site until a merge to `main` passes the conformance gate.
5. If the person has no write access, the agent does not run. The issue stays as a suggestion for a maintainer.

## One-time setup (owner)
1. **Add the token.** On your computer, run `claude setup-token` in Terminal (Claude Code must be installed). This prints a long-lived token tied to your Claude subscription. Then go to the repository on GitHub, **Settings → Secrets and variables → Actions → New repository secret**, and add it with the name `CLAUDE_CODE_OAUTH_TOKEN`.
   - Alternatively, use an Anthropic API key (pay per use). Name the secret `ANTHROPIC_API_KEY` and change `claude_code_oauth_token:` to `anthropic_api_key:` in the workflow.
2. **Install the Claude GitHub app** on the repository: https://github.com/apps/claude.
3. **Allow Actions to open pull requests:** **Settings → Actions → General → Workflow permissions**. Choose "Read and write permissions" and tick "Allow GitHub Actions to create and approve pull requests".
4. **Invite trusted contributors:** **Settings → Collaborators → Add people**. Write access is what lets their clicks reach the agent.

## Limits that keep it honest
- The agent may change only the named subject's YAML and log. It may not touch the rules, the generator or the workflows.
- It must say what it could not read. Unreachable sources stay `searched_gap` with a precise `next_step`, never a guessed answer.
- Every run is capped (`--max-turns 60`, 60 minutes) to bound cost.
