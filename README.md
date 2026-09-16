# MC Skin Studio

> 一套面向 Minecraft 皮肤的两阶段技能套件（素材采集 + 成品锻造），提供 **WorkBuddy 版** 与 **通用版** 两种分发。
> A two-stage Minecraft skin skill suite (reference gathering + skin forging), shipped in **two editions**: WorkBuddy and Generic.

---

## 两种分发 / Two Editions

两套技能**内容完全一致**，仅安装位置与说明不同。按你使用的智能体任选其一。

Both editions ship **identical skills** — only the install path and notes differ. Pick the one matching your agent.

| 版本 Edition | 适用环境 For | 安装位置 Install path |
| --- | --- | --- |
| [`workbuddy/`](workbuddy/) | WorkBuddy | `~/.workbuddy/skills/` |
| [`generic/`](generic/) | Claude Code / 任意支持 SKILL.md 的智能体 | `~/.claude/skills/` 等 |

**中文**
- 用 **WorkBuddy** → 进 `workbuddy/`，按其中说明安装到 `~/.workbuddy/skills/`。
- 用 **Claude Code 或其他代理** → 进 `generic/`，按其中说明安装到对应 skills 目录。

**English**
- Using **WorkBuddy** → go into `workbuddy/` and follow its instructions to install under `~/.workbuddy/skills/`.
- Using **Claude Code or another agent** → go into `generic/` and follow its instructions to install under the matching skills directory.

---

## 技能 / The Skills

两个发行版里都包含同样的两条流水线：

| 技能 Skill | 职责 Role | 输入 Input | 输出 Output |
| --- | --- | --- | --- |
| ① `gather-mc-skin-refs` | 素材采集 Reference Gathering | 角色参考图 / 名称 | 可追溯素材集 |
| ② `forge-mc-skin` | 成品锻造 Skin Forging | 已校验素材集 | 原创 64×64 皮肤 |

- **① 素材采集**：多源检索、批量下载、像素校验、原创性查重，止于「可用素材集」。
- **② 成品锻造**：跨图拼装、方向性光影、面朝向预览、36 面完整性 + 可见性校验，输出原创皮肤。

---

## 仓库结构 / Repository Layout

```
mc-skin-studio/
├── README.md                # 本文件（总览 / overview）
├── workbuddy/               # WorkBuddy 版（安装到 ~/.workbuddy/skills/）
│   ├── README.md            # 该版本的中英双语安装说明
│   ├── gather-mc-skin-refs/ # ① 素材采集
│   └── forge-mc-skin/       # ② 成品锻造
└── generic/                 # 通用版（安装到 ~/.claude/skills/ 等）
    ├── README.md            # 该版本的中英双语安装说明
    ├── gather-mc-skin-refs/ # ① 素材采集
    └── forge-mc-skin/       # ② 成品锻造
```

**中文**：每个发行版目录内含自己的 `README.md`（平台专属安装说明，中英双语），以及两个技能目录（各含 `SKILL.md` 与 `scripts/`）。
**English**: Each edition directory carries its own `README.md` (platform-specific, bilingual install notes) plus the two skill folders (each with `SKILL.md` and `scripts/`).

---

## 环境要求 / Requirements

**中文**：Python ≥ 3.9 + Pillow；跨 macOS / Linux / Windows。采集阶段需联网，锻造阶段可离线。
**English**: Python ≥ 3.9 + Pillow; works on macOS / Linux / Windows. Gathering needs network; forging runs fully offline.

## 许可 / License

MIT
