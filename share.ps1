Clear-Host

# Get-ChildItem "src\datafun_streaming\data_validation" -Recurse -File | ForEach-Object { Write-Host "`n=== $($_.FullName) ===`n"; Get-Content $_.FullName }

# Get-ChildItem "src\datafun_streaming\io" -Recurse -File | ForEach-Object { Write-Host "`n=== $($_.FullName) ===`n"; Get-Content $_.FullName }

# Get-ChildItem "src\datafun_streaming\kafka" -Recurse -File | ForEach-Object { Write-Host "`n=== $($_.FullName) ===`n"; Get-Content $_.FullName }

# Get-ChildItem "src\datafun_streaming\stats" -Recurse -File | ForEach-Object { Write-Host "`n=== $($_.FullName) ===`n"; Get-Content $_.FullName }

# Get-ChildItem "src\datafun_streaming\storage" -Recurse -File | ForEach-Object { Write-Host "`n=== $($_.FullName) ===`n"; Get-Content $_.FullName }

# Get-ChildItem "src\datafun_streaming\visualization" -Recurse -File | ForEach-Object { Write-Host "`n=== $($_.FullName) ===`n"; Get-Content $_.FullName }

# Get-ChildItem "tests" -Recurse -File | ForEach-Object { Write-Host "`n=== $($_.FullName) ===`n"; Get-Content $_.FullName }

Get-ChildItem "docs" -Recurse -File | ForEach-Object { Write-Host "`n=== $($_.FullName) ===`n"; Get-Content $_.FullName }
