# Synthetic R example adapted from the embedded nature-figure R workflow.
# Run: Rscript --vanilla render_example.R <new-output-directory>
# Uses its own file location, not the caller's working directory.
args_all <- commandArgs(trailingOnly = FALSE)
script_arg <- grep("^--file=", args_all, value = TRUE)
if (length(script_arg) != 1) stop("Run this example with Rscript --vanilla")
script_file <- normalizePath(sub("^--file=", "", script_arg), mustWork = TRUE)
example_dir <- dirname(script_file)
skill_dir <- normalizePath(file.path(example_dir, "..", ".."), mustWork = TRUE)
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) stop("Provide one new output directory")
output <- args[[1]]
if (file.exists(output)) stop("Choose a new output directory")
packages <- c("ggplot2", "patchwork", "jsonlite", "svglite", "ragg")
missing <- packages[!vapply(packages, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing)) stop(paste("Missing R packages:", paste(missing, collapse = ", ")))
python <- Sys.getenv("NATURE_QA_PYTHON", unset = Sys.which("python"))
if (!nzchar(python)) stop("Python is required for the non-rendering alignment JSON audit")
library(ggplot2)
library(patchwork)
source(file.path(skill_dir, "embedded", "nature-figure", "scripts", "panel_alignment.R"))
data <- read.csv(file.path(example_dir, "synthetic.csv"), check.names = FALSE)
if (any(!is.finite(data$Time)) || any(!is.finite(data$Value))) stop("Expected finite synthetic inputs")
theme_set(theme_classic(base_size = 8, base_family = "sans") +
            theme(legend.position = "bottom", plot.tag = element_text(face = "bold")))
colors <- c(A = "#0072B2", B = "#D55E00")
p1 <- ggplot(data, aes(Time, Value, color = Group, shape = Group)) +
  geom_line(linewidth = 0.5) + geom_point(size = 1.5) +
  scale_color_manual(values = colors) + labs(y = "Synthetic value", x = "Time (arbitrary units)")
p2 <- ggplot(data, aes(Time, Value, color = Group, shape = Group)) +
  geom_point(size = 2) + scale_color_manual(values = colors) +
  labs(y = "Synthetic value", x = "Time (arbitrary units)")
figure <- (p1 | p2) + plot_layout(guides = "collect") +
  plot_annotation(tag_levels = "a", caption = "Synthetic example; no experimental data")
dir.create(output, recursive = TRUE, showWarnings = FALSE)
stem <- file.path(output, "nature-r-example")
require_patchwork_panel_alignment(
  figure, manifest_path = paste0(stem, ".layout.json"), report_path = paste0(stem, ".alignment.json"),
  width_in = 7.2, height_in = 3.6, panel_ids = c("a", "b"),
  audit_script = file.path(skill_dir, "embedded", "nature-figure", "scripts", "audit_panel_alignment.py"),
  python = python, strict = TRUE)
ggsave(paste0(stem, ".svg"), figure, width = 7.2, height = 3.6, device = svglite::svglite)
ggsave(paste0(stem, ".pdf"), figure, width = 7.2, height = 3.6, device = grDevices::cairo_pdf)
ggsave(paste0(stem, ".tiff"), figure, width = 7.2, height = 3.6, dpi = 600, device = ragg::agg_tiff)
ggsave(paste0(stem, ".png"), figure, width = 7.2, height = 3.6, dpi = 300, device = ragg::agg_png)
writeLines(capture.output(sessionInfo()), file.path(output, "session-info.txt"))
message("R example exported. Actual page review and rendered-PDF audits remain required.")
