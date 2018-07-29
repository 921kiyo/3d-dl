(TeX-add-style-hook
 "report_template"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "a4paper" "11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("datetime" "nodayofweek")))
   (TeX-run-style-hooks
    "latex2e"
    "preliminary-pipeline"
    "article"
    "art11"
    "datetime"
    "fancyhdr")
   (LaTeX-add-bibliographies
    "references"))
 :latex)

