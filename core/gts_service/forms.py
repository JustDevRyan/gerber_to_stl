from django import forms

class UploadForm(forms.Form):
    # --- File Uploads ---
    solderpaste_file = forms.FileField(
        label="Solder Paste (.gtp)",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.gtp,.gbr'})
    )
    outline_file = forms.FileField(
        label="Outline (.gm1, optional)",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.gm1,.gbr'})
    )

    # --- Manual Stencil Settings ---
    manual_stencil = forms.BooleanField(
        label="Define stencil size manually",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'collapse-checkbox manual-stencil-size',
            'id': 'manual-stencil'
        })
    )
    stencil_width = forms.FloatField(
        label="Stencil Width (mm)",
        required=False,
        initial=0.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    stencil_height = forms.FloatField(
        label="Stencil Height (mm)",
        required=False,
        initial=0.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    stencil_margin = forms.FloatField(
        label="Stencil Margin (mm)",
        required=False,
        initial=0.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )

    # --- Processing Options ---
    simplify_regions = forms.BooleanField(
        label="Simplify regions (may speed up processing)",
        required=False,
        initial=False
    )
    flip_stencil = forms.BooleanField(
        label="Flip stencil (for bottom layer)",
        required=False,
        initial=False
    )
    stencil_thickness = forms.FloatField(
        label="Stencil thickness (mm)",
        initial=0.2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    increase_hole_size_by = forms.FloatField(
        label="Increase hole size by (mm)",
        initial=0.000,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'value': '0.000'})
    )
    gap = forms.FloatField(
        label="Gap around board (mm)",
        initial=0.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )

    # --- Ledge Settings ---
    include_ledge = forms.BooleanField(
        label="Include ledge",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'collapse-checkbox include-ledge',
            'id': 'include_ledge'
        })
    )
    ledge_thickness = forms.FloatField(
        label="Ledge thickness (mm)",
        initial=1.2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    full_ledge = forms.BooleanField(
        label="Full ledge (all the way around)",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            #'class': 'form-control',
            'id': 'full_ledge'
        })
    )
    # --- Frame Settings ---
    include_frame = forms.BooleanField(
        label="Include frame",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'collapse-checkbox include-frame',
            'id': 'include_frame'
        })
    )
    frame_width = forms.FloatField(
        label="Frame width (mm)",
        initial=155,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    frame_height = forms.FloatField(
        label="Frame height (mm)",
        initial=155,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    frame_thickness = forms.FloatField(
        label="Frame thickness (mm)",
        initial=1.2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )