# WorkBuddy 版 / WorkBuddy Edition

> MC Skin Studio 在 **WorkBuddy** 中的安装版。技能本体与 `generic/` 通用版完全一致，区别仅在安装位置。
> The MC Skin Studio install edition for **WorkBuddy**. Identical skills to the `generic/` edition — only the install path differs.

---

## 安装 / Install

```bash
# 1) 克隆仓库（若尚未克隆）/ 1) Clone the repo (if not yet)
git clone https://github.com/nbang2026/mc-skin-reference-workflow.git mc-skin-studio

# 2) 把两个技能复制到 WorkBuddy 的技能目录 / 2) Copy both skills into WorkBuddy's skills dir
mkdir -p ~/.workbuddy/skills
cp -r workbuddy/gather-mc-skin-refs ~/.workbuddy/skills/
cp -r workbuddy/forge-mc-skin ~/.workbuddy/skills/

# 3) 安装依赖 / 3) Install dependencies
pip install pillow
```

**中文**：完成后，在 WorkBuddy 里直接对话即可触发——提供角色参考图让它「采集素材」，或凭素材让它「锻造皮肤」。
**English**: After this, just talk to WorkBuddy — give a character reference to *gather* materials, or supply materials to *forge* a skin.

---

## 本版内容 / What's Inside

```
workbuddy/
├── README.md            # 本文件 / this file
├── gather-mc-skin-refs/ # ① 素材采集 / Reference Gathering
│   ├── SKILL.md
│   └── scripts/         # download · verify · dedup · part_scan
└── forge-mc-skin/       # ② 成品锻造 / Skin Forging
    ├── SKILL.md
    └── scripts/         # relight · render3d · render3d_body · views ·
                        # render_check · compare · head_zoom · part_scan
```

**中文**：技能以 Anthropic Agent Skills 格式存放，WorkBuddy 直接读取 `SKILL.md` 执行 `scripts/`。
**English**: Skills follow the Anthropic Agent Skills layout; WorkBuddy reads `SKILL.md` and runs `scripts/`.

---

## 依赖 / Requirements

**中文**：Python ≥ 3.9 + Pillow；跨 macOS / Linux / Windows。
**English**: Python ≥ 3.9 + Pillow; macOS / Linux / Windows.
