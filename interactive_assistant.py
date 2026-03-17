#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式智能助手 - 支持自定义问题输入
支持：天气查询、交通路线、信息查询等功能
"""

import os
import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from openai import AsyncOpenAI
import getpass

class InteractiveAssistant:
    def __init__(self):
        self.client = None
        self.setup_api()
        self.setup_tools()
    
    def setup_api(self):
        """安全设置API密钥"""
        print("=== 交互式智能助手初始化 ===")
        
        # 安全输入API密钥
        api_key = getpass.getpass("请输入你的阿里云百炼API密钥: ")
        
        # 设置环境变量
        os.environ["DASHSCOPE_API_KEY"] = api_key
        os.environ["OPENAI_API_KEY"] = "placeholder"  # 绕过检查
        
        # 初始化客户端
        self.client = AsyncOpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        
        print("✅ API客户端初始化成功")
    
    def setup_tools(self):
        """定义工具函数和映射"""
        
        # 工具函数定义
        self.tool_functions = {
            "get_weather": self.get_weather,
            "get_travel_route": self.get_travel_route,
            "get_university_info": self.get_university_info,
            "get_current_time": self.get_current_time,
            "calculate_distance": self.calculate_distance,
            "search_web": self.search_web
        }
        
        # 工具描述（给大模型使用）
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "获取指定城市的天气预报",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "城市名称，例如：沈阳、北京"
                            },
                            "days": {
                                "type": "integer",
                                "description": "预报天数，默认1天",
                                "default": 1
                            }
                        },
                        "required": ["city"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_travel_route",
                    "description": "获取两地之间的交通路线和建议",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "from_city": {
                                "type": "string",
                                "description": "出发城市"
                            },
                            "to_city": {
                                "type": "string",
                                "description": "目的地城市"
                            },
                            "preference": {
                                "type": "string",
                                "description": "偏好：fastest(最快)/cheapest(最便宜)/balanced(平衡)",
                                "default": "balanced"
                            }
                        },
                        "required": ["from_city", "to_city"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_university_info",
                    "description": "获取大学的基本信息和位置",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "university_name": {
                                "type": "string",
                                "description": "大学名称"
                            }
                        },
                        "required": ["university_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_current_time",
                    "description": "获取当前时间",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate_distance",
                    "description": "计算两个城市之间的距离",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city1": {
                                "type": "string",
                                "description": "第一个城市"
                            },
                            "city2": {
                                "type": "string",
                                "description": "第二个城市"
                            }
                        },
                        "required": ["city1", "city2"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "搜索网络信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "搜索关键词"
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        ]
    
    # === 工具函数实现 ===
    
    async def get_weather(self, city: str, days: int = 1) -> str:
        """获取天气预报（模拟数据）"""
        weather_conditions = ["晴", "多云", "阴", "小雨", "中雨", "大雨", "雪"]
        temperatures = {
            "沈阳": {"min": -10, "max": 5},
            "北京": {"min": -5, "max": 10},
            "上海": {"min": 5, "max": 15}
        }
        
        if city not in temperatures:
            temperatures[city] = {"min": 0, "max": 10}
        
        result = []
        for i in range(days):
            date = (datetime.now() + timedelta(days=i)).strftime("%m月%d日")
            weather = random.choice(weather_conditions)
            temp_range = temperatures[city]
            temp = f"{temp_range['min']}~{temp_range['max']}°C"
            
            result.append(f"{date} {city}天气：{weather}，气温：{temp}")
        
        return "\n".join(result)
    
    async def get_travel_route(self, from_city: str, to_city: str, preference: str = "balanced") -> str:
        """获取交通路线建议（模拟数据）"""
        
        # 模拟交通数据
        routes = {
            "沈阳-北京": {
                "高铁": {"time": "2.5小时", "price": "295元", "frequency": "每30分钟一班"},
                "飞机": {"time": "1.5小时", "price": "450元", "frequency": "每天10班"},
                "自驾": {"time": "7小时", "price": "300元", "frequency": "随时"},
                "普通火车": {"time": "8小时", "price": "150元", "frequency": "每天5班"}
            },
            "北京-上海": {
                "高铁": {"time": "4.5小时", "price": "553元", "frequency": "每15分钟一班"},
                "飞机": {"time": "2小时", "price": "600元", "frequency": "每天20班"}
            }
        }
        
        route_key = f"{from_city}-{to_city}"
        if route_key not in routes:
            # 默认数据
            routes[route_key] = {
                "高铁": {"time": "3小时", "price": "300元", "frequency": "每60分钟一班"},
                "飞机": {"time": "2小时", "price": "500元", "frequency": "每天5班"}
            }
        
        route_info = routes[route_key]
        
        # 根据偏好排序
        if preference == "fastest":
            sorted_routes = sorted(route_info.items(), key=lambda x: float(x[1]["time"].replace("小时", "")))
        elif preference == "cheapest":
            sorted_routes = sorted(route_info.items(), key=lambda x: float(x[1]["price"].replace("元", "")))
        else:  # balanced
            sorted_routes = list(route_info.items())
        
        result = [f"从{from_city}到{to_city}的交通方案（按{preference}排序）:"]
        for transport, info in sorted_routes:
            result.append(f"  • {transport}: 时间{info['time']}，价格{info['price']}，{info['frequency']}")
        
        return "\n".join(result)
    
    async def get_university_info(self, university_name: str) -> str:
        """获取大学信息（模拟数据）"""
        
        universities = {
            "东北大学": {
                "location": "辽宁省沈阳市和平区文化路3号巷11号",
                "campus": ["南湖校区", "浑南校区", "沈河校区"],
                "established": "1923年",
                "type": "公立大学",
                "motto": "自强不息，知行合一"
            },
            "清华大学": {
                "location": "北京市海淀区清华园",
                "established": "1911年",
                "type": "公立大学",
                "motto": "自强不息，厚德载物"
            },
            "北京大学": {
                "location": "北京市海淀区颐和园路5号",
                "established": "1898年",
                "type": "公立大学",
                "motto": "爱国、进步、民主、科学"
            }
        }
        
        if university_name not in universities:
            return f"抱歉，没有找到{university_name}的详细信息"
        
        info = universities[university_name]
        result = [f"{university_name}基本信息："]
        result.append(f"• 位置：{info['location']}")
        
        if 'campus' in info:
            result.append(f"• 校区：{', '.join(info['campus'])}")
        
        result.append(f"• 建校时间：{info['established']}")
        result.append(f"• 类型：{info['type']}")
        result.append(f"• 校训：{info['motto']}")
        
        return "\n".join(result)
    
    async def get_current_time(self) -> str:
        """获取当前时间"""
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        return f"当前时间：{current_time}"
    
    async def calculate_distance(self, city1: str, city2: str) -> str:
        """计算城市间距离（模拟数据）"""
        
        distances = {
            "沈阳-北京": "约650公里",
            "北京-上海": "约1200公里",
            "沈阳-上海": "约1600公里"
        }
        
        key1 = f"{city1}-{city2}"
        key2 = f"{city2}-{city1}"
        
        if key1 in distances:
            return f"{city1}到{city2}的距离：{distances[key1]}"
        elif key2 in distances:
            return f"{city2}到{city1}的距离：{distances[key2]}"
        else:
            return f"{city1}到{city2}的距离：约800公里（估算）"
    
    async def search_web(self, query: str) -> str:
        """模拟网络搜索（模拟数据）"""
        search_results = [
            f"关于'{query}'的搜索结果1：这是相关的模拟信息。",
            f"关于'{query}'的搜索结果2：这是另一个相关的模拟信息。",
            f"关于'{query}'的搜索结果3：这是第三个相关的模拟信息。"
        ]
        return "\n".join(search_results)
    
    # === Function Calling 核心逻辑 ===
    
    async def function_calling(self, query: str) -> tuple:
        """执行函数调用"""
        
        messages = [
            {
                "role": "system",
                "content": "你是一个智能助手，可以根据用户问题调用合适的工具来回答问题。可用的工具包括天气查询、交通路线、大学信息查询、网络搜索等。"
            },
            {
                "role": "user",
                "content": query
            }
        ]
        
        response = await self.client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            tools=self.tools,
            tool_choice="auto",
            stream=True
        )
        
        function_name = ""
        function_arguments = ""
        response_content = ""
        fun_id = None
        first_chunk = True
        
        async for chunk in response:
            if chunk.choices[0].delta.tool_calls:
                if first_chunk:
                    function_name = chunk.choices[0].delta.tool_calls[0].function.name
                    function_arguments += chunk.choices[0].delta.tool_calls[0].function.arguments
                    fun_id = chunk.choices[0].delta.tool_calls[0].id
                    first_chunk = False
                else:
                    if chunk.choices[0].delta.tool_calls[0].function.arguments:
                        function_arguments += chunk.choices[0].delta.tool_calls[0].function.arguments
            else:
                if chunk.choices[0].delta.content:
                    response_content += chunk.choices[0].delta.content
                    print(chunk.choices[0].delta.content, end="", flush=True)
        
        return function_name, function_arguments, fun_id, messages, response_content
    
    async def process_query(self, query: str):
        """处理用户查询"""
        
        print(f"\n🤖 用户问题: {query}")
        print("-" * 50)
        
        # 第一步：大模型决定调用哪个工具
        function_name, function_arguments, fun_id, messages, response_content = await self.function_calling(query)
        
        if function_name:
            print(f"\n🔧 执行工具调用：{function_name}")
            print(f"   参数：{function_arguments}")
            
            # 第二步：执行工具函数
            if function_name in self.tool_functions:
                function = self.tool_functions[function_name]
                
                try:
                    # 解析参数
                    args_dict = json.loads(function_arguments)
                    
                    # 执行函数
                    function_result = await function(**args_dict)
                    print(f"✅ 工具执行结果：{function_result}")
                    
                    # 第三步：将结果返回给大模型
                    assistant_message = {
                        "role": "assistant",
                        "content": "",
                        "tool_calls": [{
                            "id": fun_id,
                            "function": {
                                "arguments": function_arguments,
                                "name": function_name
                            },
                            "type": "function"
                        }]
                    }
                    
                    messages.append(assistant_message)
                    messages.append({
                        "role": "tool",
                        "content": function_result,
                        "tool_call_id": fun_id
                    })
                    
                    # 第四步：大模型生成最终回答
                    print("\n💡 大模型结合工具结果生成回答：")
                    final_response = await self.client.chat.completions.create(
                        model="qwen-plus",
                        messages=messages,
                        tools=self.tools,
                        tool_choice="auto",
                        stream=True
                    )
                    
                    final_content = ""
                    async for chunk in final_response:
                        if chunk.choices[0].delta.content:
                            final_content += chunk.choices[0].delta.content
                            print(chunk.choices[0].delta.content, end="", flush=True)
                    
                    print("\n")
                    
                except Exception as e:
                    print(f"❌ 工具执行错误：{e}")
            else:
                print(f"❌ 未知工具：{function_name}")
        else:
            print("📝 大模型直接回答：")
            print(response_content)
            print("\n")
    
    async def run_interactive(self):
        """运行交互式模式"""
        
        print("\n" + "="*60)
        print("🤖 交互式智能助手启动")
        print("="*60)
        print("\n💡 你可以输入任何问题，我会调用合适的工具来回答")
        print("💡 支持的功能：天气查询、交通路线、大学信息、时间查询等")
        print("💡 输入 '退出' 或 'quit' 结束对话")
        print("="*60)
        
        while True:
            try:
                # 获取用户输入
                user_input = input("\n💬 请输入你的问题: ").strip()
                
                if user_input.lower() in ['退出', 'quit', 'exit', 'q']:
                    print("\n👋 感谢使用，再见！")
                    break
                
                if not user_input:
                    print("⚠️  请输入有效的问题")
                    continue
                
                # 处理用户问题
                await self.process_query(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 用户中断，再见！")
                break
            except Exception as e:
                print(f"\n❌ 处理错误：{e}")
                print("请重新输入问题")

async def main():
    """主函数"""
    assistant = InteractiveAssistant()
    await assistant.run_interactive()

if __name__ == "__main__":
    asyncio.run(main())