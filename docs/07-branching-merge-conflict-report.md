# 07 - Git Branching & Deliberate Merge Conflict Resolution Report

**Project Title**: Puppet-Provisioned Supplier Quality Review Portal  
**Author**: Aaditya Aswale (Student ID: 23102B0044)  
**Academic Requirement**: Week 5 & Week 6 Practical Git Lab  
**Artifact Hash**: Resolved at Commit `af4e09d`

---

## 1. Objective of the Merge Conflict Simulation

In enterprise engineering teams, multiple engineers concurrently edit shared configuration files, documentation, and database migration routines. A critical competency in DevOps is the systematic detection, isolation, manual reconciliation, and resolution of three-way merge conflicts (`merge-ort` engine) without losing functional code or historical intent.

---

## 2. Step-by-Step Conflict Simulation Protocol

### Step 1: Branch Creation
A dedicated feature branch named `feature/conflict-demo` was branched from `develop`:
```bash
git checkout -b feature/conflict-demo develop
```

### Step 2: Conflicting Edit on Feature Branch
In `README.md`, lines 18–25 were edited to introduce the following text:
```markdown
### Feature Branch Evaluation Note
This section was created in feature/conflict-demo to demonstrate deliberate conflict generation.
Reviewer: Aaditya Aswale (Evaluation Mode Active)
```
The change was committed with message:
```bash
git commit -am "docs: add conflict branch evaluation note to README"
# Resulting SHA: 7c65fd1
```

### Step 3: Divergent Edit on `develop` Branch
Switching back to `develop`, the exact same lines in `README.md` were modified with divergent production release candidate text:
```bash
git checkout develop
```
Content inserted into `README.md`:
```markdown
### Production Release Candidate Note
This section was updated directly in develop to prepare for release v1.0.0.
Status: Verification In Progress
```
The change was committed with message:
```bash
git commit -am "docs: add develop release candidate note to README"
# Resulting SHA: 1a30036
```

---

## 3. Conflict Triggering & Diagnostic Output

When merging `feature/conflict-demo` back into `develop`:
```bash
git merge feature/conflict-demo
```

### Terminal Output:
```text
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
```

`git status` inspection confirmed:
```text
On branch develop
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   README.md
```

---

## 4. Conflict Markup & Manual Resolution

Inspection of `README.md` revealed the three-way conflict markers injected by Git:
```diff
<<<<<<< HEAD
### Production Release Candidate Note
This section was updated directly in develop to prepare for release v1.0.0.
Status: Verification In Progress
=======
### Feature Branch Evaluation Note
This section was created in feature/conflict-demo to demonstrate deliberate conflict generation.
Reviewer: Aaditya Aswale (Evaluation Mode Active)
>>>>>>> feature/conflict-demo
```

### Manual Synthesis Decision:
Rather than choosing one side and discarding the other, both operational notes were integrated with explicit attribution, demonstrating professional resolution practices:

```markdown
### Release Candidate & Verification Status
- **Target Release**: v1.0.0 Production Baseline
- **Evaluation Committee**: Continuous Testing Verified
- **Lead Developer**: Aaditya Aswale (Student ID: 23102B0044)
- **Git Demonstration**: Conflict between feature/conflict-demo (7c65fd1) and develop (1a30036) reconciled cleanly.
```

### Staging and Final Commit:
```bash
git add README.md
git commit -m "fix(git): resolve merge conflict in README between develop and feature/conflict-demo"
# Resulting Merge Commit SHA: af4e09d
```

---

## 5. Architectural Verification & Conclusion

Following the merge resolution:
1. `git status` returned working tree clean.
2. The complete Git tree reflects the dual-parent merge commit `af4e09d`.
3. Subsequent release tagging `v1.0.0` was executed on `main` following full synchronization.
