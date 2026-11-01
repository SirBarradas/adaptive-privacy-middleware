"""Gera o diagrama da arquitetura do middleware (arquitetura.png).

Executar a partir da pasta report/images:  python gerar_arquitetura.py
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(11, 5.6), dpi=200)
F = 1.3  # escala do texto para continuar legível quando a figura ocupa a largura da página
ax.set_xlim(0, 110)
ax.set_ylim(0, 56)
ax.axis("off")


def caixa(x, y, w, h, texto, cor="#ffffff", borda="#333333", fonte=9, negrito=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                fc=cor, ec=borda, lw=1.2))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fonte * F,
            fontweight="bold" if negrito else "normal", wrap=True)


def seta(x1, y1, x2, y2, texto=None, dx=0, dy=1.4, cor="#333333", estilo="-|>"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=estilo, color=cor, lw=1.3))
    if texto:
        ax.text((x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy, texto, ha="center", va="bottom",
                fontsize=7.5 * F, color=cor)


# Clientes
ax.text(9, 53, "Clientes", ha="center", fontsize=10 * F, fontweight="bold")
caixa(2, 40, 14, 7, "Administrador", "#e8f0fe")
caixa(2, 28, 14, 7, "Operacional /\nAnalista", "#e8f0fe")
caixa(2, 16, 14, 7, "Público /\nTerceiros", "#e8f0fe")

# Middleware (fronteira)
ax.add_patch(FancyBboxPatch((25, 3), 58, 49, boxstyle="round,pad=0.4,rounding_size=2",
                            fc="#f6f6f6", ec="#555555", lw=1.4, ls="--"))
ax.text(54, 49.5, "Middleware / Proxy de Privacidade (Python)", ha="center",
        fontsize=10 * F, fontweight="bold")

caixa(28, 38, 22, 7, "1. Autenticação e\nidentificação do perfil", "#fff4e5")
caixa(58, 38, 22, 7, "2. Encaminhamento\ndo pedido", "#fff4e5")
caixa(58, 24, 22, 8, "3. Motor de políticas\n(regras por recurso\ne perfil)", "#fff4e5")
caixa(28, 24, 22, 8, "4. Transformadores\nfiltrar · mascarar ·\npseudonimizar · agregar", "#fff4e5")
caixa(28, 8, 22, 8, "5. Entrega da\nresposta adaptada", "#fff4e5")
caixa(58, 8, 22, 8, "Registo e métricas\nlatência · CPU · memória\n$S_{orig}$, $S_{trans}$, $\\Delta D$", "#eaf6ea")

# Ficheiro de políticas e cofre de pseudónimos
caixa(87, 28, 20, 8, "Políticas\n(configuração\npor perfil)", "#fdeaea")
caixa(87, 14, 20, 8, "Chave / tabela de\npseudonimização\n(guardada à parte)", "#fdeaea")

# Backend
caixa(87, 40, 20, 8, "Serviço de backend\n(API REST)", "#e9e4f5", negrito=True)

# Fluxo
seta(16, 43.5, 28, 41.5, "pedido + token", dy=0.8)
seta(16, 31.5, 28, 40)
seta(16, 19.5, 28, 39)
seta(50, 41.5, 58, 41.5)
seta(80, 43, 87, 44, "pedido", dy=0.4)
seta(87, 42, 80, 40, "resposta\ncompleta", dy=-5.2)
seta(69, 38, 69, 32)
seta(87, 32, 80, 29, estilo="-|>")
seta(58, 28, 50, 28, "regras", dy=0.6)
seta(87, 18, 50, 25.5, estilo="-|>", cor="#a33")
seta(39, 24, 39, 16)
seta(50, 12, 58, 12, estilo="-|>", cor="#2b7a2b")
seta(28, 12, 9, 15, "resposta adaptada\nao perfil", dx=-2, dy=-6.5)

# Rejeição
ax.text(39, 35.8, "token inválido → 401/403\n(sem acesso ao backend)", ha="center",
        va="top", fontsize=7 * F, color="#a33", style="italic")

plt.tight_layout()
plt.savefig("arquitetura.png", bbox_inches="tight")
