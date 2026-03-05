"""
神工系统 V3.1 - Orchestrator 核心调度器
负责协调整个自动化连载闭环的执行流程
"""

import yaml
import sqlite3
import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AutoRunConfig:
    """自动运行限制配置"""
    
    def __init__(self, enabled: bool = False, max_chapters: int = 3, pause_on_risk: bool = True):
        self.enabled = enabled
        self.max_chapters_per_run = max_chapters
        self.pause_on_high_risk = pause_on_risk
    
    @classmethod
    def from_dict(cls, config_dict: Dict) -> 'AutoRunConfig':
        """从字典创建配置对象"""
        return cls(
            enabled=config_dict.get('enabled', False),
            max_chapters=config_dict.get('max_chapters_per_run', 3),
            pause_on_risk=config_dict.get('pause_on_high_risk', True)
        )
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'enabled': self.enabled,
            'max_chapters_per_run': self.max_chapters_per_run,
            'pause_on_high_risk': self.pause_on_high_risk
        }


class Orchestrator:
    """
    神工系统核心调度器
    负责协调整个自动化连载闭环的执行流程
    """
    
    def __init__(self, config_path: str = "config/world_setting.yaml"):
        """
        初始化 Orchestrator
        
        Args:
            config_path: 世界观配置文件路径
        """
        self.config_path = config_path
        self.world_config = {}
        self.auto_run_config = AutoRunConfig()
        self.db_path = "data/godcraft.db"
        self.chapters_generated = 0
        self.current_chapter = 0
        
        # Agent 引用（后续会注入具体实现）
        self.writer_agent = None
        self.critic_agent = None
        self.planner_agent = None
        self.lorekeeper_agent = None
        
        logger.info("Orchestrator 初始化中...")
        
    def load_config(self) -> bool:
        """
        读取 YAML 配置文件
        
        Returns:
            bool: 加载成功返回 True，否则返回 False
        """
        try:
            if not os.path.exists(self.config_path):
                logger.warning(f"配置文件不存在: {self.config_path}")
                return False
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.world_config = yaml.safe_load(f)
            
            # 加载自动运行配置
            if 'auto_run' in self.world_config:
                self.auto_run_config = AutoRunConfig.from_dict(self.world_config['auto_run'])
                logger.info(f"自动运行配置加载成功: {self.auto_run_config.to_dict()}")
            
            logger.info(f"配置加载成功: {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"配置加载失败: {e}")
            return False
    
    def init_database(self) -> bool:
        """
        初始化数据库
        
        Returns:
            bool: 初始化成功返回 True
        """
        try:
            # 确保数据目录存在
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 创建事件日志表
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
            
            # 创建伏笔追踪表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS foreshadowing_ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    clue_id TEXT UNIQUE,
                    description TEXT,
                    status TEXT DEFAULT 'active',
                    created_chapter INTEGER,
                    resolved_chapter INTEGER
                )
            ''')
            
            # 创建世界关系图表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS world_graph_edges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_node TEXT,
                    relation_type TEXT,
                    target_node TEXT,
                    relation_strength INTEGER DEFAULT 1,
                    last_updated_chapter INTEGER
                )
            ''')
            
            # 创建角色关系表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS character_relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    char_a TEXT,
                    char_b TEXT,
                    relation_type TEXT,
                    trust_level INTEGER DEFAULT 0,
                    hostility_level INTEGER DEFAULT 0,
                    last_updated_chapter INTEGER
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info(f"数据库初始化成功: {self.db_path}")
            return True
            
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            return False
    
    def load_character_state(self, char_id: str) -> Optional[Dict]:
        """
        读取角色状态 YAML
        
        Args:
            char_id: 角色ID
            
        Returns:
            Dict: 角色状态数据，失败返回 None
        """
        char_path = f"data/characters/{char_id}.yaml"
        try:
            if not os.path.exists(char_path):
                logger.warning(f"角色文件不存在: {char_path}")
                return None
            
            with open(char_path, 'r', encoding='utf-8') as f:
                char_data = yaml.safe_load(f)
            
            logger.info(f"角色状态加载成功: {char_id}")
            return char_data
            
        except Exception as e:
            logger.error(f"角色状态加载失败 {char_id}: {e}")
            return None
    
    def update_character_state(self, char_id: str, updates: Dict) -> bool:
        """
        更新角色状态（原子写入）
        
        Args:
            char_id: 角色ID
            updates: 要更新的字段
            
        Returns:
            bool: 更新成功返回 True
        """
        char_path = f"data/characters/{char_id}.yaml"
        try:
            # 读取现有数据
            char_data = self.load_character_state(char_id)
            if char_data is None:
                char_data = {
                    'character_id': char_id,
                    'static_profile': {},
                    'dynamic_state': {}
                }
            
            # 更新动态状态
            if 'dynamic_state' not in char_data:
                char_data['dynamic_state'] = {}
            
            char_data['dynamic_state'].update(updates)
            
            # 原子写入
            import tempfile
            import shutil
            
            dir_name = os.path.dirname(char_path)
            fd, tmp_path = tempfile.mkstemp(dir=dir_name, prefix='.tmp_')
            os.close(fd)
            
            with open(tmp_path, 'w', encoding='utf-8') as f:
                yaml.dump(char_data, f, allow_unicode=True, default_flow_style=False)
            
            shutil.move(tmp_path, char_path)
            
            logger.info(f"角色状态更新成功: {char_id}")
            return True
            
        except Exception as e:
            logger.error(f"角色状态更新失败 {char_id}: {e}")
            return False
    
    def can_generate_more(self) -> bool:
        """
        检查是否可以继续生成章节
        
        Returns:
            bool: 可以继续生成返回 True
        """
        if not self.auto_run_config.enabled:
            logger.info("自动运行未启用，需要人工确认")
            return False
        
        if self.chapters_generated >= self.auto_run_config.max_chapters_per_run:
            logger.info(f"已达到最大生成数量限制: {self.auto_run_config.max_chapters_per_run}")
            return False
        
        return True
    
    def generate_chapter(self, chapter_num: int, outline: str) -> Dict[str, Any]:
        """
        生成章节（主流程）
        
        Args:
            chapter_num: 章节号
            outline: 章节大纲
            
        Returns:
            Dict: 生成结果
        """
        logger.info(f"开始生成第 {chapter_num} 章")
        
        # 检查是否可以继续生成
        if not self.can_generate_more():
            return {
                'status': 'BLOCKED',
                'reason': 'auto_run_limit_reached',
                'message': f'已达到最大生成数量限制 ({self.auto_run_config.max_chapters_per_run} 章)'
            }
        
        # TODO: 实现完整的生成流程
        # 1. Planner 生成本章结构
        # 2. Writer 生成初稿
        # 3. Critic 审查
        # 4. LoreKeeper 更新状态
        
        result = {
            'status': 'SUCCESS',
            'chapter_num': chapter_num,
            'outline': outline,
            'content': '',  # 待实现
            'metrics': {
                'tokens_used': 0,
                'generation_time': 0
            }
        }
        
        self.chapters_generated += 1
        self.current_chapter = chapter_num
        
        logger.info(f"第 {chapter_num} 章生成完成")
        return result
    
    def run_pipeline(self, max_chapters: int = None) -> Dict[str, Any]:
        """
        运行完整的生成管道
        
        Args:
            max_chapters: 最大生成章节数（可选，覆盖配置）
            
        Returns:
            Dict: 执行结果
        """
        logger.info("开始运行生成管道")
        
        # 加载配置
        if not self.load_config():
            return {
                'status': 'ERROR',
                'message': '配置加载失败'
            }
        
        # 初始化数据库
        if not self.init_database():
            return {
                'status': 'ERROR',
                'message': '数据库初始化失败'
            }
        
        # 确定最大章节数
        if max_chapters is not None:
            effective_max = min(max_chapters, self.auto_run_config.max_chapters_per_run)
        else:
            effective_max = self.auto_run_config.max_chapters_per_run
        
        logger.info(f"计划生成 {effective_max} 章")
        
        # TODO: 实现完整的管道逻辑
        results = {
            'status': 'SUCCESS',
            'chapters_generated': 0,
            'chapters': []
        }
        
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取当前状态
        
        Returns:
            Dict: 状态信息
        """
        return {
            'current_chapter': self.current_chapter,
            'chapters_generated': self.chapters_generated,
            'auto_run_enabled': self.auto_run_config.enabled,
            'max_chapters_per_run': self.auto_run_config.max_chapters_per_run,
            'can_generate_more': self.can_generate_more(),
            'config_loaded': bool(self.world_config)
        }


# 测试代码
if __name__ == "__main__":
    # 创建 Orchestrator 实例
    orchestrator = Orchestrator()
    
    # 初始化
    print("=" * 50)
    print("神工系统 Orchestrator 测试")
    print("=" * 50)
    
    # 加载配置（会创建默认配置）
    orchestrator.load_config()
    
    # 初始化数据库
    orchestrator.init_database()
    
    # 获取状态
    status = orchestrator.get_status()
    print("\n当前状态:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # 测试生成限制
    print("\n测试自动生成限制:")
    print(f"  是否可以生成: {orchestrator.can_generate_more()}")
    
    print("\n✅ Orchestrator 基础功能测试完成")
