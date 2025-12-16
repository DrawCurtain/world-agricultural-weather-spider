from setuptools import setup, find_packages

setup(
    name="weather_spider",
    version="1.0.0",
    description="天气数据抓取和汇总工具，用于生成每日天气对比报告",
    author="",
    author_email="",
    packages=find_packages(),
    install_requires=[
        "requests",
        "imgkit"
    ],
    entry_points={
        "console_scripts": [
            "weather-spider=weather_spider.daily_summary:main",
            "html-to-image=weather_spider.html_to_image:main",
            "cleanup-files=weather_spider.cleanup_files:cleanup"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
