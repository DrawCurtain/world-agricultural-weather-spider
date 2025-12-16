import requests
import time

class NetworkRequest:
    """网络请求模块，负责获取图片编号和下载图片"""
    
    def __init__(self):
        self.base_url = 'http://www.worldagweather.com'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_image_numbers(self):
        """获取图片编号
        返回格式：{"forecast": fcstimgnum, "past_pcp": pastpcpimgnum, "past_tmp": pasttmpimgnum}
        """
        url = f'{self.base_url}/cgi-bin/ag/getcropimglabs.pl'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # 解析响应内容，格式为：fcstimgnum|pastpcpimgnum|pasttmpimgnum
            numbers = response.text.strip().split('|')
            if len(numbers) >= 3:
                return {
                    "forecast": numbers[0],
                    "past_pcp": numbers[1],
                    "past_tmp": numbers[2]
                }
            else:
                print(f"获取图片编号失败，响应格式不正确: {response.text}")
                return None
                
        except requests.RequestException as e:
            print(f"获取图片编号时发生错误: {e}")
            return None
    
    def download_image(self, image_url, save_path, retry=3):
        """下载图片
        
        Args:
            image_url: 图片的完整URL
            save_path: 图片的保存路径
            retry: 重试次数
        
        Returns:
            bool: 下载是否成功
        """
        for i in range(retry):
            try:
                response = requests.get(image_url, headers=self.headers, timeout=30)
                response.raise_for_status()
                
                # 保存图片
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"图片下载成功: {save_path}")
                return True
                
            except requests.RequestException as e:
                print(f"下载图片失败 (尝试 {i+1}/{retry}): {image_url}")
                print(f"错误信息: {e}")
                if i < retry - 1:
                    print("等待2秒后重试...")
                    time.sleep(2)
        
        print(f"图片下载失败，已达到最大重试次数: {image_url}")
        return False

# 测试代码
if __name__ == '__main__':
    network = NetworkRequest()
    
    # 测试获取图片编号
    print("测试获取图片编号:")
    image_numbers = network.get_image_numbers()
    if image_numbers:
        print(f"预报图片编号: {image_numbers['forecast']}")
        print(f"历史降水图片编号: {image_numbers['past_pcp']}")
        print(f"历史温度图片编号: {image_numbers['past_tmp']}")
    
    # 测试下载图片 (使用实际的图片URL)
    if image_numbers:
        print("\n测试下载图片:")
        test_url = f'{network.base_url}/crops/fcstwx/fcstpcp_soybeans_usa_{image_numbers["forecast"]}.png'
        test_path = 'test_image.png'
        success = network.download_image(test_url, test_path)
        if success:
            print(f"测试图片已下载到: {test_path}")
        else:
            print("测试图片下载失败")