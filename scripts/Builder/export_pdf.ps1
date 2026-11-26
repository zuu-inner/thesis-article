<#
.SYNOPSIS
    Export the AVITEC manuscript DOCX to PDF with Microsoft Word (COM).

.DESCRIPTION
    The AVITEC build chain is: build_docx.py -> this script -> finalize_pdf.py.
    Word is used because it is the reference renderer for the official
    template (article/article.docx); the exported PDF is afterwards finalized
    by finalize_pdf.py (metadata + restoring the source figure resolution,
    which Word lowers to ~200 ppi during export).

.EXAMPLE
    pwsh -File article/scripts/Builder/export_pdf.ps1
#>
param(
    [string]$Docx = "",
    [string]$Pdf = ""
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
if (-not $Docx) { $Docx = Join-Path $root "article\drafts\article-draft.docx" }
if (-not $Pdf)  { $Pdf  = Join-Path $root "article\drafts\article-draft.pdf" }

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($Docx, $false, $true)
    # wdExportFormatPDF = 17, wdExportOptimizeForPrint = 0, wdExportAllDocument = 0,
    # wdExportDocumentContent = 0, wdExportCreateHeadingBookmarks = 1
    $doc.ExportAsFixedFormat($Pdf, 17, $false, 0, 0, 1, 1, 0, $true, $true, 1, $true, $true, $false)
    $doc.Close(0)
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
Write-Output "exported $Pdf"
