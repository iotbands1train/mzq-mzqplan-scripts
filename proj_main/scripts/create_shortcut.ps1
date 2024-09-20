# Define the target PowerShell script path
$targetPath = "D:\dev\d_drive\proj_main\scripts\run_main.ps1"

# Define the location for the shortcut on the desktop
$desktopPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath("Desktop"), "Web_Gen_syncer.lnk")

# Create a WScript.Shell COM object
$wshShell = New-Object -ComObject WScript.Shell

# Create the shortcut object
$shortcut = $wshShell.CreateShortcut($desktopPath)

# Set the target path of the shortcut
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-File `"$targetPath`""
$shortcut.IconLocation = "powershell.exe,0"

# Save the shortcut
$shortcut.Save()

Write-Output "Shortcut created at $desktopPath"
