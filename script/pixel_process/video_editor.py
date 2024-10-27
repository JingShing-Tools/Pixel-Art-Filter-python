import cv2
from pixel_process.pixel_transform import transform
import re
from tqdm import tqdm

def video_edit(path, set_dict):
    cap = cv2.VideoCapture(path)

    # 獲取影片屬性
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_fps = int(cap.get(cv2.CAP_PROP_FPS))

    # 初始化進度條
    process = tqdm(total=frame_length, desc="Processing Video")

    # 處理影片路徑和格式
    path = path.replace("\\", "/")
    file_name, file_format = re.split("/", path)[-1].rsplit('.', 1)
    fourcc = get_fourcc(file_format)

    # 檢查四字符碼並初始化寫入器
    if fourcc:
        out = cv2.VideoWriter(f"{file_name}_edited.{file_format}", fourcc, frame_fps, (frame_width, frame_height))
        cover = None
        frame_index = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 轉換與顯示
            frame = transform(frame, set_dict)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_AREA)
            out.write(frame)

            cv2.imshow('frame_rendering', frame)
            if cv2.waitKey(1) == ord('q'):
                print('Rendering stopped by user.')
                break

            if frame_index == 0:
                cover = frame
            frame_index += 1
            process.update(1)

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        print('Processing complete.')
        return cover

def get_fourcc(file_format):
    """返回對應的四字符碼"""
    return {
        'avi': cv2.VideoWriter_fourcc(*'XVID'),  # Windows
        'mp4': cv2.VideoWriter_fourcc(*'mp4v'),  # macOS
        'flv': cv2.VideoWriter_fourcc(*'flv1')   # FLV
    }.get(file_format, None)
