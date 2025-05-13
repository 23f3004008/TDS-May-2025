from PIL import Image
import numpy as np
from collections import Counter
import os
import io

def analyze_image(image_path):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img_array = np.array(img)
    pixels = img_array.reshape(-1, 3)
    unique_colors = np.unique(pixels, axis=0)
    color_counts = Counter(map(tuple, pixels))
    width, height = img.size
    
    return {
        'dimensions': (width, height),
        'total_pixels': width * height,
        'unique_colors': len(unique_colors),
        'color_distribution': dict(color_counts),
        'original_size': os.path.getsize(image_path)
    }

def try_multiple_compressions(image_path, base_output_name):
    img = Image.open(image_path)
    original_size = os.path.getsize(image_path)
    compression_results = []
    if img.mode != 'RGB':
        img = img.convert('RGB')
    png_path = f"{base_output_name}_max.png"
    img.save(png_path, 'PNG', optimize=True, compress_level=9)
    jpg_path = f"{base_output_name}_high.jpg"
    img.save(jpg_path, 'JPEG', quality=95, optimize=True)
    jpg_med_path = f"{base_output_name}_medium.jpg"
    img.save(jpg_med_path, 'JPEG', quality=85, optimize=True)
    webp_lossless_path = f"{base_output_name}_lossless.webp"
    img.save(webp_lossless_path, 'WEBP', lossless=True, quality=100)
    webp_lossy_path = f"{base_output_name}_lossy.webp"
    img.save(webp_lossy_path, 'WEBP', lossless=False, quality=90)
    formats = [
        ('PNG (Max Compression)', png_path),
        ('JPEG (High Quality)', jpg_path),
        ('JPEG (Medium Quality)', jpg_med_path),
        ('WebP (Lossless)', webp_lossless_path),
        ('WebP (Lossy)', webp_lossy_path)
    ]

    results = []
    for format_name, path in formats:
        size = os.path.getsize(path)
        comparison = compare_images(image_path, path)
        results.append({
            'format': format_name,
            'path': path,
            'size': size,
            'compression_ratio': size / original_size,
            'identical': comparison['identical'],
            'psnr': comparison['psnr'] if 'psnr' in comparison else None
        })

    return results

def compare_images(original_path, compressed_path):
    original = Image.open(original_path)
    compressed = Image.open(compressed_path)
    if original.mode != 'RGB':
        original = original.convert('RGB')
    if compressed.mode != 'RGB':
        compressed = compressed.convert('RGB')
    original_array = np.array(original, dtype=np.float32)
    compressed_array = np.array(compressed, dtype=np.float32)
    
    are_identical = np.array_equal(original_array, compressed_array)
    
    psnr = None
    if not are_identical:
        mse = np.mean((original_array - compressed_array) ** 2)
        if mse > 0:
            psnr = 20 * np.log10(255.0 / np.sqrt(mse))
    
    return {
        'identical': are_identical,
        'original_size': os.path.getsize(original_path),
        'compressed_size': os.path.getsize(compressed_path),
        'compression_ratio': os.path.getsize(compressed_path) / os.path.getsize(original_path),
        'psnr': psnr
    }

def main():
    input_image = 'download.png'
    output_base = 'compressed_q2image'
    
    print("\nAnalyzing original image...")
    analysis = analyze_image(input_image)
    print(f"Image dimensions: {analysis['dimensions']}")
    print(f"Total pixels: {analysis['total_pixels']}")
    print(f"Number of unique colors: {analysis['unique_colors']}")
    print(f"Original file size: {analysis['original_size']} bytes")
    
    print("\nTrying different compression methods...")
    compression_results = try_multiple_compressions(input_image, output_base)
    
    print("\nCompression Results:")
    print("-" * 80)
    print(f"{'Format':<20} {'Size (bytes)':<15} {'Ratio':<10} {'Identical':<10} {'PSNR':<10}")
    print("-" * 80)
    
    for result in sorted(compression_results, key=lambda x: x['size']):
        psnr_str = f"{result['psnr']:.2f}" if result['psnr'] is not None else "N/A"
        print(f"{result['format']:<20} {result['size']:<15} {result['compression_ratio']:.3f}x    "
              f"{'Yes' if result['identical'] else 'No':<10} {psnr_str:<10}")


if __name__ == "__main__":
    main() 
