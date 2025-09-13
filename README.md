# gerber_to_stl
Simple python script for converting gerber files into a 3d printable solder stencil scad/stl file

~~This repository has both a CLI tool, and a web app available at https://solder-stencil.me.~~ Unfortunately the website no longer works so that is why i made this project a standalone windows application that starts a webserver which is 
## Installation

`gerber_to_stl` requires python 3.10

~~* Make sure you have [poetry](https://python-poetry.org/docs/) installed.~~ You no longer need poetry! Yay! (If you want to use a virtual environment just use a normal one)

Just install the requirements from the .txt file and you are good to go!
```bash
pip install -r requirements.txt
```

## Usage

Start main.exe and from there you can either directly start the webserver or if you want you can customize the port and then start it. From there open up your browser and enter localhost and your port. By default it should be:
```bash
127.0.0.1:8000
```
## Contributing

*Contributions are very welcome, I don't have a lot of time to spend on this project, but I try to review PRs as much as I can!* 

**- I had and I did spend some time to make this. Thank you [Rob](https://github.com/kirberich) for making this possible**

* *Please use ruff to format your code - if you use VS code, you can open the `gerber_to_scad.code-workspace` file to get all the right automatic formatting in your editor, or you can just run `ruff format .` in the project root.* **NOTE: I didn't format my code, it works perfectly fine even when compiled. But if you want to, do it!**
