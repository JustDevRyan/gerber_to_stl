# views.py

import os
import subprocess
import tempfile
import logging
import datetime

from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import render

import gerber
from convertion import process_gerber
from gts_service.forms import UploadForm

logger = logging.getLogger(__name__)

def main(request):
    version = "0.1.4"
    form = UploadForm(request.POST or None, files=request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        try:
            # --- 1. Process Files ---
            outline_file = form.cleaned_data["outline_file"]
            solderpaste_file = request.FILES["solderpaste_file"]
            outline = None
            solder_paste = None

            # Parse Outline
            if outline_file:
                try:
                    outline = gerber.loads(outline_file.read().decode("utf-8"))
                except Exception as e:
                    logger.error(f"Error parsing outline: {e}")
                    form.add_error("outline_file", "Invalid format. Is this a valid gerber file?")

            # Parse Solder Paste
            try:
                solder_paste = gerber.loads(solderpaste_file.read().decode("utf-8"))
            except Exception as e:
                logger.error(f"Error parsing solder paste: {e}")
                form.add_error("solderpaste_file", "Invalid format. Is this a valid gerber file?")

            if form.errors:
                return render(request, "main.html", {"form": form, "version": version})

            # --- 2. Generate SCAD Content ---
            use_manual = form.cleaned_data.get("manual_stencil")
            scad_content = process_gerber(
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
                full_ledge=form.cleaned_data["full_ledge"],
            )

            # --- 3. Run OpenSCAD ---
            file_id = datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
            temp_dir = tempfile.gettempdir()
            scad_filename = os.path.join(temp_dir, f"stencil-{file_id}.scad")
            stl_filename = os.path.join(temp_dir, f"stencil-{file_id}.stl")

            try:
                # Write SCAD file
                with open(scad_filename, "w") as scad_file:
                    scad_file.write(scad_content)

                if not os.path.isfile(settings.OPENSCAD_EXECUTABLE):
                    form.add_error(None, "OpenSCAD executable not found on server.")
                    return render(request, "main.html", {"form": form, "version": version})

                # Execute OpenSCAD
                # NOTE: Removed shell=True for security. Passing args as list.
                cmd = [settings.OPENSCAD_EXECUTABLE, "-o", stl_filename, scad_filename]
                
                # Check for Windows specifically if needed for path resolution, 
                # but subprocess.run with list handles spaces in paths better.
                process = subprocess.run(cmd, capture_output=True, text=True)

                if process.returncode != 0:
                    logger.error(f"OpenSCAD failed: {process.stderr}")
                    form.add_error(None, "Failed to generate STL file. Check logs.")
                    return render(request, "main.html", {"form": form, "version": version})

                # Read the generated STL (BINARY MODE)
                if os.path.exists(stl_filename):
                    with open(stl_filename, "rb") as stl_file:
                        stl_data = stl_file.read()
                else:
                    form.add_error(None, "Output file was not created by OpenSCAD.")
                    return render(request, "main.html", {"form": form, "version": version})

                # --- 4. Return Response ---
                response = HttpResponse(stl_data, content_type="model/stl")
                response["Content-Disposition"] = f"attachment; filename=stencil-{file_id}.stl"
                return response

            finally:
                # Cleanup Temp Files
                if os.path.exists(scad_filename):
                    os.remove(scad_filename)
                if os.path.exists(stl_filename):
                    os.remove(stl_filename)

        except Exception as e:
            logger.exception("Unexpected error in main view")
            form.add_error(None, f"An unexpected error occurred: {str(e)}")

    return render(request, "main.html", {"form": form, "version": version})