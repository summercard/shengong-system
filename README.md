# 神工系统 V3.1

基于 OpenClaw 的自动化连载闭环系统

## 项目简介

神工系统是一个基于 OpenClaw 平台的全自动记忆读写闭环系统，用于自动化生成连载小说内容。系统通过动态全局知识库（RAG）与角色档案持久化，从技术物理层面杜绝长篇连载最致命的"吃书"与"OOC"问题。

## 核心功能

- **自动化闭环**: 检索-生成-校验-更新记忆的完整流程
- **防吃书系统**: SQLite + Graph 结构化存储，避免设定冲突
- **角色档案持久化**: YAML 格式保存角色状态，防止 OOC
- **剧情节奏控制**: Beat Scheduler 自动安排情节高潮
- **多 Agent 协作**: Planner / Writer / Critic / LoreKeeper 四代理体系

## 项目结构

```
shengong_system/
├── orchestrator.py          # 核心调度器
├── config/
│   └── world_setting.yaml   # 世界观配置
├── data/
│   ├── characters/          # 角色档案
│   ├── world/               # 世界状态
│   └── godcraft.db          # SQLite 数据库
├── prompts/                 # Prompt 模板
├── artifacts/               # 输出产物
│   ├── stage_logs.json      # 阶段日志
│   └── acceptance_list.json # 验收列表
├── shengong_docs/           # 项目文档
└── requirements.txt         # Python 依赖
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化配置

```bash
python orchestrator.py
```

### 3. 配置世界观

编辑 `config/world_setting.yaml`，填写你的故事设定：

- `logline`: 一句话核心大纲
- `genre`: 题材类型
- `power_system`: 力量体系

## 开发进度

当前阶段: **P1-1 / Loop-1** - Orchestrator 框架搭建

查看详细任务列表: [STAGE_LIST.md](STAGE_LIST.md)

## 文档

- [项目文档](shengong_docs/神工系统%20V3.1.docx)
- [工程化实施指南](shengong_docs/神工系统%20V3.1%20功能说明.docx)
- [Loop 模板](shengong_docs/loop-templates-openclaw.docx)
- [开发日志](PROJECT_LOG.md)

## Git 仓库

https://github.com/summercard/shengong-system

## 许可证

私有项目 - 保留所有权利
