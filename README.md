# IENDLoader (.NET WPF)

Minimal .NET WPF port of IENDLoader. This branch only contains the .NET app.

## Build
- Open `IENDLoader.sln` in Visual Studio (Windows)
- Target framework: .NET 8 (Windows)
- Build: Debug or Release

## Run
- Debug: F5 in Visual Studio
- CLI: `dotnet build` then run the generated `IENDLoader.exe`

## Notes
- ARM64 Windows is supported. For self-contained Release publish, set `RuntimeIdentifier` appropriately.
