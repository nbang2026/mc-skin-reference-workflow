# 通用版 / Generic Edition

> MC Skin Studio 的**通用发行版**，适用于任何支持 Anthropic Agent Skills 格式（`SKILL.md` + `scripts/`）的智能体，例如 Claude Code、或其它可读取 `SKILL.md` 并执行 Python 脚本的代理。技能本体与 `workbuddy/` 版完全一致，区别仅在安装位置。
> The **generic edition** of MC Skin Studio, for any agent that supports the Anthropic Agent Skills layout (`SKILL.md` + `scripts/`) — e.g. Claude Code, or any proxy that can read `SKILL.md` and run Python scripts. Identical skills to the `workbuddy/` edition — only the install path differs.

---

## 安装 / Install

```bash
# 1) 克隆仓库（若尚未克隆）
git clone https://github.com/nbang2026/mc-skin-reference-workflow.git mc-skin-studio

# 2) 把两个技能复制到你的智能体技能目录（以 Claude Code 为例）
mkdir -p ~/.claude/skills
cp -r generic/gather-mc-skin-refs ~/.claude/skills/
cp -r generic/forge-mc-skin ~/.claude/skills/

# 其他代理：把上面路径换成该代理的 skills 目录即可
# Other agents: replace the path above with that agent's skills directory.

# 3) 安装依赖
pip install pillow
```

**中文**：复制完成后，在对应智能体里对话即可触发——给角色参考图「采集素材」，或凭素材「锻造皮肤」。
**English**: Once copied, just prompt your agent — give a character reference to *gather* materials, or supply materials to *forge* a skin.

---

## 本版内容 / What's Inside

```
generic/
├── README.md            # 本文件
├── gather-mc-skin-refs/ # ① 素材采集 / Reference Gathering
│   ├── SKILL.md
│   └── scripts/         # download · verify · dedup · part_scan
└── forge-mc-skin/       # ② 成品锻造 / Skin Forging
    ├── SKILL.md
    └── scripts/         # relight · render3d · render3d_body · views ·
                        # render_check · compare · head_zoom · part_scan
```

**中文**：标准 `SKILL.md` 格式，不含任何平台专有字段，可放任意兼容智能体。
**English**: Standard `SKILL.md` format with no platform-specific fields — drop it into any compatible agent.

---

## 依赖 / Requirements

**中文**：Python ≥ 3.9 + Pillow；跨 macOS / Linux / Windows。
**English**: Python ≥ 3.9 + Pillow; macOS / Linux / Windows.
