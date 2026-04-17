@echo off
:: BCP - Bundle, Commit, Push astermots.html to GitHub Pages
cd /d %~dp0
echo [1/3] Bundling astermots.html...
python bundle.py
if %errorlevel% neq 0 (echo BUNDLE FAILED & exit /b 1)
echo [2/3] Committing...
git add astermots.html index.html
git commit -m "Deploy: rebuild astermots.html bundle"
echo [3/3] Pushing to GitHub Pages...
git push origin main
echo Done! Site will update at https://lzzzfelipe.github.io/astermots/astermots.html
