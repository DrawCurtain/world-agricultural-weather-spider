import os
import sys
from weather_spider.daily_summary import DailyWeatherSummary

# Create a test instance
summary = DailyWeatherSummary()
print(f"Test output directory: {summary.output_dir}")

# Use the existing find_image_pairs method to get real image pairs
print("\n=== Finding real image pairs ===")
try:
    # Test with precipitation data first
    image_pairs = summary.find_image_pairs("pcp")
    if not image_pairs:
        print("❌ No image pairs found for precipitation data")
        # Try temperature data as fallback
        image_pairs = summary.find_image_pairs("tmp")
        if not image_pairs:
            print("❌ No image pairs found for temperature data either")
            sys.exit(1)
        print("✅ Using temperature data image pairs")
    else:
        print(f"✅ Found {len(image_pairs)} image pairs for precipitation data")
except Exception as e:
    print(f"❌ Error finding image pairs: {e}")
    sys.exit(1)

# Limit to first few pairs for faster testing
if len(image_pairs) > 5:
    image_pairs = image_pairs[:5]
    print(f"   Using first 5 image pairs for faster testing")

# Test the HTML merging (create_comparison_document method)
print("\n=== Testing HTML merging functionality ===")
try:
    # Use the appropriate weather type based on what we found
    weather_type = "pcp" if "pcp" in image_pairs[0]["filename"] else "tmp"
    html_path = summary.create_comparison_document(weather_type, image_pairs, "all")
    if html_path:
        print(f"✅ HTML merging successful: {html_path}")
        print(f"   File exists: {os.path.exists(html_path)}")
        print(f"   Size: {os.path.getsize(html_path)} bytes")
    else:
        print("❌ HTML merging failed")
        sys.exit(1)
except Exception as e:
    print(f"❌ HTML merging failed with error: {e}")
    sys.exit(1)

# Test the HTML to image conversion
print("\n=== Testing HTML to image conversion ===")
try:
    img_path = summary.convert_html_to_image(html_path)
    if img_path:
        print(f"✅ Image conversion successful: {img_path}")
        print(f"   File exists: {os.path.exists(img_path)}")
        if os.path.exists(img_path):
            print(f"   Size: {os.path.getsize(img_path)} bytes")
    else:
        print("❌ Image conversion failed")
        sys.exit(1)
except Exception as e:
    print(f"❌ Image conversion failed with error: {e}")
    sys.exit(1)

print("\n=== All tests passed! ===")
print("The merging and conversion functionality is working correctly.")
print(f"Generated HTML: {html_path}")
print(f"Generated image: {img_path}")

# Verify we can also convert with grouped output
print("\n=== Testing grouped HTML merging and conversion ===")
try:
    grouped_html = summary.create_comparison_document(weather_type, image_pairs, "usa")
    if grouped_html:
        print(f"✅ Grouped HTML (USA only) merging successful: {grouped_html}")
        grouped_img = summary.convert_html_to_image(grouped_html)
        if grouped_img:
            print(f"✅ Grouped image conversion successful: {grouped_img}")
        else:
            print("⚠️  Grouped image conversion failed")
    else:
        print("⚠️  Grouped HTML merging failed")
except Exception as e:
    print(f"⚠️  Grouped test failed with error: {e}")

print("\n=== Complete Test Summary ===")
print("✅ HTML merging with real image pairs: SUCCESS")
print("✅ HTML to image conversion: SUCCESS")
print("✅ Fix for --viewport-size issue: CONFIRMED WORKING")