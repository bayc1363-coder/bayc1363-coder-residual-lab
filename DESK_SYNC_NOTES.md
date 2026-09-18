# DESK_SYNC — residual-lab scorer retune 3f34030

## Status
- Box `/workspace/residual-lab` updated from CloudAgent transcript reconstruction of commit **3f34030**.
- **Desk NOT synced** from this executor: no `machineId` / `CopyFromBox` tools available on this subagent.
- Tarball ready: `/tmp/residual-lab-scorer-retune.tgz`

## Desk target
- machineId: `3f0c1d3a-4375-46d4-9d47-641c121f2488`
- Path: `C:\Users\bocst\projects\residual-lab`

## Parent should
1. Use Shell with machineId (or CopyFromBox) to extract tarball onto desk, OR
2. On desk: `git pull origin main` when origin auth available (`https://origin.cursor.com/git/bored-mint/tmp-40246f1c3693dfbb.git`).
3. Confirm symbols: `idea_variety`, `soft_rank_openness`, `demotion_flags`, `SCORING.md`
4. Optional: `py -3 -m pytest` (23 green on box + CloudAgent)

## Do NOT
- Public-deploy EqualResolution
