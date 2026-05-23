# Ce fichier contient le prompt système de MACS-Assistant
# Modifiez ce texte → committez → Render se met à jour automatiquement

SYSTEM_PROMPT = """
Tu es MACS-Assistant, l'assistant IA dédié à l'atelier de réparation
de machines à coudre. [Collez ici votre prompt complet]
"""

# URL de votre API Render
API_URL = "https://atelier-macs-api.onrender.com"

Thought for 6 seconds
terminal
Executed shell command
grep -n "PrintReception" src/App.tsx
terminal
Executed shell command
grep -n -C 5 "dossiers/\${dossier._id}/print" src/pages/DossierDetail.tsx
terminal
Executed shell command
grep -n "Upload" src/pages/DossierDetail.tsx
description
Read file
Read 1 file: src/pages/DossierDetail.tsx
lightbulb
Thought for 5 seconds
description
Read file
Read 1 file: src/pages/DossierDetail.tsx
lightbulb
Thought for 13 seconds
edit
Edited 1 file
src/pages/DossierDetail.tsx
check_circle
lightbulb
Thought for 5 seconds
description
Read file
Read 1 file: package.json
error
Failed: viewing DossierDetail.tsx
error
Failed: listing source directory
lightbulb
Thought for 3 seconds
error
Failed: listing src directory
error
Failed: viewing App.tsx
error
Failed: compiling the applet
error
Failed: viewing PrintReception.tsx
error
Failed: restarting dev server to unblock
terminal
Executed shell command
grep -rI "class DossierDetail" .
terminal
Executed shell command
grep -r "DossierDetail" .
lightbulb
Thought for 3 seconds
description
Read file
Read 3 files: src/pages/DossierDetail.tsx,src/pages/DossierDetail.tsx, and src/pages/DossierDetail.tsx
lightbulb
Thought for 7 seconds
description
Read file
Read 1 file: src/types.ts
lightbulb
Thought for 3 seconds
terminal
Executed shell command
grep -rn "devis" src/pages/DossierDetail.tsx
lightbulb
Thought for 27 seconds
edit
Edited 1 file
src/pages/PrintDetail.tsx
check_circle
description
Read file
Read 1 file: src/App.tsx
edit
Edited 1 file
src/App.tsx
check_circle
lightbulb
Thought for 3 seconds
description
Read file
Read 2 files: src/pages/DossierDetail.tsx, and src/pages/DossierDetail.tsx
lightbulb
Thought for 5 seconds
edit
Edited 1 file
src/pages/DossierDetail.tsx
check_circle
build
Built
restart_alt
Restarted dev server
