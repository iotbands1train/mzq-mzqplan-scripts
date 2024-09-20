# PowerShell script to install MySQL

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

Log-Message "Starting MySQL installation script."

# Install Chocolatey if not installed
if (-not (Get-Command choco.exe -ErrorAction SilentlyContinue)) {
    Log-Message "Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    Start-Sleep -Seconds 30
}

# Install MySQL
Log-Message "Installing MySQL..."
choco install mysql -y

Log-Message "MySQL installation script completed."
