Deploy instructions — Floxo AI (static `ui/` folder)

Option A — Quick deploy to Netlify (recommended)
1. I have created `site.zip` containing the contents of the `ui/` folder in the project root.
2. Open https://app.netlify.com → Sites → "Add new site" → "Deploy manually" → drag-and-drop `site.zip`.
3. After deploy, Netlify will provide a public URL with HTTPS. You can rename the site or connect a custom domain.

Option B — GitHub Pages (alternative)
1. Create a GitHub repo and push the `ui/` folder or the whole project.
2. In repo Settings → Pages set Source to `main` branch and `/ (root)` or `gh-pages` branch if using that.
3. GitHub Pages publishes at `https://<your-username>.github.io/<repo>/`.

PowerShell command (if you want to re-create `site.zip` locally):

```powershell
cd "C:\Users\LENOVO\OneDrive\Desktop\ai viral videos"
Compress-Archive -Path ui\* -DestinationPath site.zip -Force
```

Notes
- Keep `index.html` at the root of the deployed folder (inside the zip). The current site uses `index.html` in `ui/` which is why we zipped `ui/*`.
- `netlify.toml` is present with `publish = "ui"` in case you prefer to connect a Git repo — you can change that to `publish = "."` if deploying the repo root.

If you want, I can now:
- Upload the `site.zip` into Netlify using your account (you'll need to log in and provide access), or
- Create a GitHub repo and push code for continuous deploy.
