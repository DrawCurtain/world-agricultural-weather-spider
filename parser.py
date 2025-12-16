class WeatherParser:
    """天气数据解析模块，负责管理国家和地区列表、构建图片URL以及生成图片保存路径"""
    
    def __init__(self):
        # 从网站中提取的作物、国家和地区列表
        self.crops1 = ["corn", "soybeans", "wheat", "rapeseed", "barley"]
        
        # 中英文地区名称映射字典
        self.region_name_map = {
            "usa": "美国",
            "brazil": "巴西",
            "argentina": "阿根廷",
            "china": "中国",
            "canada": "加拿大",
            "europe": "欧洲",
            "ukraine": "乌克兰",
            "australia": "澳大利亚",
            "india": "印度",
            "iowa": "艾奥瓦州",
            "illinois": "伊利诺伊州",
            "nebraska": "内布拉斯加州",
            "minnesota": "明尼苏达州",
            "indiana": "印第安纳州",
            "parana": "巴拉那州",
            "matogrosso": "马托格罗索州",
            "minasgerais": "米纳斯吉拉斯州",
            "goias": "戈亚斯州",
            "riograndedosul": "南里奥格兰德州",
            "buenosaires": "布宜诺斯艾利斯省",
            "cordoba": "科尔多瓦省",
            "santafe": "圣菲省",
            "entrerios": "恩特雷里奥斯省",
            "santiagodelestero": "圣地亚哥-德尔埃斯特罗省",
            "shandong": "山东省",
            "heilongjiang": "黑龙江省",
            "jilin": "吉林省",
            "henan": "河南省",
            "hebei": "河北省",
            "matogrossodosul": "南马托格罗索州",
            "idaho": "爱达荷州",
            "kansas": "堪萨斯州",
            "montana": "蒙大拿州",
            "northdakota": "北达科他州",
            "oklahoma": "俄克拉荷马州",
            "southdakota": "南达科他州",
            "texas": "得克萨斯州",
            "washington": "华盛顿州",
            "alberta": "艾伯塔省",
            "saskatchewan": "萨斯喀彻温省",
            "manitoba": "曼尼托巴省",
            "france": "法国",
            "germany": "德国",
            "uk": "英国",
            "poland": "波兰",
            "spain": "西班牙",
            "czech": "捷克",
            "denmark": "丹麦",
            "central": "中部地区",
            "southern": "南部地区",
            "volga": "伏尔加地区",
            "urals": "乌拉尔地区",
            "siberia": "西伯利亚地区",
            "kazakhstan": "哈萨克斯坦",
            "anhui": "安徽省",
            "jiangsu": "江苏省",
            "westernaustralia": "西澳大利亚州",
            "victoria": "维多利亚州",
            "newsouthwales": "新南威尔士州"
        }
        
        # 地区列表（英文名称，用于构建URL）
        self.regions1 = [
            ["usa", "brazil", "argentina", "china"],  # corn
            ["usa", "brazil", "argentina"],  # soybeans
            ["usa", "canada", "europe", "ukraine", "china", "australia", "india"],  # wheat
            ["canada", "europe"],  # rapeseed
            ["canada", "europe"]  # barley
        ]
        
        # 子地区列表（英文名称，用于构建URL）
        self.subregions1 = [
            # corn
            [
                ["usa", "iowa", "illinois", "nebraska", "minnesota", "indiana"],  # USA
                ["brazil", "parana", "matogrosso", "minasgerais", "goias", "riograndedosul"],  # Brazil
                ["argentina", "buenosaires", "cordoba", "santafe", "entrerios", "santiagodelestero"],  # Argentina
                ["china", "shandong", "heilongjiang", "jilin", "henan", "hebei"]  # China
            ],
            # soybeans
            [
                ["usa", "iowa", "illinois", "minnesota", "indiana", "nebraska"],  # USA
                ["brazil", "matogrosso", "parana", "riograndedosul", "goias", "matogrossodosul"],  # Brazil
                ["argentina", "buenosaires", "cordoba", "santafe", "entrerios", "santiagodelestero"]  # Argentina
            ],
            # wheat
            [
                ["idaho", "kansas", "minnesota", "montana", "northdakota", "oklahoma", "southdakota", "texas", "washington"],  # USA
                ["canada", "alberta", "saskatchewan", "manitoba"],  # Canada
                ["france", "germany", "uk", "poland", "spain"],  # Europe
                ["ukraine", "central", "southern", "volga", "urals", "siberia", "kazakhstan"],  # Ukraine
                ["china", "henan", "shandong", "hebei", "anhui", "jiangsu"],  # China
                ["australia", "westernaustralia", "victoria", "newsouthwales"],  # Australia
                ["india"]  # India
            ],
            # rapeseed
            [
                ["canada", "alberta", "saskatchewan", "manitoba"],  # Canada
                ["france", "germany", "uk", "poland", "czech"]  # Europe
            ],
            # barley
            [
                ["canada", "alberta", "saskatchewan", "manitoba"],  # Canada
                ["france", "germany", "spain", "uk", "denmark"]  # Europe
            ]
        ]
    
    def get_supported_crops(self):
        """获取支持的作物列表"""
        return self.crops1
    
    def get_regions_by_crop(self, crop_index):
        """根据作物获取支持的地区列表
        
        Args:
            crop_index: 作物的索引（0-4）
        
        Returns:
            list: 该作物支持的地区列表
        """
        if 0 <= crop_index < len(self.regions1):
            return self.regions1[crop_index]
        else:
            return []
    
    def get_subregions_by_crop_and_region(self, crop_index, region_index):
        """根据作物和地区获取支持的子地区列表
        
        Args:
            crop_index: 作物的索引（0-4）
            region_index: 地区的索引
        
        Returns:
            list: 该作物和地区支持的子地区列表
        """
        if 0 <= crop_index < len(self.subregions1):
            if 0 <= region_index < len(self.subregions1[crop_index]):
                return self.subregions1[crop_index][region_index]
        return []
        
    def get_chinese_region_name(self, english_name):
        """获取英文地区名称对应的中文名称
        
        Args:
            english_name: 英文地区名称
        
        Returns:
            str: 中文地区名称，如果没有找到映射则返回英文名称
        """
        return self.region_name_map.get(english_name, english_name)
    
    def build_image_url(self, crop_index, region_index, subregion_index, vrbl, nday, fcstimgnum, base_url='http://www.worldagweather.com'):
        """构建图片URL
        
        Args:
            crop_index: 作物的索引（0-4）
            region_index: 地区的索引
            subregion_index: 子地区的索引
            vrbl: 天气变量（"pcp"表示降水，"tmp"表示温度）
            nday: 天数（15, 60, 180）
            fcstimgnum: 图片编号
            base_url: 网站基础URL
        
        Returns:
            str: 完整的图片URL
        """
        # 验证参数
        if not (0 <= crop_index < len(self.crops1)):
            return None
            
        if not (0 <= region_index < len(self.regions1[crop_index])):
            return None
            
        if not (0 <= subregion_index < len(self.subregions1[crop_index][region_index])):
            return None
            
        if vrbl not in ["pcp", "tmp"]:
            return None
            
        if nday not in [15, 60, 180]:
            return None
        
        # 获取作物名称、地区名称和子地区名称
        cropname = self.crops1[crop_index]
        regionname = self.regions1[crop_index][region_index]
        subregionname = self.subregions1[crop_index][region_index][subregion_index]
        
        # 根据天数构建不同类型的图片URL
        if nday == 15:
            # 预报图片
            image_path = f"crops/fcstwx/fcst{vrbl}_{cropname}_{subregionname}_{fcstimgnum}.png"
        else:
            # 历史图片
            if vrbl == "pcp":
                # 历史降水图片
                image_path = f"crops/pastwx/pastpcp_{cropname}_{subregionname}_{nday}day_{fcstimgnum}.png"
            else:
                # 历史温度图片
                image_path = f"crops/pastwx/pasttmp_{cropname}_{subregionname}_{nday}day_{fcstimgnum}.png"
        
        # 构建完整URL
        full_url = f"{base_url}/{image_path}"
        return full_url
    
    def generate_save_path(self, crop_index, region_index, subregion_index, vrbl, nday, save_root='downloads', date_str=None):
        """生成图片保存路径
        
        Args:
            crop_index: 作物的索引（0-4）
            region_index: 地区的索引
            subregion_index: 子地区的索引
            vrbl: 天气变量（"pcp"表示降水，"tmp"表示温度）
            nday: 天数（15, 60, 180）
            save_root: 保存根目录
            date_str: 日期字符串（格式：YYYYMMDD），如果为None则使用当前日期
        
        Returns:
            str: 图片保存路径
        """
        # 验证参数
        if not (0 <= crop_index < len(self.crops1)):
            return None
            
        if not (0 <= region_index < len(self.regions1[crop_index])):
            return None
            
        if not (0 <= subregion_index < len(self.subregions1[crop_index][region_index])):
            return None
            
        if vrbl not in ["pcp", "tmp"]:
            return None
            
        if nday not in [15, 60, 180]:
            return None
        
        # 获取作物名称、地区名称和子地区名称
        cropname = self.crops1[crop_index]
        regionname = self.regions1[crop_index][region_index]
        subregionname = self.subregions1[crop_index][region_index][subregion_index]
        
        # 根据天气变量选择子目录
        if vrbl == "pcp":
            weather_dir = "pcp"
        else:
            weather_dir = "tmp"
        
        # 生成日期目录名
        from datetime import datetime
        if not date_str:
            date_str = datetime.now().strftime("%Y%m%d")
        
        # 生成文件名（不带日期）
        if nday == 15:
            filename = f"{vrbl}_{cropname}_{regionname}_{subregionname}_forecast.png"
        else:
            filename = f"{vrbl}_{cropname}_{regionname}_{subregionname}_{nday}day.png"
        
        # 构建完整保存路径：downloads/[vrbl]/[date]/[filename]
        save_path = f"{save_root}/{weather_dir}/{date_str}/{filename}"
        return save_path

# 测试代码
if __name__ == '__main__':
    parser = WeatherParser()
    
    # 测试获取支持的作物
    print("支持的作物:")
    crops = parser.get_supported_crops()
    for i, crop in enumerate(crops):
        print(f"{i}: {crop}")
    
    # 测试获取作物支持的地区
    print("\n大豆(soybeans)支持的地区:")
    soybean_regions = parser.get_regions_by_crop(1)  # 1表示soybeans
    for i, region in enumerate(soybean_regions):
        print(f"{i}: {region}")
    
    # 测试获取地区支持的子地区
    print("\n大豆(soybeans)美国(USA)支持的子地区:")
    soybean_usa_subregions = parser.get_subregions_by_crop_and_region(1, 0)  # 1表示soybeans，0表示USA
    for i, subregion in enumerate(soybean_usa_subregions):
        print(f"{i}: {subregion}")
    
    # 测试构建图片URL
    print("\n测试构建图片URL:")
    fcstimgnum = "4890"  # 示例图片编号
    image_url = parser.build_image_url(
        crop_index=1,  # soybeans
        region_index=0,  # USA
        subregion_index=0,  # National (usa)
        vrbl="pcp",  # precipitation
        nday=15,  # 15天预报
        fcstimgnum=fcstimgnum
    )
    print(f"图片URL: {image_url}")
    
    # 测试生成保存路径
    print("\n测试生成保存路径:")
    save_path = parser.generate_save_path(
        crop_index=1,  # soybeans
        region_index=0,  # USA
        subregion_index=0,  # National (usa)
        vrbl="pcp",  # precipitation
        nday=15  # 15天预报
    )
    print(f"保存路径: {save_path}")