from downloader import ImageDownloader
import sys
import argparse

class WeatherSpider:
    """主程序类，整合所有功能"""
    
    def __init__(self):
        self.downloader = ImageDownloader()
        self.crops = self.downloader.parser.get_supported_crops()
    
    def show_menu(self):
        """显示主菜单"""
        print("=" * 50)
        print("世界农业天气数据爬虫")
        print("=" * 50)
        print("支持下载降水(PCP)和温度(TMP)数据")
        print("\n可选的作物:")
        for i, crop in enumerate(self.crops):
            print(f"{i}: {crop}")
        print("\n可选的数据类型:")
        print("0: 降水(PCP)")
        print("1: 温度(TMP)")
        print("\n可选的天数:")
        print("1: 15天预报")
        print("2: 60天历史数据")
        print("3: 180天历史数据")
        print("=" * 50)
    
    def get_user_choice(self):
        """获取用户选择"""
        # 获取作物选择
        while True:
            try:
                crop_choice = int(input("请输入作物编号: "))
                if 0 <= crop_choice < len(self.crops):
                    break
                else:
                    print(f"请输入0-{len(self.crops)-1}之间的数字")
            except ValueError:
                print("请输入有效的数字")
        
        # 获取数据类型选择
        while True:
            try:
                data_type_choice = int(input("请输入数据类型编号: "))
                if data_type_choice in [0, 1]:
                    break
                else:
                    print("请输入0或1")
            except ValueError:
                print("请输入有效的数字")
        
        # 获取天数选择
        while True:
            try:
                day_choice = int(input("请输入天数编号: "))
                if day_choice in [1, 2, 3]:
                    break
                else:
                    print("请输入1、2或3")
            except ValueError:
                print("请输入有效的数字")
        
        # 转换用户选择为实际参数
        vrbl = "pcp" if data_type_choice == 0 else "tmp"
        nday_map = {1: 15, 2: 60, 3: 180}
        nday = nday_map[day_choice]
        
        return crop_choice, vrbl, nday
    
    def run(self):
        """运行爬虫"""
        while True:
            self.show_menu()
            
            # 获取用户选择
            crop_choice, vrbl, nday = self.get_user_choice()
            
            print(f"\n准备下载: {self.crops[crop_choice]} 的 {vrbl} 数据 ({nday}天)")
            
            # 确认下载
            confirm = input("是否继续? (y/n): ")
            if confirm.lower() != "y":
                print("下载已取消")
                continue
            
            # 执行下载
            print(f"\n开始下载 {self.crops[crop_choice]} 的 {vrbl} 数据 ({nday}天)...")
            results = self.downloader.download_all_images_by_crop(
                crop_index=crop_choice,
                vrbl=vrbl,
                nday=nday
            )
            
            # 显示下载结果
            self.show_results(results)
            
            # 询问是否继续下载
            again = input("\n是否继续下载其他数据? (y/n): ")
            if again.lower() != "y":
                break
    
    def show_results(self, results):
        """显示下载结果"""
        print("\n" + "=" * 50)
        print("下载结果统计")
        print("=" * 50)
        
        if not results:
            print("没有下载任何图片")
            return
        
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        
        print(f"总图片数: {total_count}")
        print(f"成功下载: {success_count}")
        print(f"下载失败: {total_count - success_count}")
        print(f"成功率: {(success_count / total_count * 100):.1f}%")
        
        if success_count > 0:
            print("\n成功下载的图片:")
            for path, success in results.items():
                if success:
                    print(f"✓ {path}")
        
        if total_count - success_count > 0:
            print("\n下载失败的图片:")
            for path, success in results.items():
                if not success:
                    print(f"✗ {path}")

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='世界农业天气数据爬虫')
    parser.add_argument('-c', '--crop', type=int, help='作物编号', required=False)
    parser.add_argument('-d', '--datatype', type=int, help='数据类型编号 (0: 降水, 1: 温度)', required=False)
    parser.add_argument('-n', '--days', type=int, help='天数编号 (1: 15天, 2: 60天, 3: 180天)', required=False)
    return parser.parse_args()

if __name__ == '__main__':
    spider = WeatherSpider()
    args = parse_args()
    
    # 如果没有提供命令行参数，则运行交互式界面
    if not args.crop and not args.datatype and not args.days:
        spider.run()
    else:
        # 验证命令行参数
        if args.crop is None or not (0 <= args.crop < len(spider.crops)):
            print(f"错误: 作物编号必须是0-{len(spider.crops)-1}之间的数字")
            sys.exit(1)
        
        if args.datatype is None or args.datatype not in [0, 1]:
            print("错误: 数据类型编号必须是0或1")
            sys.exit(1)
        
        if args.days is None or args.days not in [1, 2, 3]:
            print("错误: 天数编号必须是1、2或3")
            sys.exit(1)
        
        # 转换参数
        vrbl = "pcp" if args.datatype == 0 else "tmp"
        nday_map = {1: 15, 2: 60, 3: 180}
        nday = nday_map[args.days]
        
        # 执行下载
        print(f"开始下载 {spider.crops[args.crop]} 的 {vrbl} 数据 ({nday}天)...")
        results = spider.downloader.download_all_images_by_crop(
            crop_index=args.crop,
            vrbl=vrbl,
            nday=nday
        )
        
        # 显示结果
        spider.show_results(results)