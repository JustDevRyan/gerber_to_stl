# Gerber to STL

## A great tool for making your pcb solder stencil a 3D Printable STL by just uploading two gerber files

~~This repository has both a CLI tool, and a web app available at https://solder-stencil.me.~~ Unfortunately the website is no longer available so that is why i made this project a standalone windows application.

## Installation

### Option 1: Install the latest [Release](https://github.com/JustDevRyan/gerber_to_stl/releases) (Recommended) (Windows Installer coming soon...)

* Go to the [Releases](https://github.com/JustDevRyan/gerber_to_stl/releases) page

* Download the latest release ZIP

* Extract the ZIP into a folder of your choice

* Create a shortcut to **Gerber to STL.exe** to the desktop

* Open the shortcut (no Python installation required)

* Enjoy using **Gerber to STL** without manual setup!

**Note:** Some antivirus programs may flag the app as a virus.  
This is a common false-positive for Python apps. The source code is open, continue to Option 2 if you are sceptical.

### Option 2: Build the app by yourself

If you prefer building the application from the source code:

* Make sure you have **Python 3.9 or 3.10** installed.

* Clone this repository:
```bash
git clone https://github.com/JustDevRyan/gerber_to_stl.git
cd gerber_to_stl
```

* Install the requirements:
```bash
pip install -r requirements.txt
```

* To build the repository into a directory, run:
```bash
python setup.py build
```

* Your builded app should be located in the **build** folder

* Send a shortcut to the desktop and name it (Optional).

* Enjoy!

### Option 3: Setup and run the application with Python (Not recommended)
`gerber_to_stl` **requires Python 3.9 or 3.10**

* Unzip openscad.zip

* Install the requirements
```bash
pip install -r requirements.txt
```
* Open **Gerber to STL.py** and thats it!

## Usage

* Run `Gerber to STL.exe` or `Gerber to STL.py`. You can either start it directly or customize the port before starting it.  

* Once the server is running, you can either open it in your default browser or you can launch a webview that is like a window rather than a browser.

If you liked this project and my work, I would really appreciate a ⭐ on the repository!


## Changes
* Added support to windows
* Made a GUI in PyQt5
* Cleaned and optimized parts of the code
* Brand new styled and animated web page
* Made OpenSCAD work directly from the base directory making the whole app standalone
* Removed the need of poetry
* Removed unnecessary files
* Designed an icon

## Contributing

*Contributions are very welcome, I don't have a lot of time to spend on this project, but I try to review PRs as much as I can!* 
**- I had and I did spend some time to make this. Thank you [Rob](https://github.com/kirberich)!**

* *Please use ruff to format your code - if you use VS code, you can open the `gerber_to_scad.code-workspace` file to get all the right automatic formatting in your editor, or you can just run `ruff format .` in the project root.* **NOTE: I didn't format my code, it works perfectly fine even when compiled. But if you want to, do it!**
