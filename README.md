# Gerber to STL

## A great tool for making your pcb solder stencil a 3D Printable STL by just uploading two gerber files

~~This repository has both a CLI tool, and a web app available at https://solder-stencil.me.~~ Unfortunately the website is no longer available so that is why i made this project a standalone windows application.

## Installation

### Option 1: The Easy Way (Recommended)
Download and run the **Windows Installer**. This is the fastest method; it automatically handles shortcut creation and configures the necessary permissions to avoid "Access Denied" errors.

* **Download**: Get `GerberToSTL_Setup_v2.5.2.exe` from the [Releases](https://github.com/JustDevRyan/gerber_to_stl/releases) page.
* **Run**: Open the installer. It will request Administrator privileges to ensure the app can write STL files to your disk without `Errno 13` issues.
* **Customize**: Use the checkboxes to automatically add **Gerber to STL** to your **Desktop** and **Start Menu**.
* **Launch**: You can start the app immediately from the final installer screen.

### Option 2: Portable Version (No Installation)
If you prefer not to use an installer, you can run the app from a standalone folder.

* **Download**: Download the latest release **ZIP** from the [Releases](https://github.com/JustDevRyan/gerber_to_stl/releases) page.
* **Extract**: Unzip the contents into a folder of your choice.
* **Shortcut**: Right-click `Gerber To STL.exe` and select "Send to > Desktop (create shortcut)".
* **Note**: You may need to right-click the EXE and "Run as Administrator" if you encounter permission errors during the STL generation process.

> **Note on Antivirus:** Some programs (like Windows Defender) may flag the installer or the standalone EXE as a threat. This is a common **false-positive** for compressed Python applications. Since this project is open-source, you can verify the code yourself or choose Option 3 to build it from scratch.

### Option 3: Build the app by yourself
If you want to compile the binary or the installer yourself:

1. **Prerequisites**: Ensure you have **Python 3.9 or 3.10** installed.
2. **Clone & Setup**:
   ```bash
   git clone [https://github.com/JustDevRyan/gerber_to_stl.git](https://github.com/JustDevRyan/gerber_to_stl.git)
   cd gerber_to_stl
   pip install -r requirements.txt
   python setup.py build
Find the exe in the build folder and run it

### Option 4: Setup and run the application with Python
`gerber_to_stl` **requires Python 3.9 or 3.10**

* Unzip openscad.zip

* Install the requirements
```bash
pip install -r requirements.txt
```
* Open **Gerber to STL.py**

## Changes
* Added support to windows
* Made an installer
* Made a GUI in PyQt5
* Cleaned and optimized parts of the code
* Brand new styled and animated web page
* Made OpenSCAD work directly from the base directory making the whole app standalone
* Removed the need of poetry
* Removed unnecessary files
* Designed an icon

If you liked this project and my work, I would really appreciate a ⭐ on the repository!

## Contributing

*Contributions are very welcome, I don't have a lot of time to spend on this project, but I try to review PRs as much as I can!* 
**- I had and I did spend some time to make this. Thank you [Rob](https://github.com/kirberich)!**

* *Please use ruff to format your code - if you use VS code, you can open the `gerber_to_scad.code-workspace` file to get all the right automatic formatting in your editor, or you can just run `ruff format .` in the project root.* **NOTE: I didn't format my code, it works perfectly fine even when compiled. But if you want to, do it!**
