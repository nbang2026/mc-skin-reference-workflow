---
name: forge-mc-skin
description: >-
  锻造原创 Minecraft 皮肤——基于已校验素材集跨图拼装部件、施加方向性光影与面朝向光照，经 36 面完整性与可见性校验输出 64×64 成品皮肤。当用户要求将素材拼成皮肤、为角色制作皮肤或重着色已有皮肤时调用。
  / Forge an original Minecraft skin: cross-assemble parts from a validated reference set, apply directional lighting and face-oriented shading, then validate 36-face completeness and visibility to output a 64×64 skin. Trigger when the user wants to assemble references into a skin, build a character skin from scratch, or recolor an existing skin.
agent_created: true
---

# 成品皮肤锻造 / MC Skin Forging

## 1. 职责范围 / Scope

**输入 Input**：经 `gather-mc-skin-refs` 产出的已校验素材集（或多张候选皮肤）。
**输出 Output**：一张原创 64×64 Minecraft 皮肤（含 overlay 层），附三视图预览与校验报告。

### 能力边界 / Capability Boundary

| 包含（本技能）In scope | 不包含（交由 gather-mc-skin-refs）Out of scope |
|---|---|
| 跨图部件拆解与拼装 Cross-image part disassembly & assembly | 角色识别与联网检索 Character ID & web search |
| 方向性光影重着色 Directional lighting recolor | 批量下载与完整性采集 Bulk download & collection |
| 面朝向光照渲染预览 Face-oriented shaded preview | 素材原创性查重 Originality dedup (done pre-assembly by A) |
| 36 面完整性 + 可见性校验 36-face completeness & visibility check | — |

本技能止于「成品皮肤」；素材的检索、下载与查重由 `gather-mc-skin-refs` 前置完成。
This skill stops at the "finished skin"; reference search, download and dedup are handled upstream by `gather-mc-skin-refs`.

## 2. 触发条件 / When to Use

满足以下任一条件时调用 / Call this skill when any of the following applies:

- 已有参考素材，要求拼装成某角色的成品皮肤； / already have reference material and want it assembled into a finished skin for a character;
- 要求为角色从头制作一张 Minecraft 皮肤； / want a Minecraft skin built for a character from scratch;
- 要求对既有皮肤施加方向性光影或重着色。 / want directional lighting or recoloring applied to an existing skin.

**不适用 Not applicable**：仅要检索/下载素材（转 `gather-mc-skin-refs`）。
/ Pure retrieval/download of material should be routed to `gather-mc-skin-refs`.

## 3. 核心流程 / Workflow

1. **部件体检 Part health-check** —— 对候选素材逐部件扫描（头/躯干/双臂/双腿的顶/底/前/后/左/右），标记空洞与近白像素，仅取六面完整、配色有饱和度的来源。
   Scan each candidate part (head/torso/both arms/both legs — top/bottom/front/back/left/right) for holes and near-white pixels; keep only sources that are six-face complete and have saturated colors.
2. **跨图拼装 Cross-image assembly** —— 按 UV 坐标整块搬运部件（头取 A、躯干取 B、腿取 C），而非仅正面，避免侧面残影；不照搬单张，确保为拼装原创。
   Move parts as whole UV blocks (head from A, torso from B, legs from C) — not just the front face — to avoid side ghosting; never copy a single skin verbatim, so the result is an assembled original.
3. **光影重着色 Lighting recolor** —— 将头发/衣料映射到方向性色阶（光源定左上前方），保留分缕结构；近白结构（拉链/描边）加饱和度门槛保护，不被误改。
   Map hair/fabric onto a directional ramp (light from upper-left-front), preserving strand structure; guard near-white structures (zippers/outlines) with a saturation threshold so they are not mis-edited.
4. **面朝向渲染 Face-oriented render** —— 按 MC 规则（顶 1.0 / 正 0.8 / 侧 0.6 / 底 0.5）等轴测渲染前/右/顶三面，输出预览供目视复核。
   Render front/right/top faces isometrically per MC rules (top 1.0 / front 0.8 / side 0.6 / bottom 0.5) and output a preview for visual review.
5. **成品校验 Output validation** —— 扫描 36 面无透明洞、配色有饱和度（避免游戏内糊掉），并做拼装后原创性差异率判定。
   Scan that all 36 faces have no transparent holes, colors are saturated (to avoid washing out in-game), and compute a post-assembly originality diff rate.

## 4. 关键原则 / Key Principles

- 严禁整体照搬单张真实皮肤，必须跨图拼装。 / Never copy a single real skin wholesale; cross-image assembly is mandatory.
- 禁用纯白/近白主色（饱和度≈0 在游戏高亮下不可见）；白色只做描边/小面积高光。 / No pure/near-white main colors (saturation≈0 vanishes under in-game highlight); white is for outlines/small highlights only.
- 光影须方向性单调过渡，禁棋盘格抖动；单一主色系 + 冷暖对比，≥6 档色阶。 / Lighting must transition directionally and monotonically — no checkerboard dithering; one hue family + warm/cool contrast, ≥6 ramp steps.
- 头/身/双臂/双腿的 36 面（含顶底面）必填，漏填即建模空洞。 / All 36 faces of head/torso/both arms/both legs (including top & bottom) must be filled; a gap means a modeling hole.
