# Allure Report Generation Scripts

This directory contains scripts for generating and managing Allure reports.

## Windows Scripts (.bat)

- **gerar_allure.bat** - Generate Allure HTML report and open in browser
- **allure_server.bat** - Start Allure local server on port 4040
- **limpar_allure.bat** - Clean old Allure results and reports

### Usage (Windows)
```cmd
cd scripts
gerar_allure.bat
```

## Unix/Linux/macOS Scripts (.sh)

- **gerar_allure.sh** - Generate Allure HTML report and open in browser
- **allure_server.sh** - Start Allure local server on port 4040
- **limpar_allure.sh** - Clean old Allure results and reports

### First Time Setup (Unix/Linux/macOS)

Make the scripts executable:
```bash
chmod +x scripts/gerar_allure.sh
chmod +x scripts/allure_server.sh
chmod +x scripts/limpar_allure.sh
```

### Usage (Unix/Linux/macOS)
```bash
cd scripts
./gerar_allure.sh
```

## Prerequisites

All scripts require Allure CLI to be installed. Installation instructions:

### Windows
```cmd
# Using Scoop
scoop install allure

# Using npm
npm install -g allure-commandline
```

### macOS
```bash
# Using Homebrew
brew install allure
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

### Verify Installation
```bash
allure --version
```

## Workflow

1. **Run tests** to generate Allure results:
   ```bash
   pytest tests/ --alluredir=reports/allure-results
   ```

2. **Generate report** (choose one):
   - Static HTML report: `gerar_allure.bat` or `./gerar_allure.sh`
   - Live server: `allure_server.bat` or `./allure_server.sh`

3. **Clean old results** (optional):
   ```bash
   limpar_allure.bat  # Windows
   ./limpar_allure.sh # Unix
   ```

## Troubleshooting

### "Allure CLI not found"
Install Allure CLI using one of the methods above.

### "No test results found"
Run tests first: `pytest tests/ --alluredir=reports/allure-results`

### "Permission denied" (Unix)
Make scripts executable: `chmod +x scripts/*.sh`

### Port 4040 already in use
Stop the existing Allure server or change the port in the script.
