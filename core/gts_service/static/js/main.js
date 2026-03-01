$(document).ready(function () {

  // ---------- Download Toast ----------
  window.showDownloadToast = function (filename) {
    const toast = document.getElementById("download-toast");
    const filenameEl = document.getElementById("toast-filename");
    filenameEl.textContent = filename || "stencil.stl";

    // Remove old progress bar, add fresh one
    const oldBar = toast.querySelector(".toast-progress");
    if (oldBar) oldBar.remove();
    const bar = document.createElement("div");
    bar.className = "toast-progress";
    toast.appendChild(bar);

    // Show: set display first, then trigger transition on next frame
    toast.style.display = "flex";
    toast.style.opacity = "0";
    toast.style.transform = "translateY(16px)";
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        toast.style.transition = "opacity 0.28s ease, transform 0.28s ease";
        toast.style.opacity = "1";
        toast.style.transform = "translateY(0)";
      });
    });

    // Auto-hide after 3.5s
    clearTimeout(toast._hideTimer);
    toast._hideTimer = setTimeout(function () {
      toast.style.opacity = "0";
      toast.style.transform = "translateY(16px)";
      setTimeout(function () {
        toast.style.display = "none";
        toast.style.transition = "";
      }, 300);
    }, 3500);
  };

  // ---------- Form Submit via fetch ----------
  $("#gerber-form").on("submit", function (e) {
    e.preventDefault();

    const form = $(this)[0];
    const formData = new FormData(form);

    $("#spinner").addClass("active");
    $("#convert-btn").prop("disabled", true).text("Converting...");

    fetch(form.action || window.location.href, {
      method: "POST",
      body: formData,
    })
      .then(function (response) {
        if (!response.ok) {
          return response.text().then(function (text) {
            throw new Error("Server error " + response.status + ": " + text.substring(0, 200));
          });
        }

        // Get filename from Content-Disposition header
        const disposition = response.headers.get("Content-Disposition") || "";
        let filename = "stencil.stl";
        const match = disposition.match(/filename[^;=\n]*=['"]?([^'"\n;]+)['"]?/);
        if (match) filename = match[1].trim();

        return response.arrayBuffer().then(function (buffer) {
          return { buffer, filename };
        });
      })
      .then(function ({ buffer, filename }) {
        const isStandalone = window.__STANDALONE__ === true;

        if (isStandalone && window.pywebview && window.pywebview.api) {
          // --- Standalone: save via Python API ---
          const bytes = new Uint8Array(buffer);
          let hex = "";
          for (let i = 0; i < bytes.length; i++) {
            hex += bytes[i].toString(16).padStart(2, "0");
          }

          window.pywebview.api.save_file(filename, hex).then(function (result) {
            if (result.ok) {
              window.showDownloadToast(filename);
            } else {
              alert("Failed to save file: " + result.error);
            }
          });

        } else {
          // --- Browser: trigger blob download ---
          const blob = new Blob([buffer]);
          const url = URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = filename;
          document.body.appendChild(a);
          a.click();
          setTimeout(function () {
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
          }, 150);

          window.showDownloadToast(filename);
        }
      })
      .catch(function (err) {
        alert("Conversion failed: " + err.message);
        console.error(err);
      })
      .finally(function () {
        $("#spinner").removeClass("active");
        $("#convert-btn").prop("disabled", false).text("Convert to STL");
      });
  });

  // ---------- Collapsible Sections ----------
  function initCollapse(selector) {
    $(selector).each(function () {
      const content = $(this).closest(".collapse-container").find(".collapse-content").first();
      content.toggleClass("expanded", $(this).prop("checked"));
    });
    $(selector).on("change", function () {
      const content = $(this).closest(".collapse-container").find(".collapse-content").first();
      content.toggleClass("expanded", $(this).prop("checked"));
    });
  }

  initCollapse(".collapse-checkbox");
  initCollapse(".include-ledge");
  initCollapse(".manual-stencil-size");

  // ---------- Manual Size Toggle ----------
  $(".manual-stencil").each(function () {
    const checked = $(this).prop("checked");
    $("#id_outline_file").prop("disabled", checked);
    $("#stencil_width, #stencil_height, #stencil_margin").prop("disabled", !checked);
  });

  $(".manual-stencil").change(function () {
    const checked = $(this).prop("checked");
    $("#id_outline_file").prop("disabled", checked);
    $("#stencil_width, #stencil_height, #stencil_margin").prop("disabled", !checked);
  });

  // ---------- Frame / Ledge Toggle ----------
  const frameOptions = $("#frame-options");

  $(".include-frame").each(function () {
    if ($(this).prop("checked")) frameOptions.addClass("expanded");
  });

  $(".include-frame").change(function () {
    if ($(this).prop("checked")) {
      $(".include-ledge").prop("checked", false).trigger("change");
      frameOptions.addClass("expanded");
    } else {
      frameOptions.removeClass("expanded");
    }
  });

  $(".include-ledge").each(function () {
    if ($(this).prop("checked")) frameOptions.removeClass("expanded");
  });

  $(".include-ledge").change(function () {
    if ($(this).prop("checked")) {
      $(".include-frame").prop("checked", false).trigger("change");
      frameOptions.removeClass("expanded");
    }
  });

  // ---------- Credits Toggle ----------
  $("#credits-content").hide(); 
  $("#credits-toggle").on("click", function () {
    const btn = $(this);
    $("#credits-content").slideToggle(300, function() {
      if ($(this).is(":visible")) {
        btn.text("Show Less Credits");
      } else {
        btn.text("Show More Credits");
      }
    });
  });

});