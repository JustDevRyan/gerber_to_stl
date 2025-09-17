import os
from random import randint
import subprocess
import tempfile
import logging

from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import render

import gerber
from gerber_to_scad import process_gerber
from gts_service.forms import UploadForm

def main(request):
    form = UploadForm(request.POST or None, files=request.FILES or None)
    version = "0.1.4"
    if form.is_valid():
        outline_file = form.cleaned_data["outline_file"]
        solderpaste_file = request.FILES["solderpaste_file"]
        outline = None

        if outline_file:
            try:
                outline = gerber.loads(outline_file.read().decode("utf-8"))
            except Exception as e:
                logging.error(e)
                outline = None
                form.errors["outline_file"] = [
                    "Invalid format, is this a valid gerber file?"
                ]

        try:
            solder_paste = gerber.loads(solderpaste_file.read().decode("utf-8"))
        except Exception as e:
            logging.error(e)
            solder_paste = None
            form.errors["solderpaste_file"] = [
                "Invalid format, is this a valid gerber file?"
            ]

        if not form.errors:
            output = process_gerber(
                outline_file=outline,
                solderpaste_file=solder_paste,
                stencil_thickness=form.cleaned_data["stencil_thickness"],
                include_ledge=form.cleaned_data["include_ledge"],
                ledge_thickness=form.cleaned_data["ledge_thickness"],
                gap=form.cleaned_data["gap"],
                include_frame=form.cleaned_data["include_frame"],
                frame_width=form.cleaned_data["frame_width"],
                frame_height=form.cleaned_data["frame_height"],
                frame_thickness=form.cleaned_data["frame_thickness"],
                increase_hole_size_by=form.cleaned_data["increase_hole_size_by"],
                simplify_regions=form.cleaned_data["simplify_regions"],
                flip_stencil=form.cleaned_data["flip_stencil"],
                stencil_width=form.cleaned_data["stencil_width"],
                stencil_height=form.cleaned_data["stencil_height"],
                stencil_margin=form.cleaned_data["stencil_margin"],
            )

            # Name generator " stencil_<random-number> " 
            file_id = randint(1000000000, 9999999999)
            temp_dir = tempfile.gettempdir()  # Windows temp directory
            scad_filename = os.path.join(temp_dir, f"stencil-{file_id}.scad")
            stl_filename = os.path.join(temp_dir, f"stencil-{file_id}.stl")

            with open(scad_filename, "w") as scad_file:
                scad_file.write(output)

            # Ensure OPENSCAD_EXECUTABLE points to OpenSCAD executable
            if not os.path.isfile(settings.OPENSCAD_EXECUTABLE):
                form.errors["__all__"] = ["OpenSCAD executable not found"]
                return render(request, "main.html", {"form": form, "version": version})

            # Run OpenSCAD on Windows
            p = subprocess.Popen(
            [settings.OPENSCAD_EXECUTABLE, "-o", stl_filename, scad_filename],
            shell=True
        )

            p.wait()

            if p.returncode:
                form.errors["__all__"] = ["Failed to create an STL file from inputs"]
            else:
                with open(stl_filename, "r") as stl_file:
                    stl_data = stl_file.read()
                os.remove(stl_filename)

            # Clean up SCAD file
            os.remove(scad_filename)

        if form.errors:
            return render(request, "main.html", {"form": form, "version": version})

        response = HttpResponse(stl_data, content_type="application/zip")
        response["Content-Disposition"] = (
            f"attachment; filename={os.path.basename(stl_filename)}"
        )
        return response

    return render(request, "main.html", {"form": form, "version": version})
