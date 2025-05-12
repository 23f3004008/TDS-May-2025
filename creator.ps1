# PowerShell script to create Question folders and .md files
# Usage: .\creator.ps1 <number_of_questions>

param(
    [Parameter(Mandatory=$true)]
    [int]$numberOfQuestions
)

# Get current directory
$currentDir = Get-Location

# Create Question folders and .md files
for ($i = 1; $i -le $numberOfQuestions; $i++) {
    # Create Question folder
    $questionDir = Join-Path $currentDir "Question-$i"
    if (-not (Test-Path $questionDir)) {
        New-Item -Path $questionDir -ItemType Directory
        Write-Host "Created directory: $questionDir"
    } else {
        Write-Host "Directory already exists: $questionDir"
    }

    # Create .md file
    $mdFile = Join-Path $questionDir "$i.md"
    if (-not (Test-Path $mdFile)) {
        New-Item -Path $mdFile -ItemType File
        Write-Host "Created file: $mdFile"
    } else {
        Write-Host "File already exists: $mdFile"
    }
}

Write-Host "`nCreation complete! Created $numberOfQuestions question folders and files in: $currentDir"
