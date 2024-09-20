# add.ps1

# Define the path for the new directory and file
$newDirectoryPath = 'D:\dev\d_drive\proj_main\outfiles'
$newFilePath = Join-Path -Path $newDirectoryPath -ChildPath 'sample.txt'

# Create the new directory if it doesn't exist
if (-Not (Test-Path -Path $newDirectoryPath)) {
    New-Item -Path $newDirectoryPath -ItemType Directory
}

# Add a new file with some content
$content = "This is a sample file created by add.ps1."
Set-Content -Path $newFilePath -Value $content

Write-Output "Directory and file created successfully."
