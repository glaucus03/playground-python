import os
from PIL import Image, ImageDraw, ImageFont

def split_text_to_images(input_file, output_dir, font_path="arial.ttf", font_size=20, max_lines=50, image_width=800):
    # テキストを読み込む
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 出力ディレクトリを作成
    os.makedirs(output_dir, exist_ok=True)

    # フォント設定
    font = ImageFont.truetype(font_path, font_size)
    line_height = font_size + 5
    image_height = line_height * max_lines + 20

    # テキストを分割して画像を作成
    images = []
    for i in range(0, len(lines), max_lines):
        chunk = lines[i:i + max_lines]
        image = Image.new("RGB", (image_width, image_height), "black")
        draw = ImageDraw.Draw(image)

        y = 10
        for line in chunk:
            draw.text((10, y), line.strip(), fill="white", font=font)
            y += line_height

        image_file = os.path.join(output_dir, f"staffroll_{i // max_lines + 1:03d}.png")
        image.save(image_file)
        images.append(image_file)

    return images

# 実行例
split_text_to_images("input.txt", "output_images", max_lines=50)
