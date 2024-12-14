from PIL import Image, ImageDraw, ImageFont
import cv2
import os

def calculate_lines_per_screen(font_path, font_size, line_height, screen_height=1080):
    """
    1画面に収まる行数を計算
    """
    font = ImageFont.truetype(font_path, font_size)
    return screen_height // line_height

def generate_images_with_overlap(input_text, output_dir, font_path, font_size=24, line_height=30, max_width=1920, screen_height=1080):
    """
    前後の行を含む画像を生成
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # テキストを行単位で分割
    with open(input_text, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 1画面に収まる行数
    lines_per_screen = calculate_lines_per_screen(font_path, font_size, line_height, screen_height)
    extra_lines = lines_per_screen // 2  # 前後に余分な行を含む
    images = []

    # フォント設定
    font = ImageFont.truetype(font_path, font_size)

    # スライスごとに画像生成
    for i in range(0, len(lines), lines_per_screen):
        chunk = lines[max(0, i - extra_lines):min(len(lines), i + lines_per_screen + extra_lines)]
        img_height = line_height * len(chunk)
        img = Image.new("RGB", (max_width, img_height), "black")
        draw = ImageDraw.Draw(img)

        y = 0
        for line in chunk:
            draw.text((10, y), line.strip(), fill="white", font=font)
            y += line_height

        output_image_path = os.path.join(output_dir, f"frame_{i // lines_per_screen:03d}.png")
        img.save(output_image_path)
        images.append(output_image_path)
        print(f"生成された画像: {output_image_path}")

    return images, lines_per_screen

def generate_video_frames(images, output_frames_dir, scroll_speed, fps, line_height, screen_height=1080):
    """
    1ピクセルずつ動かしてフレームを生成
    """
    os.makedirs(output_frames_dir, exist_ok=True)
    frame_count = 0

    for img_path in images:
        img = Image.open(img_path)
        img_width, img_height = img.size

        for y_offset in range(0, img_height - screen_height, scroll_speed):
            frame = img.crop((0, y_offset, img_width, y_offset + screen_height))
            output_frame_path = os.path.join(output_frames_dir, f"frame_{frame_count:05d}.png")
            frame.save(output_frame_path)
            frame_count += 1

    print(f"すべてのフレームが生成されました: {frame_count} フレーム")
    return frame_count

def frames_to_video(frames_dir, output_video_path, fps, screen_width=1920, screen_height=1080):
    """
    生成したフレームを動画に結合
    """
    frames = sorted([os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.endswith(".png")])
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (screen_width, screen_height))

    for frame_path in frames:
        frame = cv2.imread(frame_path)
        out.write(frame)

    out.release()
    print(f"動画が生成されました: {output_video_path}")

def main():
    input_text = "input_text.txt"  # 入力テキストファイル
    output_dir = "images"  # テキストから生成する画像保存先
    output_frames_dir = "frames"  # フレーム保存先
    output_video_path = "endroll_video.mp4"  # 最終動画
    font_path = "NotoSansJP-Regular.otf"  # 日本語フォント
    font_size = 24
    line_height = 30
    scroll_speed = 1  # ピクセル単位のスクロール速度
    fps = 30

    # 画像生成（前後の行を含む）
    images, lines_per_screen = generate_images_with_overlap(input_text, output_dir, font_path, font_size, line_height)

    # フレームを生成
    generate_video_frames(images, output_frames_dir, scroll_speed, fps, line_height)

    # フレームから動画を生成
    frames_to_video(output_frames_dir, output_video_path, fps)

if __name__ == "__main__":
    main()
