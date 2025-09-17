# Gerber to STL
## Makes a 3D printable solder stencil by just uploading two gerber files!

~~This repository has both a CLI tool, and a web app available at https://solder-stencil.me.~~ Unfortunately the website is no longer available so that is why i made this project a standalone windows application that starts a webserver.

## Installation

### Option 1: Setup and run the application with Python
`gerber_to_stl` **requires Python 3.9**

* Unzip openscad.zip

* Install the requirements.txt
```bash
pip install -r requirements.txt
```
* Open main.py and thats it!

### Option 2: Install the latest [Release](https://github.com/JustDevRyan/gerber_to_stl/releases) (Recommended) (Windows Installer coming soon...)

* Go to the [Releases](https://github.com/JustDevRyan/gerber_to_stl/releases) page

* Download the latest release ZIP

* Extract the ZIP into a folder of your choice

* Make a shortcut to main.exe named **Gerber to STL** to the desktop

* Open the shortcut (no Python installation required)

* Enjoy using `gerber_to_stl` without manual setup!

**Note:** Some antivirus programs may flag the app as a virus.  
This is a common false-positive for Python apps. The source code is open, continue to Option 3 if you are sceptical.

### Option 3: Build the app by yourself

If you prefer building the application from the source code:

* Make sure you have **Python 3.10** installed.

* Clone this repository:
```bash
git clone https://github.com/JustDevRyan/gerber_to_stl.git
cd gerber_to_stl
```

* Install the required dependencies:
```bash
pip install -r requirements.txt
```

* To build the repository into a standalone directory, run:
```bash
python setup.py build
```

* Your builded app should be located in the **build** folder

* Send a shortcut to the desktop and name it (Optional).


## Usage

Run `main.exe` or `main.py`. You can either start the webserver directly or customize the port before starting it.  

Once the server is running, open your browser and go to:

```bash
http://127.0.0.1:8000
```

Replace `8000` with your chosen port if you customized it. The web interface should now be accessible and ready to use.

If you liked this project and my work, I would really appreciate a ⭐ on the repository!


## Changes
* Added support to windows
* Made a GUI in PyQt5
* Removed the need of poetry
* Removed unnecessary files
* Cleaned and optimized parts of the code
* Optimized the HTML page
* Added a loading spinner next to the "Convert to STL" button that lasts 15 seconds to prevent clicking it again while its already loading
* Made OpenSCAD work directly from the base directory making the whole app standalone
* Designed an icon


## Contributing

*Contributions are very welcome, I don't have a lot of time to spend on this project, but I try to review PRs as much as I can!* 

**- I had and I did spend some time to make this. Thank you [Rob](https://github.com/kirberich) for making this possible**

* *Please use ruff to format your code - if you use VS code, you can open the `gerber_to_scad.code-workspace` file to get all the right automatic formatting in your editor, or you can just run `ruff format .` in the project root.* **NOTE: I didn't format my code, it works perfectly fine even when compiled. But if you want to, do it!**
