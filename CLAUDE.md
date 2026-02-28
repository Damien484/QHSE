# CLAUDE.md — Règles permanentes pour le projet QHSE

## Skills disponibles

Ce projet utilise les superpowers (obra/superpowers) et le skill UI/UX Pro Max.
Invoque toujours le skill approprié **avant** d'agir.

### Skills clés à invoquer

| Tâche | Skill à utiliser |
|-------|-----------------|
| Nouvelle fonctionnalité complexe | `brainstorming` → `writing-plans` → `executing-plans` |
| Bug à corriger | `systematic-debugging` |
| Code à livrer | `verification-before-completion` |
| Interface (composant, page, dashboard) | `ui-ux-pro-max` |
| Tests | `test-driven-development` |
| Revue de code | `requesting-code-review` / `receiving-code-review` |

---

## Règles UI/UX obligatoires

**Pour tout travail sur l'interface (frontend, templates HTML, composants), invoquer impérativement le skill `ui-ux-pro-max` puis :**

### 1. Toujours commencer par générer un design system

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<type produit> <industrie> <mots-clés>" --design-system -p "Nom du projet"
```

### 2. Checklist pré-livraison (obligatoire)

- [ ] Aucun emoji utilisé comme icône (SVG Heroicons/Lucide uniquement)
- [ ] `cursor-pointer` sur tous les éléments cliquables
- [ ] Transitions fluides (150-300ms)
- [ ] Contraste texte 4.5:1 minimum en mode clair
- [ ] Focus states visibles (navigation clavier)
- [ ] `prefers-reduced-motion` respecté
- [ ] Responsive : 375px, 768px, 1024px, 1440px
- [ ] Pas de scroll horizontal sur mobile

### 3. Règles critiques d'accessibilité

- Ratio de contraste minimum 4.5:1 pour le texte normal
- Zones cliquables minimum 44×44px (touch targets)
- Alt text sur toutes les images
- Labels associés aux champs de formulaire

### 4. Anti-patterns interdits

- Emojis comme icônes UI
- Transforms au hover qui décalent le layout
- Texte trop petit (< 16px) sur mobile
- Éléments interactifs sans retour visuel
- Contenu masqué derrière une navbar fixe

---

## Stack de référence

- **Backend** : Flask / Python (SQLAlchemy, SQLite)
- **Frontend par défaut** : HTML + Tailwind CSS
- **Génération de documents** : ReportLab (PDF), python-docx (DOCX)

## Workflow de développement

1. **Jamais de push direct sur `main`** — toujours via une branche `claude/...`
2. Lancer les tests avant toute PR : `pytest tests/`
3. Linter : `flake8 backend/ --max-line-length=120`
