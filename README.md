# BlobSculptor

### _A desktop app for building ZombieNW Blob avatars._

![Languages](https://badgen.net/badge/language/Python/yellow) ![Platform](https://badgen.net/badge/platform/Windows/blue) ![License](https://badgen.net/badge/license/MIT/red)

# Usage

- Have Blender 5.0 or greater installed.
- Download BlobSculptor from releases.
- Open, select hair, select color, click "Sculpt"
- `.blend` file will be output to same directory as executable.

# Stack

I am using a stack I've not seen used before for this program. The frontend is built with `SvelteKit` and the backend is in `Python`. The `SvelteKit` interface runs inside a `PyWebView` window and is built into an executable using `PyInstall`.
