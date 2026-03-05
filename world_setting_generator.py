"""
神工系统 V3.1 - 世界观配置生成器
根据 Logline 和 Genre_Rules 生成 world_setting.yaml
"""

import yaml
import os
from typing import Dict, List, Optional
from datetime import datetime


class WorldSettingGenerator:
    """
    世界观配置生成器
    根据用户输入的 Logline 和 Genre_Rules 生成完整的配置文件
    """
    
    def __init__(self, output_path: str = "config/world_setting.yaml"):
        self.output_path = output_path
        self.world_config = {}
    
    def generate(
        self,
        logline: str,
        genre: str,
        power_system: Optional[str] = None,
        do_not_include: Optional[List[str]] = None,
        mandatory_hooks: Optional[List[str]] = None,
        project_name: str = "未命名项目",
        auto_run_enabled: bool = False,
        max_chapters_per_run: int = 3
    ) -> Dict:
        """
        生成世界观配置
        
        Args:
            logline: 一句话核心大纲
            genre: 题材类型
            power_system: 力量体系（可选）
            do_not_include: 禁用元素列表（可选）
            mandatory_hooks: 必须包含的钩子（可选）
            project_name: 项目名称
            auto_run_enabled: 是否启用自动运行
            max_chapters_per_run: 单次最大生成章节数
            
        Returns:
            Dict: 生成的配置字典
        """
        # 生成项目ID
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        project_id = f"novel_{timestamp}"
        
        # 构建配置
        self.world_config = {
            "project_id": project_id,
            "project_name": project_name,
            "created_at": datetime.now().isoformat(),
            
            # 全局锚点
            "global_anchors": {
                "logline": logline,
                "genre": genre,
                "power_system": power_system or "无"
            },
            
            # 绝对规则
            "absolute_rules": {
                "do_not_include": do_not_include or [],
                "mandatory_hooks": mandatory_hooks or []
            },
            
            # 自动运行配置
            "auto_run": {
                "enabled": auto_run_enabled,
                "max_chapters_per_run": max_chapters_per_run,
                "pause_on_high_risk": True
            },
            
            # 故事节奏配置（Beat Scheduler）
            "story_beats": {
                "hook": {"type": "fixed", "value": 1},
                "first_payoff": {"type": "range", "min": 2, "max": 4},
                "mini_climax": {"type": "range", "min": 8, "max": 12},
                "arc_climax": {"type": "range", "min": 25, "max": 35},
                "world_reveal": {"type": "range", "min": 80, "max": 120}
            }
        }
        
        return self.world_config
    
    def save(self) -> bool:
        """
        保存配置到 YAML 文件
        
        Returns:
            bool: 保存成功返回 True
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            
            # 写入文件
            with open(self.output_path, 'w', encoding='utf-8') as f:
                yaml.dump(
                    self.world_config,
                    f,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False
                )
            
            print(f"✅ 世界观配置已保存: {self.output_path}")
            return True
            
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False
    
    def load(self) -> Optional[Dict]:
        """
        从文件加载配置
        
        Returns:
            Dict: 配置字典，失败返回 None
        """
        try:
            if not os.path.exists(self.output_path):
                return None
            
            with open(self.output_path, 'r', encoding='utf-8') as f:
                self.world_config = yaml.safe_load(f)
            
            return self.world_config
            
        except Exception as e:
            print(f"❌ 加载失败: {e}")
            return None


def interactive_generate():
    """
    交互式生成世界观配置
    """
    print("=" * 60)
    print("🌍 神工系统 - 世界观配置生成器")
    print("=" * 60)
    print()
    
    # 收集用户输入
    print("请输入世界观配置信息：\n")
    
    project_name = input("📝 项目名称: ").strip() or "未命名项目"
    print()
    
    logline = input("📖 一句话大纲 (Logline): ").strip()
    if not logline:
        print("⚠️  警告: Logline 是必填项，使用默认值")
        logline = "待填写：一句话核心大纲"
    print()
    
    genre = input("🎭 题材类型 (Genre): ").strip() or "奇幻"
    print()
    
    power_system = input("⚡ 力量体系 (可选，如：修仙/魔法/异能): ").strip() or None
    print()
    
    # 禁用元素
    do_not_include = []
    print("🚫 禁用元素 (输入空行结束):")
    while True:
        item = input(f"  [{len(do_not_include) + 1}] ").strip()
        if not item:
            break
        do_not_include.append(item)
    print()
    
    # 必须包含的钩子
    mandatory_hooks = []
    print("🪝 必须包含的钩子 (输入空行结束):")
    while True:
        item = input(f"  [{len(mandatory_hooks) + 1}] ").strip()
        if not item:
            break
        mandatory_hooks.append(item)
    print()
    
    # 自动运行配置
    auto_run_input = input("🔄 启用自动运行? (y/N): ").strip().lower()
    auto_run_enabled = auto_run_input == 'y'
    print()
    
    max_chapters = 3
    if auto_run_enabled:
        max_chapters_input = input("📊 单次最大生成章节数 (默认3): ").strip()
        if max_chapters_input.isdigit():
            max_chapters = int(max_chapters_input)
    print()
    
    # 生成配置
    print("⏳ 正在生成配置...\n")
    
    generator = WorldSettingGenerator()
    config = generator.generate(
        logline=logline,
        genre=genre,
        power_system=power_system,
        do_not_include=do_not_include,
        mandatory_hooks=mandatory_hooks,
        project_name=project_name,
        auto_run_enabled=auto_run_enabled,
        max_chapters_per_run=max_chapters
    )
    
    # 保存配置
    if generator.save():
        print("\n" + "=" * 60)
        print("✅ 世界观配置生成完成！")
        print("=" * 60)
        print(f"\n项目ID: {config['project_id']}")
        print(f"项目名称: {config['project_name']}")
        print(f"核心大纲: {config['global_anchors']['logline']}")
        print(f"题材类型: {config['global_anchors']['genre']}")
        print(f"\n配置文件: {generator.output_path}")
        return config
    else:
        print("\n❌ 配置生成失败")
        return None


def demo_generate():
    """
    演示模式：生成示例配置
    """
    print("=" * 60)
    print("🌍 神工系统 - 世界观配置生成器 (演示模式)")
    print("=" * 60)
    print()
    
    generator = WorldSettingGenerator()
    
    # 使用示例数据
    config = generator.generate(
        logline="一个普通少年意外获得神秘传承，踏上修仙之路，在九天十地间书写传奇",
        genre="仙侠",
        power_system="修仙体系：炼气-筑基-金丹-元婴-化神-渡劫-大乘",
        do_not_include=[
            "现代科技",
            "西方魔法元素",
            "时间穿越"
        ],
        mandatory_hooks=[
            "主角必须有成长性挫折",
            "每卷必须有势力冲突"
        ],
        project_name="九天仙途",
        auto_run_enabled=False,
        max_chapters_per_run=3
    )
    
    # 保存配置
    if generator.save():
        print("\n✅ 演示配置生成完成！")
        print(f"配置文件: {generator.output_path}\n")
        
        # 显示配置内容
        print("配置预览:")
        print("-" * 60)
        print(yaml.dump(config, allow_unicode=True, default_flow_style=False, sort_keys=False))
        
        return config
    else:
        print("\n❌ 配置生成失败")
        return None


if __name__ == "__main__":
    import sys
    
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # 演示模式
        demo_generate()
    else:
        # 交互模式
        interactive_generate()
