# CONTEXT — cyber-neo

> Formato compatible con Claude y Antigravity AI  
> Última actualización: 2026-04-19  
> ⚠️ Este archivo extiende y complementa el `CLAUDE.md` existente. No reemplaza su contenido.

## Resumen Ejecutivo

**cyber-neo** es un agente de seguridad de código abierto que se ejecuta como plugin de Claude Code. Escanea proyectos locales en busca de vulnerabilidades según **OWASP 2025 Top 10** y **CWE Top 25**, generando reportes priorizados con guía de remediación accionable.

**Rol en el ecosistema**: Es la herramienta de auditoría estática que @erk puede invocar sobre cualquier proyecto local antes de integrar o publicar código.

## Stack Tecnológico

| Componente | Tecnología |
|---|---|
| Lenguaje | Python (solo stdlib) + Markdown |
| Motor de Análisis | Claude Code (LLM nativo) |
| Analizadores externos (opcionales) | Semgrep, Trivy, Gitleaks |
| Protocolo | MCP (skill via `mcp_server.py`) |
| Licencia | MIT |

## Componentes Principales

```
cyber-neo/
├── CLAUDE.md                          # Guidelines para agentes contribuidores
├── mcp_server.py                      # Servidor MCP (check_lockfiles, scan_secrets)
├── skills/cyber-neo/
│   ├── SKILL.md                       # Prompt maestro (el producto core)
│   ├── scripts/
│   │   ├── scan_secrets.py            # Escáner de secretos por regex
│   │   └── check_lockfiles.py         # Verificador de integridad de lockfiles
│   └── references/                    # Base de conocimiento de seguridad
│       ├── owasp-top-10.md
│       ├── cwe-top-25.md
│       ├── secrets-patterns.md
│       ├── lang-python.md
│       ├── lang-javascript.md
│       ├── iac-docker.md
│       └── report-template.md
└── README.md
```

## Skills MCP Expuestas

| Herramienta | Descripción |
|---|---|
| `check_lockfiles` | Verifica integridad de lockfiles (supply chain) |
| `scan_secrets` | Escanea directorio buscando secretos expuestos |

## Interrelaciones con Otros Proyectos

| Proyecto | Tipo de Relación |
|---|---|
| **carbonioClaw** | carbonioClaw puede invocar cyber-neo para auditar skills antes de registrarlas |
| **breakerClaw** | Complementario: cyber-neo hace análisis estático, breakerClaw hace dinámico |
| **OmniSync / Vibe-Voice** | Proyectos candidatos a auditoría periódica con cyber-neo |
| **superpowers** | Sigue el mismo patrón de skill architecture (SKILL.md + references) |

## Comandos Principales

```bash
# Servidor MCP
python3 /home/erk/cyber-neo/mcp_server.py

# Escaneo de secretos en un proyecto
python3 skills/cyber-neo/scripts/scan_secrets.py /ruta/al/proyecto

# Verificación de lockfiles
python3 skills/cyber-neo/scripts/check_lockfiles.py /ruta/al/proyecto
```

## Notas para Agentes

- Claude ES el motor de análisis. `SKILL.md` es el producto. No es necesario Semgrep para funcionar.
- Los scripts Python usan solo stdlib — sin dependencias externas.
- Siempre modo READ-ONLY sobre el proyecto objetivo. Nunca modificar, nunca ejecutar código del target.
- Clasificar todos los hallazgos con CWE ID + categoría OWASP 2025.
