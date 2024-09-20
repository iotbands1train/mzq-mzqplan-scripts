# Define the URL to download the Python installer
$pythonInstallerUrl = "https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe"

# Define the path to save the downloaded installer
$installerPath = "$env:TEMP\python-3.9.6-amd64.exe"

# Download the Python installer
Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $installerPath

# Run the installer silently
Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait

# Verify the installation
$pythonVersion = python --version

if ($pythonVersion) {
    Write-Output "Python installed successfully. Version: $pythonVersion"
} else {
    Write-Output "Python installation failed."
}