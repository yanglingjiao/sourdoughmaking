def sourdough_architect():
    print("--- 🍞 欧包大师脚本 v1.0 ---")
    
    # 1. 基础参数输入
    total_flour = float(input("请输入目标面粉总量 (g): "))
    flour_type = input("请输入面粉类型 (low/medium/high): ").lower()
    season = input("当前季节 (summer/winter): ").lower()

    # 2. 核心算法逻辑 (基于视频原理与大师建议)
    # 自动适配含水量 [cite: 56-60]
    hydration_map = {'low': 0.60, 'medium': 0.70, 'high': 0.82}
    hydration_ratio = hydration_map.get(flour_type, 0.70)
    
    # 自动适配天然种比例 [cite: 69-71]
    starter_ratio = 0.10 if season == 'summer' else 0.20
    
    # 固定参数
    salt_ratio = 0.02  # 盐通常占粉量的 2%
    stiff_starter_hydration = 0.50  # 视频推荐的硬种含水量 [cite: 77]

    # 3. 计算组件重量
    # 这里采用 Baker's Math，所有比例均基于主面粉总量 
    starter_weight = total_flour * starter_ratio
    salt_weight = total_flour * salt_ratio
    total_water = total_flour * hydration_ratio
    
    # 硬种拆解 (硬种 = 粉 + 水，由于含水量 50%，粉是水的2倍)
    starter_flour = (starter_weight / (1 + stiff_starter_hydration))
    starter_water = starter_weight - starter_flour
    
    # 最终主面团需要添加的量
    main_flour = total_flour - starter_flour
    main_water = total_water - starter_water

    # 4. 格式化输出
    print("\n" + "="*30)
    print(f"📊 您的【{flour_type.upper()}筋度】欧包执行清单：")
    print(f"1. 预备硬种 (Stiff Starter): {starter_weight:.1f}g")
    print(f"   └─ 喂养比例: {starter_flour:.1f}g粉 + {starter_water:.1f}g水")
    print(f"2. 主面粉 (Main Flour): {main_flour:.1f}g")
    print(f"3. 核心加水 (Water): {main_water:.1f}g")
    print(f"4. 食盐 (Salt): {salt_weight:.1f}g")
    print("="*30)
    print("💡 大师建议：")
    print(f"- 保持目标面温 (TDF) 在 24-26°C。")
    print(f"- 采用发酵探测器 (Probe) 监控体积，翻倍即停止 Bulk Fermentation [cite: 98, 194]。")

sourdough_architect()