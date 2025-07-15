import cv2 as cv
import pywt
import numpy as np
import os
import sys
import json
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='DWT Color + Grayscale Compression')
    parser.add_argument('--image', type=str, required=True)
    parser.add_argument('--aggressive', action='store_true')
    parser.add_argument('--output_color', type=str, default='compressed_color.jpg')
    parser.add_argument('--output_gray', type=str, default='compressed_gray.jpg')
    return parser.parse_args()

def compress_channel(channel, wavelet, threshold, aggressive):
    ll, (lh, hl, hh) = pywt.dwt2(channel, wavelet)
    if aggressive:
        lh[:] = 0
        hl[:] = 0
        hh[:] = 0
    else:
        lh[np.abs(lh) < threshold] = 0
        hl[np.abs(hl) < threshold] = 0
        hh[np.abs(hh) < threshold] = 0
    compressed_channel = pywt.idwt2((ll, (lh, hl, hh)), wavelet)
    return np.clip(compressed_channel, 0, 255)

def main():
    args = parse_args()
    wavelet = 'haar'
    threshold = 10

    original_size = os.path.getsize(args.image)

    # Color Compression 
    img_color = cv.imread(args.image, cv.IMREAD_COLOR)
    if img_color is None:
        print(json.dumps({'error': 'Invalid image'}))
        sys.exit(1)

    b, g, r = cv.split(img_color)
    b_c = compress_channel(b, wavelet, threshold, args.aggressive)
    g_c = compress_channel(g, wavelet, threshold, args.aggressive)
    r_c = compress_channel(r, wavelet, threshold, args.aggressive)
    compressed_color = cv.merge([b_c.astype(np.uint8), g_c.astype(np.uint8), r_c.astype(np.uint8)])
    cv.imwrite(args.output_color, compressed_color, [cv.IMWRITE_JPEG_QUALITY, 80])
    color_size = os.path.getsize(args.output_color)

    # Grayscale Compression 
    img_gray = cv.imread(args.image, cv.IMREAD_GRAYSCALE)
    gray_c = compress_channel(img_gray, wavelet, threshold, args.aggressive)
    gray_c = gray_c.astype(np.uint8)
    cv.imwrite(args.output_gray, gray_c, [cv.IMWRITE_JPEG_QUALITY, 80])
    gray_size = os.path.getsize(args.output_gray)

    result = {
        'original_size': original_size,
        'color': {
            'compressed_size': color_size,
            'compression_ratio': round(original_size / color_size, 3) if color_size else None
        },
        'grayscale': {
            'compressed_size': gray_size,
            'compression_ratio': round(original_size / gray_size, 3) if gray_size else None
        }
    }

    print(json.dumps(result))

if __name__ == '__main__':
    main()
