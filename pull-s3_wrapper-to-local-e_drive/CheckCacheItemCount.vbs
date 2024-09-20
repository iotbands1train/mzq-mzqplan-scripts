' Define the path to the cache directory
Dim cachePath
cachePath = "C:\Users\Administrator\AppData\Local\Box\Box\cache"

' Define the maximum number of items allowed
Dim maxItems
maxItems = 20

' Count the number of items in the cache directory
Dim fso, folder, files
Set fso = CreateObject("Scripting.FileSystemObject")
Set folder = fso.GetFolder(cachePath)
Set files = folder.Files

Dim itemCount
itemCount = files.Count

' Count the number of items in subfolders
Dim subfolders, subfolder
Set subfolders = folder.SubFolders

For Each subfolder In subfolders
    itemCount = itemCount + subfolder.Files.Count
Next

' Check if the item count exceeds the maximum allowed
If itemCount > maxItems Then
    ' Log an event to the Windows Event Log
    Dim shell, eventMessage
    eventMessage = "Cache directory contains more than " & maxItems & " items. Current count: " & itemCount
    Set shell = CreateObject("WScript.Shell")
    shell.LogEvent 4, eventMessage ' 4 = Information event
End If
