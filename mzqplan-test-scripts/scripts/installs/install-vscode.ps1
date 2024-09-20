# PowerShell script to install Visual Studio Code

# Enable script execution
Set-ExecutionPolicy Unrestricted -Force

# Function to log messages
function Log-Message {
    param (
        [string]$message
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Output "$timestamp - $message"
}

Log-Message "Starting Visual Studio Code installation script."

# Install Chocolatey if not installed
if (-not (Get-Command choco.exe -ErrorAction SilentlyContinue)) {
    Log-Message "Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    Start-Sleep -Seconds 30
}

# Install Visual Studio Code
Log-Message "Installing Visual Studio Code..."
choco install vscode -y

Log-Message "Visual Studio Code installation script completed."
