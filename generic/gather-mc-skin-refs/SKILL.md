---
name: gather-mc-skin-refs
description: >-
  采集 Minecraft 皮肤素材——从角色参考图或名称出发，经多源检索、批量下载、像素校验与原创性查重，产出可追溯的已筛选素材集。当用户要求识别角色并查找皮肤、下载皮肤素材或构建素材库时调用。
  / Gather Minecraft skin references: from a character image or name, run multi-source search, bulk download, pixel validation and originality dedup to produce a traceable, pre-filtered material set. Trigger when the user wants to identify a character and find skins, download skin material, or build a reference library.
agent_created: true
---

# 皮肤素材采集 / MC Skin Reference Gathering

## 1. 职责范围 / Scope

**输入 Input**：一张或多张角色参考图（或已知角色名）。
**输出 Output**：一份经像素级验证的 Minecraft 皮肤素材集，存于独立目录，附筛选与来源报告。

### 能力边界 / Capability Boundary

| 包含（本技能）In scope | 不包含（交由 forge-mc-skin）Out of scope |
|---|---|
| 参考图特征提取 Reference feature extraction | 皮肤部件拆解 Skin part disassembly |
| 多源检索与直链获取 Multi-source search & direct links | 跨图部件拼装 Cross-image assembly |
| 批量下载与完整性校验 Bulk download & integrity check | 颜色重映射 / 重着色 Color remap / recolor |
| 像素特征判定与分类 Pixel feature judging & classification | 成品皮肤生成与 UV 校验 Skin generation & UV check |
| 原创性查重与来源标记 Originality dedup & source tagging | — |

本技能止于「可用素材集」；下游的部件拼装与成品生成由 `forge-mc-skin` 承担。
This skill stops at a "usable material set"; downstream part assembly and skin generation are owned by `forge-mc-skin`.

## 2. 触发条件 / When to Use

满足以下任一条件时调用 / Call this skill when any of the following applies:

- 提供角色参考图，要求检索并下载对应 Minecraft 皮肤； / provide a character image and want the matching Minecraft skin searched & downloaded;
- 提供角色名称，要求收集该角色的皮肤素材； / provide a character name and want that character's skin material collected;
- 提及「找参考皮肤」「下载皮肤素材」「构建素材库」。 / mention "find reference skins", "download skin material", or "build a reference library".

**不适用 Not applicable**：要求直接产出成品皮肤，或对既有素材做拼装改造（转 `forge-mc-skin`）。
/ Directly producing a finished skin or modifying material by assembly should be routed to `forge-mc-skin`.

## 3. 核心流程 / Workflow

1. **特征提取 Feature extraction** —— 从参考图提取可检索标识（作品名、角色名中/英/罗马音）与校验特征（发色、瞳色及异色瞳左右分配、服饰款式、标志配件）。
   Extract searchable IDs (title, character name in CN/EN/romaji) and validation features (hair color, eye color & heterochromia side, outfit style, signature accessories).
2. **多源检索 Multi-source search** —— 按可靠性降序：主源取皮肤直链，备用源按玩家名取皮，通用搜索兜底；主源失效自动回退。
   Search by reliability: primary source for skin direct links, fallback by player name, generic search as last resort; auto-fall-back if the primary fails.
3. **批量下载 Bulk download** —— 设浏览器 UA 绕过反爬，指数退避重试，幂等跳过已下载；单批 5–20 个（<5 强制扩查，>20 按可靠性截断）。
   Use a browser UA to bypass anti-scraping, retry with exponential backoff, skip already-downloaded idempotently; batch 5–20 (force expansion if <5, truncate by reliability if >20).
4. **像素校验 Pixel validation** —— 尺寸白名单 `{64×64, 64×32}`；逐像素判定发色/瞳色/服饰是否吻合，剔除错标文件。
   Size whitelist `{64×64, 64×32}`; judge hair/eye/outfit per-pixel for match and drop mislabeled files.
5. **原创性查重 Originality dedup** —— 像素指纹（抓完全/近重复）+ 逐像素差异率（抓改色衍生）+ 可选 AI 视觉比对（抓语义同源）；命中者禁止标为原创。
   Pixel fingerprint (exact/near-duplicate) + per-pixel diff rate (recolor variants) + optional AI visual match (semantic clones); matches must not be tagged original.

## 4. 闭环自检 / Closed-loop Self-check

以整批为单位闭环：全批通过方进下一轮；程序环节失败整批重采，视觉复核失败仅剔单文件；连续三轮无进展主动中止并提示人工。
Close the loop per batch: advance only when the whole batch passes; re-collect the batch on a program failure, drop single files on visual-review failure; abort and ask a human after three fruitless rounds.

## 5. 关键原则 / Key Principles

- 文件名不可信，一切以像素校验为准。 / File names are not trusted; pixel validation is the only source of truth.
- 来源必须可追溯，报告逐文件标注出处。 / Sources must be traceable; the report tags each file's origin.
- 零饱和度色（纯白）在游戏高亮下与背景融为不可见，须在校验阶段拦截。 / Zero-saturation colors (pure white) merge with the background under in-game highlight and must be blocked at validation.
- 素材隔离：下载物存独立目录，不污染、不覆盖既有文件。 / Material isolation: downloads go to a dedicated directory, never polluting or overwriting existing files.
