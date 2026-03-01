$(document).ready(function () {

  // ---------- Download Toast ----------
  window.showDownloadToast = function (filename) {
    const toast = document.getElementById("download-toast");
    const filenameEl = document.getElementById("toast-filename");
    filenameEl.textContent = filename || "stencil.stl";

    const oldBar = toast.querySelector(".toast-progress");
    if (oldBar) oldBar.remove();
    const bar = document.createElement("div");
    bar.className = "toast-progress";
    toast.appendChild(bar);

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

  // ---------- CSRF helper ----------
  function getCsrfToken() {
    const v = document.cookie.match("(^|;) ?csrftoken=([^;]*)(;|$)");
    return v ? v[2] : "";
  }

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
      redirect: "error",
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    })
      .then(function (response) {
        // Clone response so we can read it twice if needed
        const contentType = response.headers.get("Content-Type") || "";

        if (!response.ok) {
          // Could be our JsonResponse error
          if (contentType.includes("application/json")) {
            return response.json().then(function (data) {
              throw new Error(data.error || "Unknown server error");
            });
          }
          return response.text().then(function (text) {
            throw new Error("Server error " + response.status + ": " + text.substring(0, 300));
          });
        }

        // Django returned HTML = unhandled form error or 500
        if (contentType.includes("text/html")) {
          return response.text().then(function (html) {
            const errMatch = html.match(/<ul class="errorlist">([\s\S]*?)<\/ul>/);
            if (errMatch) {
              throw new Error("Form error: " + errMatch[1].replace(/<[^>]+>/g, " ").trim());
            }
            const excMatch = html.match(/<pre class="exception_value">([\s\S]*?)<\/pre>/);
            if (excMatch) {
              throw new Error("Server exception: " + excMatch[1].replace(/<[^>]+>/g, "").trim());
            }
            const snippet = html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim().substring(0, 400);
            throw new Error("Server returned HTML.\n\nCheck gts_error.log in the app folder.\n\n" + snippet);
          });
        }

        // Handle our JsonResponse errors that somehow come back as 200
        if (contentType.includes("application/json")) {
          return response.json().then(function (data) {
            if (data.error) throw new Error(data.error);
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
        alert("Conversion failed:\n\n" + err.message);
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
    const content = $("#credits-content");
    const btn = $(this);
    content.slideToggle(300, function () {
      // Runs after animation completes — check final visibility state
      btn.text(content.is(":visible") ? "Show Less Credits" : "Show More Credits");
    });
  });

});