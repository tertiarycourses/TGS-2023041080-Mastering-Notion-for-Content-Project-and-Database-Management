#!/usr/bin/env bash
# Single-command aligned build from the single source (course_data.py + data_domain*.py + data_teaching.py):
#   labs/ (folders + mock data + workflow PNG + instruction PDF) → PPT (+ slide_map.json) → LP → LG (+ MD mirror)
#   → PDFs (LibreOffice) → page-numbered TOC injection (LP + LG) → re-render.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; REPO="$(dirname "$HERE")"; CW="$REPO/courseware"
SOFFICE="${SOFFICE:-soffice}"
SHORT="$(python3 -c "import sys; sys.path.insert(0,'$HERE'); import course_data as C; print(C.SHORT_TITLE)")"
VER="$(python3 -c "import sys; sys.path.insert(0,'$HERE'); import course_data as C; print(C.VERSION)")"

echo "==> Labs: folders, mock data, README, lab.yaml"
python3 "$HERE/build_labs.py" data
echo "==> Lab workflow figures"
python3 "$HERE/build_lab_figures.py"
echo "==> Lab instruction PDFs"
python3 "$HERE/build_labs.py" pdf

echo "==> Slide deck"
python3 "$HERE/build_slides.py"
echo "==> Lesson Plan (slide numbers from slide_map.json)"
python3 "$HERE/build_lesson_plan.py"
echo "==> Learner Guide (DOCX + Markdown mirror)"
python3 "$HERE/build_learner_guide.py"

PPT="$CW/$SHORT-$VER.pptx"; LP="$CW/LP-$SHORT.docx"; LG="$CW/LG-$SHORT.docx"
echo "==> Render PDFs (pass 1)"
"$SOFFICE" --headless --convert-to pdf --outdir "$CW" "$PPT" >/dev/null 2>&1
echo "==> Inject page-numbered TOC (LP + LG) and re-render"
python3 "$HERE/inject_toc2.py" "$LP" 2
python3 "$HERE/inject_toc2.py" "$LG" 2
"$SOFFICE" --headless --convert-to pdf --outdir "$CW" "$LP" >/dev/null 2>&1
"$SOFFICE" --headless --convert-to pdf --outdir "$CW" "$LG" >/dev/null 2>&1

echo "==> Archive superseded versions"
mkdir -p "$CW/archive"
for f in "$CW"/*-v*.pptx "$CW"/*-v*.pdf; do
  [ -e "$f" ] || continue
  case "$(basename "$f")" in *"-$VER."*) ;; *) mv -f "$f" "$CW/archive/";; esac
done
find "$REPO" -name ".DS_Store" -delete 2>/dev/null || true
echo "==> Done:"; ls -1 "$CW"/*.pptx "$CW"/*.docx "$CW"/*.pdf
