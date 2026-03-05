"""
神工系统 V3.1 - 角色模板生成器
创建角色 YAML 模板文件
"""

import yaml
import os
from typing import Dict, List, Optional
from datetime import datetime


class CharacterTemplateGenerator:
    """
    角色模板生成器
    生成角色的 static_profile 和 dynamic_state
    """
    
    def __init__(self, output_dir: str = "data/characters"):
        self.output_dir = output_dir
    
    def generate(
        self,
        char_id: str,
        name: str,
        archetype: str,
        core_motive: str,
        role: str = "配角",
        current_location: str = "未知",
        physical_health: str = "健康",
        mental_state: str = "正常",
        inventory: Optional[List[str]] = None
    ) -> Dict:
        """
        生成角色 YAML 模板
        
        Args:
            char_id: 角色ID（如 char_main_01）
            name: 角色姓名
            archetype: 原型定位（如孤狼、圣母、狂战士）
            core_motive: 核心驱动力（如复仇、生存、长生）
            role: 角色定位（主角/配角/反派）
            current_location: 当前位置
            physical_health: 生理状态
            mental_state: 心理状态
            inventory: 初始物品列表
            
        Returns:
            Dict: 角色配置字典
        """
        character = {
            "character_id": char_id,
            "created_at": datetime.now().isoformat(),
            
            # 静态档案（不会自动更新）
            "static_profile": {
                "name": name,
                "role": role,
                "archetype": archetype,
                "core_motive": core_motive
            },
            
            # 动态状态（每章结束后自动更新）
            "dynamic_state": {
                "current_location": current_location,
                "physical_health": physical_health,
                "mental_state": mental_state,
                "inventory": inventory or []
            }
        }
        
        return character
    
    def save(self, char_id: str, character: Dict) -> bool:
        """
        保存角色配置到 YAML 文件
        
        Args:
            char_id: 角色ID
            character: 角色配置字典
            
        Returns:
            bool: 保存成功返回 True
        """
        try:
            # 确保目录存在
            os.makedirs(self.output_dir, exist_ok=True)
            
            # 文件路径
            file_path = os.path.join(self.output_dir, f"{char_id}.yaml")
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(
                    character,
                    f,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False
                )
            
            print(f"✅ 角色配置已保存: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False
    
    def create_main_character(
        self,
        name: str = "主角",
        archetype: str = "孤狼",
        core_motive: str = "复仇"
    ) -> Dict:
        """
        创建主角模板
        
        Args:
            name: 角色姓名
            archetype: 原型定位
            core_motive: 核心驱动力
            
        Returns:
            Dict: 主角配置
        """
        return self.generate(
            char_id="char_main_01",
            name=name,
            archetype=archetype,
            core_motive=core_motive,
            role="主角",
            current_location="初始村庄",
            physical_health="健康",
            mental_state="坚定",
            inventory=["破旧的衣服", "祖传玉佩"]
        )
    
    def create_mentor(
        self,
        name: str = "导师",
        archetype: str = "智者",
        core_motive: str = "传承"
    ) -> Dict:
        """
        创建导师角色模板
        
        Args:
            name: 角色姓名
            archetype: 原型定位
            core_motive: 核心驱动力
            
        Returns:
            Dict: 导师配置
        """
        return self.generate(
            char_id="char_mentor_01",
            name=name,
            archetype=archetype,
            core_motive=core_motive,
            role="导师",
            current_location="隐世洞府",
            physical_health="虚弱",
            mental_state="平静",
            inventory=["古老典籍", "灵丹若干"]
        )
    
    def create_antagonist(
        self,
        name: str = "反派",
        archetype: str = "野心家",
        core_motive: str = "统治"
    ) -> Dict:
        """
        创建反派角色模板
        
        Args:
            name: 角色姓名
            archetype: 原型定位
            core_motive: 核心驱动力
            
        Returns:
            Dict: 反派配置
        """
        return self.generate(
            char_id="char_antagonist_01",
            name=name,
            archetype=archetype,
            core_motive=core_motive,
            role="反派",
            current_location="魔宗总坛",
            physical_health="巅峰",
            mental_state="狂傲",
            inventory=["魔器", "护法令牌"]
        )


def demo_generate():
    """
    演示模式：生成示例角色模板
    """
    print("=" * 60)
    print("👤 神工系统 - 角色模板生成器 (演示模式)")
    print("=" * 60)
    print()
    
    generator = CharacterTemplateGenerator()
    
    # 1. 创建主角
    print("1️⃣  创建主角...")
    main_char = generator.create_main_character(
        name="林云",
        archetype="孤狼",
        core_motive="寻找真相"
    )
    generator.save("char_main_01", main_char)
    print()
    
    # 2. 创建导师
    print("2️⃣  创建导师...")
    mentor = generator.create_mentor(
        name="玄机子",
        archetype="智者",
        core_motive="传承衣钵"
    )
    generator.save("char_mentor_01", mentor)
    print()
    
    # 3. 创建反派
    print("3️⃣  创建反派...")
    antagonist = generator.create_antagonist(
        name="血魔老祖",
        archetype="野心家",
        core_motive="一统魔道"
    )
    generator.save("char_antagonist_01", antagonist)
    print()
    
    # 4. 创建配角
    print("4️⃣  创建配角...")
    support_char = generator.generate(
        char_id="char_support_01",
        name="苏晴",
        archetype="圣母",
        core_motive="守护",
        role="配角",
        current_location="青云宗",
        physical_health="健康",
        mental_state="担忧",
        inventory=["疗伤丹药", "宗门令牌"]
    )
    generator.save("char_support_01", support_char)
    print()
    
    print("=" * 60)
    print("✅ 角色模板生成完成！")
    print("=" * 60)
    print()
    
    # 显示主角配置示例
    print("主角配置示例:")
    print("-" * 60)
    print(yaml.dump(main_char, allow_unicode=True, default_flow_style=False, sort_keys=False))
    
    return [main_char, mentor, antagonist, support_char]


def interactive_generate():
    """
    交互式生成角色模板
    """
    print("=" * 60)
    print("👤 神工系统 - 角色模板生成器")
    print("=" * 60)
    print()
    
    generator = CharacterTemplateGenerator()
    
    while True:
        print("\n请输入角色信息：\n")
        
        char_id = input("🆔 角色ID (如 char_main_01): ").strip()
        if not char_id:
            print("❌ 角色ID 是必填项")
            continue
        
        name = input("📝 角色姓名: ").strip()
        if not name:
            print("❌ 角色姓名是必填项")
            continue
        
        role = input("🎭 角色定位 (主角/配角/反派/导师): ").strip() or "配角"
        archetype = input("🏛️  原型定位 (如孤狼/圣母/智者): ").strip() or "普通人"
        core_motive = input("💪 核心驱动力 (如复仇/生存/传承): ").strip() or "生存"
        
        # 生成角色
        character = generator.generate(
            char_id=char_id,
            name=name,
            archetype=archetype,
            core_motive=core_motive,
            role=role
        )
        
        # 保存
        if generator.save(char_id, character):
            print(f"\n✅ 角色 '{name}' 创建成功！")
        
        # 是否继续
        continue_input = input("\n是否继续创建其他角色? (y/N): ").strip().lower()
        if continue_input != 'y':
            break
    
    print("\n✅ 角色创建完成！")


if __name__ == "__main__":
    import sys
    
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # 演示模式
        demo_generate()
    else:
        # 交互模式
        interactive_generate()
