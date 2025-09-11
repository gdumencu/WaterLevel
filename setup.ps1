# Run as administrator in the WaterLevel root folder

# Install Chocolatey if not present
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
   // iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
   Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

}

# Install core tools
choco install -y python nodejs-lts postgresql docker-desktop vscode git

# VSCode extensions (optional)
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-azuretools.vscode-docker
code --install-extension esbenp.prettier-vscode
code --install-extension dbaeumer.vscode-eslint

Write-Host "Core tools installed. Please restart your computer if Docker Desktop or PostgreSQL were just installed."
