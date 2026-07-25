# AOS Development Setup

This guide describes the verified local development environment for the AOS Platform on Odoo 18 Community.

## Prerequisites

- Supported Windows development workstation
- Python 3.12
- PostgreSQL
- Git
- Visual Studio Code
- Odoo 18 Community source at `D:\Odoo\odoo`

wkhtmltopdf is not currently installed. PDF reports are unavailable, but this does not block normal custom-module development.

## Windows Version

- Edition: Windows 11 Pro
- Version: 25H2
- OS build: 26200.8875
- Architecture: x64

Windows retains a legacy `Windows 10 Pro` product name in the system registry for this build.

## Python Version

AOS uses Python 3.12.10.

```text
D:\Odoo\venv\Scripts\python.exe
```

Use this interpreter for all Odoo commands. Do not install project dependencies into the system Python environment.

## PostgreSQL

- PostgreSQL version: 17.10
- Host: `localhost`
- Port: `5432`
- Odoo database role: `odoo18`

The PostgreSQL command-line tools are installed under:

```text
C:\Program Files\PostgreSQL\17\bin
```

That directory is not currently on `PATH`, so use its full path when running `psql` or add it to the user `PATH`.

Database credentials are maintained in the local Odoo configuration and should not be copied into documentation or committed to a public repository.

## Odoo Version

- Edition: Odoo 18 Community
- Server version: 18.0
- Source location: `D:\Odoo\odoo`
- Entry point: `D:\Odoo\odoo\odoo-bin`

The Odoo source code is treated as an external dependency and must never be modified. All AOS custom modules belong in `D:\Odoo\AOS\addons`.

## Virtual Environment

The Python virtual environment is located at:

```text
D:\Odoo\venv
```

Activate it from PowerShell when an interactive environment is useful:

```powershell
cd D:\Odoo
.\venv\Scripts\Activate.ps1
```

Activation is optional when commands invoke `D:\Odoo\venv\Scripts\python.exe` directly.

### Installing Odoo Requirements

With the virtual environment activated, install the Odoo 18 Community requirements:

```powershell
cd D:\Odoo
.\venv\Scripts\python.exe -m pip install -r .\odoo\requirements.txt
```

Do not add external packages beyond Odoo requirements without explicit project approval.

### PostgreSQL Configuration

Create a local PostgreSQL role and development database appropriate for Odoo. The confirmed development database is `aos`.

Copy `D:\Odoo\AOS\config\odoo.conf.example` to `D:\Odoo\AOS\config\odoo.conf`, then replace placeholder credentials locally. Never commit the local configuration or expose its database and Odoo master passwords.

## VS Code

The verified Visual Studio Code version is 1.130.0 x64.

Open `D:\Odoo` as the workspace folder. Shared editor configuration is stored in:

```text
D:\Odoo\.vscode\settings.json
D:\Odoo\.vscode\launch.json
```

The workspace selects `D:\Odoo\venv\Scripts\python.exe` and provides the **Run AOS - Odoo 18** debug configuration. Start it from the **Run and Debug** view or press `F5`.

To select the interpreter manually, run **Python: Select Interpreter** in the Command Palette and choose:

```text
D:\Odoo\venv\Scripts\python.exe
```

## Required Extensions

The following installed extensions support the current Python and Odoo workflow:

- Python: `ms-python.python`
- Pylance: `ms-python.vscode-pylance`
- Python Debugger: `ms-python.debugpy`

The installed Ruff and Black Formatter extensions may assist with Python quality and formatting, but project formatting must remain compatible with Odoo conventions and PEP 8.

## Running Odoo

Ensure PostgreSQL is running, then execute:

```powershell
cd D:\Odoo
.\venv\Scripts\python.exe .\odoo\odoo-bin -c .\AOS\config\odoo.conf
```

Open the application at:

```text
http://localhost:8069
```

Runtime configuration is read from `D:\Odoo\AOS\config\odoo.conf`, and logs are written to `D:\Odoo\AOS\logs\odoo.log`.

## Updating the Apps List

1. Start Odoo and sign in to the `aos` database as an administrator.
2. Enable developer mode.
3. Open **Apps**.
4. Use **Update Apps List** and confirm the update.
5. Remove the default Apps filter when searching for technical modules such as `aos_base`.

## Installing and Upgrading Custom Modules

Stop the running development server before performing a command-line update. Replace `aos` with the intended development database when necessary.

Update one module:

```powershell
cd D:\Odoo
.\venv\Scripts\python.exe .\odoo\odoo-bin -c .\AOS\config\odoo.conf -d aos -u aos_base --stop-after-init
```

Install a new module:

```powershell
cd D:\Odoo
.\venv\Scripts\python.exe .\odoo\odoo-bin -c .\AOS\config\odoo.conf -d aos -i module_name --stop-after-init
```

Use `-u all` only when a full update is deliberate and its impact has been reviewed.

## Common Commands

Check Python:

```powershell
.\venv\Scripts\python.exe --version
```

Check Odoo:

```powershell
.\venv\Scripts\python.exe .\odoo\odoo-bin --version
```

Run Odoo with development features:

```powershell
.\venv\Scripts\python.exe .\odoo\odoo-bin -c .\AOS\config\odoo.conf --dev=all
```

Run module tests in an isolated test database:

```powershell
.\venv\Scripts\python.exe .\odoo\odoo-bin -c .\AOS\config\odoo.conf -d aos_test -i module_name --test-enable --stop-after-init
```

View recent log entries:

```powershell
Get-Content .\AOS\logs\odoo.log -Tail 100
```

List custom modules:

```powershell
Get-ChildItem .\AOS\addons -Directory
```

## Troubleshooting

### Odoo cannot connect to PostgreSQL

- Confirm the PostgreSQL service is running.
- Verify the host, port, role, and password in `D:\Odoo\AOS\config\odoo.conf`.
- Confirm the selected database exists and the `odoo18` role has access to it.

### A custom module is not visible

- Confirm the module is inside `D:\Odoo\AOS\addons`.
- Confirm the custom addons path is present in `addons_path`.
- Validate the module manifest and ensure `installable` is `True`.
- Restart Odoo and update the Apps list.

### Port 8069 is already in use

- Stop the other Odoo process, or run the development instance with a different port:

```powershell
.\venv\Scripts\python.exe .\odoo\odoo-bin -c .\AOS\config\odoo.conf --http-port=8070
```

### Python imports or dependencies fail

- Confirm commands use `D:\Odoo\venv\Scripts\python.exe`.
- Confirm VS Code has selected the same interpreter.
- Do not add external Python packages without explicit project approval.

### Changes do not appear

- Restart the development server after Python changes.
- Update the affected module after manifest, model, security, data, or view changes.
- Use `--dev=all` during active development when automatic reload behavior is appropriate.

### Odoo fails during startup or module update

Review the latest entries in:

```text
D:\Odoo\AOS\logs\odoo.log
```

Resolve the first relevant Python, XML, dependency, database, or access-control error before retrying.
