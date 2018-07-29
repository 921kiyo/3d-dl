(TeX-add-style-hook
 "second_report"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "a4paper" "11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("geometry" "margin=2cm") ("footmisc" "bottom") ("datetime" "nodayofweek")))
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art11"
    "geometry"
    "footmisc"
    "graphicx"
    "subcaption"
    "datetime"
    "fancyhdr")
   (LaTeX-add-labels
    "fig:sample_image"
    "fig:trainig_pipeline"
    "fig:rendering_process"
    "fig:test_eval_schematic")
   (LaTeX-add-bibliographies
    "biblio"))
 :latex)

