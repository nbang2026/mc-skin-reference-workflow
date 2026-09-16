# MC Skin Studio

> 一套面向 Minecraft 皮肤的两阶段技能套件（素材采集 + 成品锻造），提供 **WorkBuddy 版** 与 **通用版** 两种分发。
> A two-stage Minecraft skin skill suite (reference gathering + skin forging), shipped in **two editions**: WorkBuddy and Generic.

---

## 简介 / Overview

**中文**：做一张"贴进游戏能看、又不被说抄袭"的 Minecraft 64×64 皮肤，常见做法各有坑：手工逐像素画费时且容易比例崩；直接下载现成皮肤常踩原创性雷；照搬单张真实皮肤会被认出是"别人的角色"。本套件把流程拆成「采集可信素材」和「锻造原创成品」两段，各自校验、可追溯来源，输出既合规又好看。

**English**: Producing a Minecraft 64×64 skin that *looks right in-game and isn't flagged as a copy* is harder than it seems. Hand-painting pixel-by-pixel is slow and error-prone; downloading an existing skin risks originality issues; copying a single real skin just reads as "someone else's character." This suite splits the work into *gather trustworthy references* and *forge an original result* — each stage validated, every source traceable, output both compliant and good-looking.

### 背景与痛点 / Background & Pain Points

| 做法 Approach | 问题 Problem |
| --- | --- |
| 手工绘制<br>Hand-drawing | 耗时、易比例崩<br>Slow; proportions easily break |
| 直接下载现成皮肤<br>Downloading as-is | 原创性风险<br>Originality risk |
| 照搬单张真实皮肤<br>Copying one real skin | 被认出是他人角色<br>Recognized as someone else's character |
| 纯白主色<br>Pure-white main color | 游戏内高亮后糊成一片、不可见<br>Washes out under in-game highlight, invisible |

本套件如何逐个解决 / How this suite addresses each:

- **采集阶段**做多源检索 + 像素校验 + 原创性查重，止于「可用素材集」。`The gather stage` does multi-source search + pixel validation + originality dedup, stopping at a "usable reference set."
- **锻造阶段**跨图拼装部件、施加方向性光影、36 面完整性 + 可见性校验，输出原创皮肤。`The forge stage` assembles parts across images, applies directional lighting, runs 36-face completeness + visibility checks, and outputs an original skin.

---

## 工作流总览 / Workflow Overview

```
角色参考图 / 名称
Character image / name
        │
        ▼
┌──────────────────────────┐
│ ① gather-mc-skin-refs    │  素材采集 / Reference Gathering
│   检索 → 下载 → 校验 → 查重 │  search → download → validate → dedup
└──────────────────────────┘
        │  可追溯素材集 / Traceable reference set
        ▼
┌──────────────────────────┐
│ ② forge-mc-skin          │  成品锻造 / Skin Forging
│   拼装 → 光影 → 预览 → 校验 │  assemble → light → preview → validate
└──────────────────────────┘
        │  原创 64×64 皮肤 / Original 64×64 skin
        ▼
   可直接导入 Minecraft / Ready to import into Minecraft
```

**中文**：两个阶段靠"素材集"衔接，可单独跑（例如只采集、只锻造）。
**English**: The two stages connect through the "reference set" and can run independently (e.g. gather only, or forge only).

---

## 两种分发 / Two Editions

两套技能**内容完全一致**，仅安装位置与说明不同。按你使用的智能体任选其一。
Both editions ship **identical skills** — only the install path and notes differ. Pick the one matching your agent.

| 版本 Edition | 适用环境 For | 安装位置 Install path |
| --- | --- | --- |
| [`workbuddy/`](workbuddy/) | WorkBuddy | `~/.workbuddy/skills/` |
| [`generic/`](generic/) | Claude Code / 任意支持 SKILL.md 的智能体<br>Claude Code / any SKILL.md-compatible agent | `~/.claude/skills/` 等 / etc. |

**中文**
- 用 **WorkBuddy** → 进 `workbuddy/`，按其中说明安装到 `~/.workbuddy/skills/`。
- 用 **Claude Code 或其他代理** → 进 `generic/`，按其中说明安装到对应 skills 目录。

**English**
- Using **WorkBuddy** → go into `workbuddy/` and follow its instructions to install under `~/.workbuddy/skills/`.
- Using **Claude Code or another agent** → go into `generic/` and follow its instructions to install under the matching skills directory.

---

## 技能 / The Skills

两个发行版里都包含同样的两条流水线：
Both editions ship the same two pipelines:

| 技能 Skill | 职责 Role | 输入 Input | 输出 Output |
| --- | --- | --- | --- |
| ① `gather-mc-skin-refs` | 素材采集<br>Reference Gathering | 角色参考图 / 名称<br>Character image / name | 可追溯素材集<br>Traceable reference set |
| ② `forge-mc-skin` | 成品锻造<br>Skin Forging | 已校验素材集<br>Validated reference set | 原创 64×64 皮肤<br>Original 64×64 skin |

- **① 素材采集 / Reference Gathering**：多源检索、批量下载、像素校验、原创性查重，止于「可用素材集」。
  Multi-source search, bulk download, pixel validation, originality dedup — ends at a "usable reference set".
- **② 成品锻造 / Skin Forging**：跨图拼装、方向性光影、面朝向预览、36 面完整性 + 可见性校验，输出原创皮肤。
  Cross-image assembly, directional lighting, face-oriented preview, 36-face completeness + visibility check — outputs an original skin.

---

## 何时用哪个 / When to Use Which

| 你的目标 Your goal | 调用 Call |
| --- | --- |
| 已有角色图，想凑一批可用皮肤素材<br>You have a character and want a batch of usable skin sources | `gather-mc-skin-refs` |
| 已有素材集，想合成一张原创皮肤<br>You have a reference set and want to forge one original skin | `forge-mc-skin` |
| 从零到成品一张皮肤<br>From scratch to one finished skin | 先 `gather` 再 `forge` / gather first, then forge |

**中文**：一句话判断——要"素材"用采集，要"皮肤"用锻造，两者都要就顺序跑。
**English**: One-line rule — need *sources* → gather; need a *skin* → forge; need both → run in order.

---

## 快速开始 / Quick Start

**中文**
```bash
# 1) 克隆仓库（若尚未克隆）/ 1) Clone the repo (if not yet)
git clone https://github.com/nbang2026/mc-skin-reference-workflow.git mc-skin-studio
cd mc-skin-studio

# 2) 选一个发行版，例如 WorkBuddy 版 / 2) Pick an edition, e.g. WorkBuddy
cd workbuddy

# 3) 把两个技能复制到技能目录 / 3) Copy both skills into the skills dir
mkdir -p ~/.workbuddy/skills
cp -r gather-mc-skin-refs ~/.workbuddy/skills/
cp -r forge-mc-skin ~/.workbuddy/skills/

# 4) 安装依赖 / 4) Install dependencies
pip install pillow
```
之后在对话里描述角色即可触发对应技能。
Then just describe the character in chat to trigger the matching skill.

**English**
```bash
# 1) Clone the repo (if not yet)
git clone https://github.com/nbang2026/mc-skin-reference-workflow.git mc-skin-studio
cd mc-skin-studio

# 2) Pick an edition, e.g. the Generic edition
cd generic

# 3) Copy both skills into your agent's skills dir (Claude Code shown)
mkdir -p ~/.claude/skills
cp -r gather-mc-skin-refs ~/.claude/skills/
cp -r forge-mc-skin ~/.claude/skills/

# 4) Install dependencies
pip install pillow
```
Then describe the character in chat to trigger the matching skill.

---

## 质量保障 / Quality Assurance

- **36 面完整性** / **36-face completeness**：Minecraft 64×64 共 36 个面，逐面扫描，杜绝漏顶/漏底。
- **原创性查重** / **Originality dedup**：与素材集逐像素比对，确保不是某张原皮肤的照搬。
- **饱和度门槛** / **Saturation guard**：近白结构（如拉链）不被误判为头发而错误重着色。
- **方向性光影** / **Directional lighting**：光来自左上前，横向左→右、纵向上→下单调过渡，无棋盘格噪点。
- **可见性校验** / **Visibility check**：主色带饱和度，避免纯白在游戏高亮下消失。
- **来源可追溯** / **Traceable sources**：每张素材记录检索来源，便于复核。

---

## 仓库结构 / Repository Layout

```
mc-skin-studio/
├── README.md                # 本文件 / this file（总览 overview）
├── workbuddy/               # WorkBuddy 版 / WorkBuddy edition → ~/.workbuddy/skills/
│   ├── README.md            # 安装说明 / install notes（中英双语 bilingual）
│   ├── gather-mc-skin-refs/ # ① 素材采集 / reference gathering
│   └── forge-mc-skin/       # ② 成品锻造 / skin forging
└── generic/                 # 通用版 / generic edition → ~/.claude/skills/ 等 / etc.
    ├── README.md            # 安装说明 / install notes（中英双语 bilingual）
    ├── gather-mc-skin-refs/ # ① 素材采集 / reference gathering
    └── forge-mc-skin/       # ② 成品锻造 / skin forging
```

**中文**：每个发行版目录内含自己的 `README.md`（平台专属安装说明，中英双语），以及两个技能目录（各含 `SKILL.md` 与 `scripts/`）。
**English**: Each edition directory carries its own `README.md` (platform-specific, bilingual install notes) plus the two skill folders (each with `SKILL.md` and `scripts/`).

---

## 环境要求 / Requirements

**中文**：Python ≥ 3.9 + Pillow；跨 macOS / Linux / Windows。采集阶段需联网，锻造阶段可离线。
**English**: Python ≥ 3.9 + Pillow; works on macOS / Linux / Windows. Gathering needs network; forging runs fully offline.

## 许可 / License

MIT
