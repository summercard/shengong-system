#!/usr/bin/env python3
"""
神工系统 V3.1 - 项目初始化脚本
P0-3: 数据库初始化 + 配置生成 + 角色模板创建

功能:
1. 读取用户交互输入 {Logline}、{Genre_Rules}、{Core_Hook_Mechanic}
2. 生成基础 config/world_setting.yaml
3. 创建初始角色 YAML 模板 data/characters/{char_id}.yaml
4. 初始化 SQLite（创建所有表）
5. 提供简单交互（CLI）
"""

import yaml
import sqlite3
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional


class ProjectInitializer:
    """
    项目初始化器
    负责完成项目的完整初始化流程
    """
    
    def __init__(self, project_dir: str = "."):
        self.project_dir = project_dir
        self.config_dir = os.path.join(project_dir, "config")
        self.data_dir = os.path.join(project_dir, "data")
        self.characters_dir = os.path.join(project_dir, "data", "characters")
        self.db_path = os.path.join(project_dir, "data", "godcraft.db")
        self.config_path = os.path.join(project_dir, "config", "world_setting.yaml")
        
    def create_directories(self):
        """
        创建必要的目录结构
        """
        dirs = [
            self.config_dir,
            self.data_dir,
            self.characters_dir,
            os.path.join(self.project_dir, "prompts"),
            os.path.join(self.project_dir, "artifacts")
        ]
        
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
            print(f"✅ 目录创建: {dir_path}")
    
    def create_world_setting(
        self,
        logline: str,
        genre_rules: Dict,
        core_hook: str,
        auto_run: bool = False
    ) -> Dict:
        """
        生成 world_setting.yaml
        
        Args:
            logline: 一句话核心大纲
            genre_rules: 题材规则
            core_hook: 核心钩子机制
            auto_run: 是否启用自动运行
            
        Returns:
            Dict: 生成的配置
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        world_config = {
            "project_id": f"novel_{timestamp}",
            "created_at": datetime.now().isoformat(),
            
            "global_anchors": {
                "logline": logline,
                "genre": genre_rules.get("genre", ""),
                "power_system": genre_rules.get("power_system", "")
            },
            
            "absolute_rules": {
                "do_not_include": genre_rules.get("do_not_include", []),
                "mandatory_hooks": [core_hook]
            },
            
            "auto_run": {
                "enabled": auto_run,
                "max_chapters_per_run": 3,
                "pause_on_high_risk": True
            },
            
            "story_beats": {
                "hook": {"type": "fixed", "value": 1},
                "first_payoff": {"type": "range", "min": 2, "max": 4},
                "mini_climax": {"type": "range", "min": 8, "max": 12},
                "arc_climax": {"type": "range", "min": 25, "max": 35},
                "world_reveal": {"type": "range", "min": 80, "max": 120}
            }
        }
        
        # 保存配置
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(world_config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        print(f"✅ 世界观配置已生成: {self.config_path}")
        return world_config
    
    def create_character_template(
        self,
        char_id: str,
        name: str,
        archetype: str,
        core_motive: str,
        role: str = "主角"
    ) -> Dict:
        """
        创建角色 YAML 模板
        
        Args:
            char_id: 角色ID
            name: 角色姓名
            archetype: 原型定位
            core_motive: 核心驱动力
            role: 角色定位
            
        Returns:
            Dict: 角色配置
        """
        char_config = {
            "character_id": char_id,
            "created_at": datetime.now().isoformat(),
            
            "static_profile": {
                "name": name,
                "role": role,
                "archetype": archetype,
                "core_motive": core_motive
            },
            
            "dynamic_state": {
                "current_location": "待设定",
                "physical_health": "健康",
                "mental_state": "正常",
                "inventory": []
            }
        }
        
        # 保存角色配置
        char_path = os.path.join(self.characters_dir, f"{char_id}.yaml")
        with open(char_path, 'w', encoding='utf-8') as f:
            yaml.dump(char_config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        print(f"✅ 角色模板已创建: {char_path}")
        return char_config
    
    def init_database(self):
        """
        初始化 SQLite 数据库
        创建所有必要的表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 1. 事件日志表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chapter_id INTEGER,
                event_type TEXT,
                event_summary TEXT,
                involved_characters TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 2. 伏笔追踪表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS foreshadowing_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                clue_id TEXT UNIQUE,
                description TEXT,
                status TEXT DEFAULT 'active',
                created_chapter INTEGER,
                resolved_chapter INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 3. 世界关系图表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS world_graph_edges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_node TEXT,
                relation_type TEXT,
                target_node TEXT,
                relation_strength INTEGER DEFAULT 1,
                last_updated_chapter INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 4. 角色关系表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS character_relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                char_a TEXT,
                char_b TEXT,
                relation_type TEXT,
                trust_level INTEGER DEFAULT 0,
                hostility_level INTEGER DEFAULT 0,
                last_updated_chapter INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"✅ 数据库已初始化: {self.db_path}")
        print("   - events_log")
        print("   - foreshadowing_ledger")
        print("   - world_graph_edges")
        print("   - character_relationships")
    
    def run_interactive(self):
        """
        交互式初始化流程
        """
        print("=" * 60)
        print("🚀 神工系统 V3.1 - 项目初始化")
        print("=" * 60)
        print()
        
        # 1. 创建目录结构
        print("📁 创建目录结构...")
        self.create_directories()
        print()
        
        # 2. 收集用户输入
        print("📝 请输入世界观配置：\n")
        
        logline = input("📖 一句话大纲 (Logline): ").strip()
        if not logline:
            logline = "待填写：一句话核心大纲"
        
        genre = input("🎭 题材类型 (Genre): ").strip() or "奇幻"
        power_system = input("⚡ 力量体系 (可选): ").strip()
        
        # 禁用元素
        do_not_include = []
        print("\n🚫 禁用元素 (输入空行结束):")
        while True:
            item = input(f"  [{len(do_not_include) + 1}] ").strip()
            if not item:
                break
            do_not_include.append(item)
        
        # 核心钩子
        core_hook = input("\n🪝 核心钩子机制: ").strip() or "成长"
        
        # 自动运行
        auto_run_input = input("\n🔄 启用自动运行? (y/N): ").strip().lower()
        auto_run = auto_run_input == 'y'
        
        # 3. 生成世界观配置
        print("\n🌍 生成世界观配置...")
        genre_rules = {
            "genre": genre,
            "power_system": power_system,
            "do_not_include": do_not_include
        }
        world_config = self.create_world_setting(logline, genre_rules, core_hook, auto_run)
        
        # 4. 创建角色模板
        print("\n👤 创建角色模板...")
        
        # 主角
        print("\n[主角]")
        main_name = input("  姓名: ").strip() or "主角"
        main_archetype = input("  原型定位: ").strip() or "孤狼"
        main_motive = input("  核心驱动力: ").strip() or "复仇"
        self.create_character_template("char_main_01", main_name, main_archetype, main_motive, "主角")
        
        # 是否创建更多角色
        while True:
            create_more = input("\n是否创建其他角色? (y/N): ").strip().lower()
            if create_more != 'y':
                break
            
            char_id = input("  角色ID (如 char_support_01): ").strip()
            if not char_id:
                continue
            
            name = input("  姓名: ").strip()
            archetype = input("  原型定位: ").strip()
            motive = input("  核心驱动力: ").strip()
            role = input("  角色定位 (配角/反派/导师): ").strip() or "配角"
            
            self.create_character_template(char_id, name, archetype, motive, role)
        
        # 5. 初始化数据库
        print("\n💾 初始化数据库...")
        self.init_database()
        
        # 完成
        print("\n" + "=" * 60)
        print("✅ 项目初始化完成！")
        print("=" * 60)
        print(f"\n项目ID: {world_config['project_id']}")
        print(f"配置文件: {self.config_path}")
        print(f"数据库: {self.db_path}")
        print(f"角色目录: {self.characters_dir}")
        print()
    
    def run_demo(self):
        """
        演示模式初始化
        """
        print("=" * 60)
        print("🚀 神工系统 V3.1 - 项目初始化 (演示模式)")
        print("=" * 60)
        print()
        
        # 1. 创建目录结构
        print("📁 创建目录结构...")
        self.create_directories()
        print()
        
        # 2. 生成示例世界观配置
        print("🌍 生成世界观配置...")
        logline = "一个普通少年意外获得神秘传承，踏上修仙之路，在九天十地间书写传奇"
        genre_rules = {
            "genre": "仙侠",
            "power_system": "修仙体系：炼气-筑基-金丹-元婴-化神-渡劫-大乘",
            "do_not_include": ["现代科技", "西方魔法元素", "时间穿越"]
        }
        core_hook = "主角必须有成长性挫折"
        world_config = self.create_world_setting(logline, genre_rules, core_hook, auto_run=False)
        print()
        
        # 3. 创建角色模板
        print("👤 创建角色模板...")
        self.create_character_template("char_main_01", "林云", "孤狼", "寻找真相", "主角")
        self.create_character_template("char_mentor_01", "玄机子", "智者", "传承衣钵", "导师")
        self.create_character_template("char_antagonist_01", "血魔老祖", "野心家", "一统魔道", "反派")
        self.create_character_template("char_support_01", "苏晴", "圣母", "守护", "配角")
        print()
        
        # 4. 初始化数据库
        print("💾 初始化数据库...")
        self.init_database()
        print()
        
        # 完成
        print("=" * 60)
        print("✅ 演示项目初始化完成！")
        print("=" * 60)
        print(f"\n项目ID: {world_config['project_id']}")
        print(f"核心大纲: {logline}")
        print()


def main():
    """主入口"""
    initializer = ProjectInitializer()
    
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        initializer.run_demo()
    else:
        initializer.run_interactive()


if __name__ == "__main__":
    main()
