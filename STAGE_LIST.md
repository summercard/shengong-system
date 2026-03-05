# 神工系统项目工程阶段列表

## 阶段总览

| 阶段ID | 阶段名称 | Loop-1 | Loop-2 | Loop-3 | 状态 | 负责人 |
|--------|---------|--------|--------|--------|------|--------|
| **P0** | 项目初始化 | - | - | - | DONE | OpenClaw |
| **P1** | 核心管道开发 | - | - | - | PENDING | - |
| **P2** | 记忆与状态管理 | - | - | - | PENDING | - |
| **P3** | 规划与节奏细化 | - | - | - | PENDING | - |
| **P4** | 前端与监控细化 | - | - | - | PENDING | - |
| **P5** | 调试优化与测试 | - | - | - | PENDING | - |
| **P6** | 打包发布 | - | - | - | PENDING | - |

---

## 详细任务列表

### P0 - 项目初始化

| 任务ID | 任务名称 | Loop | 状态 | 开始时间 | 完成时间 |
|--------|---------|------|------|---------|---------|
| P0-1 | 世界观配置生成 | Loop-1 | **DONE** | 2026-03-05 15:21 | 2026-03-05 15:21 |
| P0-1 | 世界观配置生成 | Loop-2 | **READY** | - | - |
| P0-1 | 世界观配置生成 | Loop-3 | PENDING | - | - |
| P0-2 | 角色模板创建 | Loop-1 | **DONE** | 2026-03-05 15:22 | 2026-03-05 15:22 |
| P0-2 | 角色模板创建 | Loop-2 | PENDING | - | - |
| P0-2 | 角色模板创建 | Loop-3 | PENDING | - | - |
| P0-3 | 数据库初始化脚本 | Loop-1 | **DONE** | 2026-03-05 15:24 | 2026-03-05 15:24 |
| P0-3 | 数据库初始化脚本 | Loop-2 | PENDING | - | - |
| P0-3 | 数据库初始化脚本 | Loop-3 | PENDING | - | - |

**P0-1 验收项**:
- [x] 实现交互式输入（Logline、Genre_Rules）
- [x] 根据输入生成 world_setting.yaml
- [x] 包含故事大纲、题材标签、禁用元素等

**P0-2 验收项**:
- [x] 创建主角 YAML 模板
- [x] 创建配角 YAML 模板
- [x] 包含 static_profile 和 dynamic_state

**P0-3 验收项**:
- [x] 独立的 init_project.py 脚本
- [x] 创建所有数据库表
- [x] 支持命令行运行

---

### P1 - 核心管道开发

| 任务ID | 任务名称 | Loop | 状态 | 开始时间 | 完成时间 |
|--------|---------|------|------|---------|---------|
| P1-1 | Orchestrator 框架搭建 | Loop-1 | **DONE** | 2026-03-05 15:13 | 2026-03-05 15:13 |
| P1-1 | Orchestrator 框架搭建 | Loop-2 | **READY** | - | - |
| P1-1 | Orchestrator 框架搭建 | Loop-3 | PENDING | - | - |
| P1-2 | Writer Agent 实现 | Loop-1 | PENDING | - | - |
| P1-2 | Writer Agent 实现 | Loop-2 | PENDING | - | - |
| P1-2 | Writer Agent 实现 | Loop-3 | PENDING | - | - |
| P1-3 | Critic Agent 实现 | Loop-1 | PENDING | - | - |
| P1-3 | Critic Agent 实现 | Loop-2 | PENDING | - | - |
| P1-3 | Critic Agent 实现 | Loop-3 | PENDING | - | - |
| P1-4 | 小规模验证 | Loop-1 | PENDING | - | - |
| P1-4 | 小规模验证 | Loop-2 | PENDING | - | - |
| P1-4 | 小规模验证 | Loop-3 | PENDING | - | - |

**P1-1 验收项**:
- [ ] Orchestrator 类骨架完成
- [ ] 支持读取 YAML 配置
- [ ] 支持调用 Writer 和 Critic Agent
- [ ] 实现自动运行限制配置 (max_chapters_per_run)

---

### P2 - 记忆与状态管理

| 任务ID | 任务名称 | Loop | 状态 | 开始时间 | 完成时间 |
|--------|---------|------|------|---------|---------|
| P2-1 | 角色状态读写 | Loop-1 | PENDING | - | - |
| P2-1 | 角色状态读写 | Loop-2 | PENDING | - | - |
| P2-1 | 角色状态读写 | Loop-3 | PENDING | - | - |
| P2-2 | 事件日志管理 | Loop-1 | PENDING | - | - |
| P2-2 | 事件日志管理 | Loop-2 | PENDING | - | - |
| P2-2 | 事件日志管理 | Loop-3 | PENDING | - | - |
| P2-3 | 世界与关系图更新 | Loop-1 | PENDING | - | - |
| P2-3 | 世界与关系图更新 | Loop-2 | PENDING | - | - |
| P2-3 | 世界与关系图更新 | Loop-3 | PENDING | - | - |
| P2-4 | 伏笔跟踪表 | Loop-1 | PENDING | - | - |
| P2-4 | 伏笔跟踪表 | Loop-2 | PENDING | - | - |
| P2-4 | 伏笔跟踪表 | Loop-3 | PENDING | - | - |

---

### P3 - 规划与节奏细化

| 任务ID | 任务名称 | Loop | 状态 | 开始时间 | 完成时间 |
|--------|---------|------|------|---------|---------|
| P3-1 | Beat Scheduler 配置 | Loop-1 | PENDING | - | - |
| P3-1 | Beat Scheduler 配置 | Loop-2 | PENDING | - | - |
| P3-1 | Beat Scheduler 配置 | Loop-3 | PENDING | - | - |
| P3-2 | Planner Agent 细分 | Loop-1 | PENDING | - | - |
| P3-2 | Planner Agent 细分 | Loop-2 | PENDING | - | - |
| P3-2 | Planner Agent 细分 | Loop-3 | PENDING | - | - |
| P3-3 | 伏笔引用 | Loop-1 | PENDING | - | - |
| P3-3 | 伏笔引用 | Loop-2 | PENDING | - | - |
| P3-3 | 伏笔引用 | Loop-3 | PENDING | - | - |

---

### P4 - 前端与监控细化

| 任务ID | 任务名称 | Loop | 状态 | 开始时间 | 完成时间 |
|--------|---------|------|------|---------|---------|
| P4-1 | 剧本编辑界面 | Loop-1 | PENDING | - | - |
| P4-1 | 剧本编辑界面 | Loop-2 | PENDING | - | - |
| P4-1 | 剧本编辑界面 | Loop-3 | PENDING | - | - |
| P4-2 | 角色状态监控界面 | Loop-1 | PENDING | - | - |
| P4-2 | 角色状态监控界面 | Loop-2 | PENDING | - | - |
| P4-2 | 角色状态监控界面 | Loop-3 | PENDING | - | - |
| P4-3 | 生成监控面板 | Loop-1 | PENDING | - | - |
| P4-3 | 生成监控面板 | Loop-2 | PENDING | - | - |
| P4-3 | 生成监控面板 | Loop-3 | PENDING | - | - |
| P4-4 | 并行触发控制 | Loop-1 | PENDING | - | - |
| P4-4 | 并行触发控制 | Loop-2 | PENDING | - | - |
| P4-4 | 并行触发控制 | Loop-3 | PENDING | - | - |

---

### P5 - 调试优化与测试

| 任务ID | 任务名称 | Loop | 状态 | 开始时间 | 完成时间 |
|--------|---------|------|------|---------|---------|
| P5-1 | 单元测试编写 | Loop-1 | PENDING | - | - |
| P5-1 | 单元测试编写 | Loop-2 | PENDING | - | - |
| P5-1 | 单元测试编写 | Loop-3 | PENDING | - | - |
| P5-2 | 大模型效率 | Loop-1 | PENDING | - | - |
| P5-2 | 大模型效率 | Loop-2 | PENDING | - | - |
| P5-2 | 大模型效率 | Loop-3 | PENDING | - | - |
| P5-3 | 压力测试 | Loop-1 | PENDING | - | - |
| P5-3 | 压力测试 | Loop-2 | PENDING | - | - |
| P5-3 | 压力测试 | Loop-3 | PENDING | - | - |

---

### P6 - 打包发布

| 任务ID | 任务名称 | Loop | 状态 | 开始时间 | 完成时间 |
|--------|---------|------|------|---------|---------|
| P6-1 | 安装脚本完善 | Loop-1 | PENDING | - | - |
| P6-1 | 安装脚本完善 | Loop-2 | PENDING | - | - |
| P6-1 | 安装脚本完善 | Loop-3 | PENDING | - | - |
| P6-2 | 发布版本管理 | Loop-1 | PENDING | - | - |
| P6-2 | 发布版本管理 | Loop-2 | PENDING | - | - |
| P6-2 | 发布版本管理 | Loop-3 | PENDING | - | - |

---

## 当前待执行任务

**🎯 下一个任务**: **P1-1 / Loop-1 - Orchestrator 框架搭建**

**任务描述**: 实现 Orchestrator 类骨架，包括读取输入、组织上下文、调用各 Agent。

**验收标准**:
- Orchestrator 类骨架完成
- 支持读取 YAML 配置
- 支持调用 Writer 和 Critic Agent
- 实现自动运行限制配置

**上游依赖**: 无 (P0已完成)

---
