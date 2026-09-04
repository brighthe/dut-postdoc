---
title: "Benchmark 算例原始文件归档索引"
tags:
  - postdoc
  - benchmark-case
  - source-archive
  - BDF
status: "active"
date_added: 2026-09-03
date_update: 2026-09-03
---

# Benchmark 算例原始文件归档索引

> 本页登记 `research/benchmark-cases/` 所依赖的全部原始算例文件，并作为算例页 frontmatter 中逻辑标识 `source: "DLUTFEM-20260720:<包内相对路径>"` 的**唯一解析器**：拿到标识后到本页查文件名、SHA-256 与归档位置，不依赖任何本机路径。

## 存储与解析规则

- **数据包**：`DLUTFEM-20260720`，第三方 FEM 交付物随附的 Nastran BDF 算例，共 18 个文件、约 310 MB；无 DOI、无第三方托管，属不可再生原件，人拥有、AI 只读、永不修改。
- **主档（iCloud）**：`iCloudDrive/博士后-大连理工大学/dut-institute-work-原件/hpc/程序与手册/DLUTFEM-20260720/testcases/`（随交付物程序与手册一并归档；2026-09-03 逐文件核对，18 个文件 SHA-256 与本表一致）。
- **本地副本**：`sources/DLUTFEM-20260720/testcases/*.bdf`，仅供 AI 读取与复原，`.gitignore` 排除、不入 Git；与 `literature/**/sources/` 的论文 PDF 缓存同构。
- **校验**：算例页 frontmatter 的 `source_sha256` 必须与本表一致；不一致时以原件为准并在页面标注。
- **表中「使用页面」**：登记直接从该文件复原数学模型的算例页；未被引用的文件只登记不解读。

## 文件清单

| 文件 | 求解序列 | 大小（字节） | 最后修改 | SHA-256 | 使用页面 |
|---|---|---|---|---|---|
| `100-mix12d-mpcnested.bdf` | `SOL 101` | 4,640 | 2025-12-22 17:08:38 | `B7CD90B5197749AEA7BCE4F3AA58BDCFC4E909B1541736978F18DF54D834FB7F` | — |
| `100w-mix23d-rbe.bdf` | `SOL 101` | 37,016,445 | 2025-12-11 14:19:08 | `58D9827D1AA1CF0BC0052D6EE61A40BBFA610457D0FD68FB6FADF605634990C9` | — |
| `100w-mix23d.bdf` | `SOL 101` | 37,015,648 | 2025-12-11 13:17:20 | `43F1031B5BD846B79E8622ACEC2F0783FCA5E431C2FF75A9ADF4A3EFD49424FC` | — |
| `10w-3d-mpc-1st.bdf` | `SOL 101` | 13,121,378 | 2025-12-17 13:04:08 | `2FF21C9BB2BF64614A860F2989B4C606248C8D28F4977218A0BBA6D628DBA704` | — |
| `10w-3d.bdf` | `SOL 101` | 15,082,200 | 2025-12-10 13:41:34 | `7E2710699A96E5F24A28EE130587A337B38D6E0421A0EB4F9C031E6FDB50068A` | [[10w-3d-linear-elasticity-model]] |
| `10w-mix013d.bdf` | `SOL 101` | 15,015,344 | 2025-12-10 14:51:08 | `A7A43A4287FF2E39C061A104DC77C0B44B027BD80A3E9C0CBA51093C56AA2A71` | — |
| `10w-mix12d-mpcnested.bdf` | `SOL 101` | 1,624,826 | 2025-12-22 18:51:14 | `C5A3DFB7C27C8D8E9650FBEAE9739E8036D83F483ECABA664BCC16C5FDC422B1` | — |
| `1k-cquad4-2case.bdf` | `SOL 101` | 10,252 | 2026-01-09 12:06:00 | `9238950AC377141A2C6CFB8C365F448B72589782D0F84EEB49A3B9E8DF928709` | — |
| `50w-2d-allF_M_P.bdf` | `SOL 101` | 17,638,595 | 2026-01-04 14:53:40 | `A26F9F3D26953F471A41371CBD2D8E93774286E8032312C80959B71DD8243E3E` | — |
| `50w-2d-pload.bdf` | `SOL 101` | 14,287,320 | 2026-01-22 11:46:50 | `FF8A319DDBD7F9358295BD5865A716DB03D41D825F35A7D79C359667314EA45C` | — |
| `50w-2d.bdf` | `SOL 101` | 13,828,970 | 2025-12-10 15:52:14 | `64D2783811E4619147CDB4652FA3F095CCA86F6240567EE21408097578EE5E1D` | [[50w-2d-linear-elasticity-model]] |
| `50w-mix02d-allrbe2.bdf` | `SOL 101` | 11,324,509 | 2025-12-11 11:21:16 | `71922284E08DBFBE8B497A0818FD2EBF65416795B7C15CB66872311004D7BB3F` | — |
| `50w-mix23d.bdf` | `SOL 101` | 33,467,797 | 2025-12-11 11:29:20 | `2EB9EB864A7C9DF5935F0386DCF962C255889BEB5C82466DADAD5ADCDE5C1A9D` | — |
| `Cquad4_10W_SOL105.bdf` | `SOL 105` | 10,876,999 | 2025-09-01 17:17:12 | `00EA79D41FC5A13F0BCD89F9A86EFBE1809DD780F719BC0C3D7C578F539E1F56` | — |
| `Cquad4_16660elem_SOL105.bdf` | `SOL 105` | 1,831,149 | 2025-09-01 17:31:14 | `2578933B18250BC6DD5BC9F8116677C08E63156FFF1E6BC3C6DC5F8574C57165` | — |
| `Pshear_17w_cquad4_Pload2.bdf` | `SOL 101` | 70,377,934 | 2026-01-23 15:33:06 | `DF7C082FFD368A17FD5E26D512788CABE9735EA4D98F7AF4B4F3497554E76249` | — |
| `Pshell_17w_cquad4_Pload2.bdf` | `SOL 101` | 18,978,353 | 2026-01-23 14:38:46 | `6DC7110D738E0557C75BD6123F6A218A79C58D132AF233FAE4B0C838250E95A2` | — |
| `YUANTONG_10w_Cweld_SOL101.bdf` | `SOL 101` | 13,505,209 | 2025-12-09 16:38:40 | `87BAD5278E5CCC2C6077443C70E5D9F3C0EF31F59853A3DEA34857BB4CAFEF5D` | — |

「最后修改」取 iCloud 主档的时间戳；本地副本同一文件早 1–2 s，是复制时的时间戳取整，不构成版本差异。大小与 SHA-256 于 2026-09-03 在主档与本地副本上各算一次并一致（`Get-FileHash -Algorithm SHA256`）。

## 使用边界

- 新增算例页时先在本表确认文件已登记，再以 `DLUTFEM-20260720:testcases/<文件名>` 写入 `source`。
- 本表不解释模型内容；几何、材料、载荷与离散系统的复原只写在各算例页。
- 数据包内若追加文件，先补本表再引用；删除或替换文件视为新版本，不覆盖旧行。
