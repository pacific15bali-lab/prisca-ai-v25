# Prisca AI V25

Windows one-click build for the Prisca AI Operations Manager.

The repository contains the V25 source ZIP and a GitHub Actions workflow that builds a Windows executable on a GitHub-hosted Windows runner.

## Build

Open Actions, select "Build Prisca V25 for Windows", then choose "Run workflow".

The workflow produces Prisca_V25_Windows_One_Click.zip.

Extract the artifact and double-click START_PRISCA.exe.

The browser opens automatically at http://127.0.0.1:8765.

No Python installation is required on the machine running the built artifact.
