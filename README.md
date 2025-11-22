# Student Performance Analyzer

Small Flask app that uses Supabase as a backend to store `students`, `courses`, and `grades`.

## Quick start (Windows PowerShell)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

3. Create a `.env` file (copy from `.env.example`) and add your Supabase values:

```powershell
copy .env.example .env
# then edit .env to paste your keys
```

4. Run the app:

```powershell
python .\app.py
```

Open http://localhost:5000 in your browser.

## Database setup

The SQL migration is at `supabase/migrations/20251109165013_create_student_performance_schema.sql`.

- To create the tables in your Supabase project, open the Supabase SQL Editor and paste the SQL there, or use the `supabase` CLI to apply migrations.
- Ensure your Supabase project allows the operations you need. This migration enables permissive RLS policies for demo purposes — do not use these policies in production.

## Security & cleanup (important)

It looks like a `.env` with Supabase keys exists in the repository root. That file contains sensitive keys and must NOT be committed.

Recommended steps (run from project root):

```powershell
# 1) Remove the file from the Git index (stop tracking), then commit
git rm --cached .env
git commit -m "Remove .env from repository"

# 2) Rotate the Supabase anon key in the Supabase dashboard
#    (generate a new anon key and update your local .env)

# 3) If the secret was pushed to remote history, purge it from history using a tool like BFG or git filter-repo.
#    Example with BFG (run outside PowerShell if not installed):
#    bfg --delete-files .env
#    git reflog expire --expire=now --all && git gc --prune=now --aggressive
```

If you want, I can prepare a commit that adds `.env.example` and updates `.gitignore` (already included here). I cannot rotate keys for you — do that in the Supabase dashboard.

## Files added

- `.env.example` — example environment variables
- `.gitignore` updated to ignore `.venv` and caches
- `README.md` — this file

## Next suggestions

- Add a `LICENSE` file if you plan to share the repo publicly.
- Consider removing the permissive RLS policies in `supabase/migrations` and replace them with tighter policies for production.
- Add automated tests for the Flask routes.
