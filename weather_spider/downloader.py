import os
from .network import NetworkRequest
from .parser import WeatherParser

class ImageDownloader:
    """图片下载器，用于按国家和地区分类下载降水和温度图片"""
    
    def __init__(self):
        self.network = NetworkRequest()
        self.parser = WeatherParser()
    
    def ensure_directory_exists(self, directory):
        """确保目录存在，如果不存在则创建"""
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def download_all_images_by_crop(self, crop_index, vrbl, nday=15, date_str=None):
        """下载指定作物的所有国家和地区的图片

        Args:
            crop_index: 作物的索引（0-4）
            vrbl: 天气变量（"pcp"表示降水，"tmp"表示温度）
            nday: 天数（15, 60, 180），默认是15
            date_str: 日期字符串（格式：YYYYMMDD），如果为None则使用当前日期

        Returns:
            dict: 下载结果，键为图片保存路径，值为布尔值表示下载是否成功
        """
        from .daily_summary import log
        results = {}

        # 获取指定作物的所有地区
        regions = self.parser.get_regions_by_crop(crop_index)
        crops = self.parser.get_supported_crops()
        crop_name = crops[crop_index]

        total_count = 0
        success_count = 0

        for region_index, region in enumerate(regions):
            # 获取该地区的所有子地区
            subregions = self.parser.get_subregions_by_crop_and_region(crop_index, region_index)

            for subregion_index, subregion in enumerate(subregions):
                # 下载该子地区的图片
                result = self.download_image(crop_index, region_index, subregion_index, vrbl, nday, date_str)
                results.update(result)
                total_count += 1
                for path, success in result.items():
                    if success:
                        success_count += 1

        log(f"  {crop_name} {vrbl}: {success_count}/{total_count} 下载成功")
        return results
    
    def download_all_images_by_region(self, crop_index, region_index, vrbl, nday=15, date_str=None):
        """下载指定作物和地区的所有子地区的图片

        Args:
            crop_index: 作物的索引（0-4）
            region_index: 地区的索引
            vrbl: 天气变量（"pcp"表示降水，"tmp"表示温度）
            nday: 天数（15, 60, 180），默认是15
            date_str: 日期字符串（格式：YYYYMMDD），如果为None则使用当前日期

        Returns:
            dict: 下载结果，键为图片保存路径，值为布尔值表示下载是否成功
        """
        results = {}

        # 获取该地区的所有子地区
        subregions = self.parser.get_subregions_by_crop_and_region(crop_index, region_index)

        for subregion_index, subregion in enumerate(subregions):
            # 下载该子地区的图片
            result = self.download_image(crop_index, region_index, subregion_index, vrbl, nday, date_str)
            results.update(result)

        return results

    def download_image(self, crop_index, region_index, subregion_index, vrbl, nday=15, date_str=None):
        """下载指定作物、地区和子地区的图片

        Args:
            crop_index: 作物的索引（0-4）
            region_index: 地区的索引
            subregion_index: 子地区的索引
            vrbl: 天气变量（"pcp"表示降水，"tmp"表示温度）
            nday: 天数（15, 60, 180），默认是15
            date_str: 日期字符串（格式：YYYYMMDD），如果为None则使用当前日期

        Returns:
            dict: 下载结果，键为图片保存路径，值为布尔值表示下载是否成功
        """
        result = {}

        try:
            # 获取图片编号
            img_numbers = self.network.get_image_numbers()

            if not img_numbers:
                return result

            # 根据vrbl选择对应的图片编号
            if vrbl == "pcp":
                if nday == 15:
                    img_number = img_numbers["forecast"]  # 预报降水
                else:
                    img_number = img_numbers["past_pcp"]  # 历史降水
            else:
                if nday == 15:
                    img_number = img_numbers["forecast"]  # 预报温度
                else:
                    img_number = img_numbers["past_tmp"]  # 历史温度

            # 构建图片URL
            image_url = self.parser.build_image_url(
                crop_index=crop_index,
                region_index=region_index,
                subregion_index=subregion_index,
                vrbl=vrbl,
                nday=nday,
                fcstimgnum=img_number
            )

            if not image_url:
                return result

            # 生成保存路径
            save_path = self.parser.generate_save_path(
                crop_index=crop_index,
                region_index=region_index,
                subregion_index=subregion_index,
                vrbl=vrbl,
                nday=nday,
                date_str=date_str
            )

            if not save_path:
                return result

            # 确保保存目录存在
            directory = os.path.dirname(save_path)
            self.ensure_directory_exists(directory)

            # 下载图片
            success = self.network.download_image(image_url, save_path)

            if success:
                result[save_path] = True
            else:
                result[save_path] = False

        except Exception as e:
            pass  # 静默失败，避免大量错误日志

        return result