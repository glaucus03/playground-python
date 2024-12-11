from PIL import Image, ImageDraw, ImageFont
import os
import cv2

def text_to_single_image(input_text_path, output_image_path, font_path="NotoSansJP-Regular.otf", font_size=24, line_height=30, max_width=1920):
    """
    テキストファイルを読み込み、縦長の1枚の画像を生成
    """
    # フォント設定
    font = ImageFont.truetype(font_path, font_size)

    # テキストを読み込み
    with open(input_text_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 描画する行を計算
    image_height = line_height * len(lines) + 20  # 余白を20px追加
    img = Image.new("RGB", (max_width, image_height), "black")
    draw = ImageDraw.Draw(img)

    # 各行を描画
    y = 10  # 上部余白
    for line in lines:
        draw.text((10, y), line.strip(), fill="white", font=font)
        y += line_height

    # 画像を保存
    img.save(output_image_path)
    print(f"縦長の画像が生成されました: {output_image_path}")
    return output_image_path

def create_video_from_image(image_path, output_video_path, scroll_speed=2, fps=30, video_width=1920, video_height=1080):
    """
    縦長画像を使用してスクロール動画を生成
    """
    img = cv2.imread(image_path)
    img_height, img_width, _ = img.shape

    # 動画設定
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (video_width, video_height))

    y_offset = 0
    total_frames = (img_height - video_height) // scroll_speed + fps  # スクロール終了までのフレーム数

    for _ in range(total_frames):
        frame = img[y_offset:y_offset + video_height, 0:video_width]

        # 必要に応じて下部を黒で埋める
        if frame.shape[0] < video_height:
            pad_height = video_height - frame.shape[0]
            black_pad = cv2.copyMakeBorder(frame, 0, pad_height, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
            frame = black_pad

        out.write(frame)
        y_offset += scroll_speed

    out.release()
    print(f"スクロール動画が生成されました: {output_video_path}")

def main():
    input_text_path = "input.txt"  # 手動で作成したテキストファイル
    output_image_path = "vertical_text_image.png"
    output_video_path = "scroll_video.mp4"
    font_path = "NotoSansJP-Regular.otf"  # 日本語フォントを指定

    # ステップ1: テキストを縦長の画像に変換
    text_to_single_image(input_text_path, output_image_path, font_path=font_path, font_size=24, line_height=30)

    # ステップ2: 縦長画像をスクロール動画に変換
    create_video_from_image(output_image_path, output_video_path, scroll_speed=6, fps=30, video_width=1920, video_height=1080)

if __name__ == "__main__":
    main()
