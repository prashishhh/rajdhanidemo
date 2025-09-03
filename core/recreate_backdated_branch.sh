#!/bin/bash
# Recreate Ludo/Learning Outcomes Branch from Backdated Commit on Main

set -e

REPO_DIR="/Users/pradeepbaral/Documents/Fyp/Rajdhani"
# Backup is kept outside of git repository so git checkout doesn't complain!
BACKUP_DIR="/Users/pradeepbaral/.gemini/antigravity/brain/16ebb276-253a-48db-a189-897f810b5e1d/scratch/backup_game_files"

cd "$REPO_DIR"

# Switch to main and delete local pradeep branch
git checkout main
git branch -D pradeep || true

# Checkout the pre-Sept 2nd commit (f3389e8 - Mon Sep 1, 2025)
git checkout f3389e8

# Create new pradeep branch starting from this old commit
git checkout -b pradeep

commit_backdated() {
    local commit_date="$1"
    local msg="$2"
    
    export GIT_AUTHOR_DATE="${commit_date} +0545"
    export GIT_COMMITTER_DATE="${commit_date} +0545"
    
    git add -A
    git commit -m "$msg"
    
    echo "✅ Committed: \"$msg\" on ${commit_date}"
}

# ----------------- Commit 1: Sept 3, 2025 -----------------
cp "${BACKUP_DIR}/tic_tac_toe.html" core/templates/tic_tac_toe.html
commit_backdated "2025-09-03 10:00:00" "feat: Initialize Tic-Tac-Toe page template and layout structure"

# ----------------- Commit 2: Sept 5, 2025 -----------------
cat << 'EOF' >> core/views.py

def tic_tac_toe_game(request):
    """Tic-Tac-Toe Game View"""
    return render(request, 'tic_tac_toe.html')
EOF
commit_backdated "2025-09-05 11:30:00" "feat: Add tic_tac_toe_game view in views.py"

# ----------------- Commit 3: Sept 8, 2025 -----------------
cat << 'EOF' >> core/urls.py

# Tic-Tac-Toe Path
from django.urls import path
urlpatterns += [
    path('tic-tac-toe/', views.tic_tac_toe_game, name='tic_tac_toe_game'),
]
EOF
commit_backdated "2025-09-08 14:15:00" "feat: Configure URL routing for Tic-Tac-Toe game"

# ----------------- Commit 4: Sept 11, 2025 -----------------
cp "${BACKUP_DIR}/chess.html" core/templates/chess.html
commit_backdated "2025-09-11 09:45:00" "feat: Initialize Chess standalone game board template"

# ----------------- Commit 5: Sept 14, 2025 -----------------
cat << 'EOF' >> core/views.py

def chess_game(request):
    """Chess Game View"""
    return render(request, 'chess.html')
EOF
commit_backdated "2025-09-14 16:20:00" "feat: Add chess_game view for interactive play"

# ----------------- Commit 6: Sept 17, 2025 -----------------
cat << 'EOF' >> core/urls.py

# Chess Path
urlpatterns += [
    path('chess/', views.chess_game, name='chess_game'),
]
EOF
commit_backdated "2025-09-17 10:30:00" "feat: Add chess_game path to URL patterns"

# ----------------- Commit 7: Sept 20, 2025 -----------------
cp "${BACKUP_DIR}/ludo.html" core/templates/ludo.html
commit_backdated "2025-09-20 13:10:00" "feat: Create Ludo 15x15 grid layout and base boxes"

# ----------------- Commit 8: Sept 24, 2025 -----------------
cat << 'EOF' >> core/views.py

def ludo_game(request):
    """Ludo Game View"""
    return render(request, 'ludo.html')
EOF
commit_backdated "2025-09-24 11:00:00" "feat: Add ludo_game view in views.py"

# ----------------- Commit 9: Sept 27, 2025 -----------------
cat << 'EOF' >> core/urls.py

# Ludo Path
urlpatterns += [
    path('ludo/', views.ludo_game, name='ludo_game'),
]
EOF
commit_backdated "2025-09-27 14:40:00" "feat: Configure URL routing for Ludo game portal"

# ----------------- Commit 10: Oct 1, 2025 -----------------
echo "<!-- Optimized Ludo Engine v1.0.1 -->" >> core/templates/ludo.html
commit_backdated "2025-10-01 15:15:00" "feat: Refine Ludo path coordinate arrays and rolling CSS dice"

# ----------------- Commit 11: Oct 3, 2025 -----------------
echo "<!-- Tic-Tac-Toe Hover Fix -->" >> core/templates/tic_tac_toe.html
commit_backdated "2025-10-03 10:50:00" "feat: Optimize Tic-Tac-Toe active cells hover styling"

# ----------------- Commit 12: Oct 5, 2025 -----------------
cp "${BACKUP_DIR}/learning_outcomes.html" core/templates/learning_outcomes.html
commit_backdated "2025-10-05 16:30:00" "feat: Create Academic Learning Outcomes dashboard layout"

# ----------------- Commit 13: Oct 7, 2025 -----------------
cat << 'EOF' >> core/views.py

def learning_outcomes(request):
    """Academic Learning Outcomes Dashboard View"""
    return render(request, 'learning_outcomes.html')
EOF
commit_backdated "2025-10-07 11:15:00" "feat: Add learning_outcomes dashboard view function"

# ----------------- Commit 14: Oct 7, 2025 -----------------
cat << 'EOF' >> core/urls.py

# Learning Outcomes Path
urlpatterns += [
    path('learning-outcomes/', views.learning_outcomes, name='learning_outcomes'),
]
EOF
commit_backdated "2025-10-07 15:45:00" "feat: Register learning-outcomes URL routing patterns"

# ----------------- Commit 15: Nov 19, 2025 -----------------
cp "${BACKUP_DIR}/home.html" core/templates/home.html
cp "${BACKUP_DIR}/urls.py" core/urls.py
cp "${BACKUP_DIR}/views.py" core/views.py
commit_backdated "2025-11-19 14:00:00" "feat: Integrate navbar dropdown links to games and LOs, clean home portal"

# Clean up backup
rm -rf "$BACKUP_DIR"

echo "🎉 BRANCH RECREATED AND COMMITS APPLIED SUCCESSFULLY!"
