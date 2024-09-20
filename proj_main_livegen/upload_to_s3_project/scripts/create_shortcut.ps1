# Path to the Python executable
$pythonPath = "D:\dev\d_drive\.venv\Scripts\python.exe"

# Path to the main.py script
$scriptPath = "D:\dev\d_drive\proj_main_livegen\upload_to_s3_project\src\main.py"

# Path to the desktop
$desktopPath = [Environment]::GetFolderPath("Desktop")

# Shortcut name
$shortcutName = "Web_Gen_box_to_s3.lnk"

# Full path to the shortcut
$shortcutPath = Join-Path -Path $desktopPath -ChildPath $shortcutName

# Create a WScript.Shell COM object
$wsh = New-Object -ComObject WScript.Shell

# Create the shortcut
$shortcut = $wsh.CreateShortcut($shortcutPath)

# Set the target path, working directory, and icon location
$shortcut.TargetPath = $pythonPath
$shortcut.Arguments = $scriptPath
$shortcut.WorkingDirectory = [System.IO.Path]::GetDirectoryName($scriptPath)
$shortcut.IconLocation = $pythonPath
$shortcut.Save()

Write-Output "Shortcut created on desktop: $shortcutPath"
