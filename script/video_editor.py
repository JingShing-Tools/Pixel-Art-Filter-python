import cv2
from pixel_transform import transform
import re
from tqdm import tqdm

def video_edit(path, set_dict):
    cap = cv2.VideoCapture(path)

    # fps = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_index = 0
    process = tqdm(total=frame_length)

    path.replace("\\", "/")
    file_name = re.split("/", path)[-1]
    file_format = file_name.split('.')[-1]
    file_name = file_name.split('.'+file_format)[0]
    cover = None

    fourcc = None
    if file_format == 'avi':
        fourcc = cv2.VideoWriter_fourcc(*'XVID') # windows
    elif file_format == 'mp4':
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # macos
    elif file_format == 'flv':
        fourcc = cv2.VideoWriter_fourcc(*'flv1')
    #     # fourcc = cv2.VideoWriter_fourcc(*'FLV1')
    #     fourcc = cv2.VideoWriter_fourcc('F','L','V','1')

    if fourcc:
        out = cv2.VideoWriter(file_name + '_edited' + '.' + file_format, fourcc, frame_fps, (frame_width,  frame_height))
        # out = cv2.VideoWriter(file_name + '_edited' + '.' + file_format, fourcc, frame_fps, (frame_width,  frame_height), 0)

        while(cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break

            frame = transform(frame, set_dict)
            # Turn into right color space
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            # compress frame
            frame = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_AREA)
            out.write(frame)
            
            cv2.imshow('frame_rendering', frame)
            if cv2.waitKey(1) == ord('q'):
                # press q to stop render
                print('Stop rendering video')
                break

            if frame_index == 0:
                cover = frame
            frame_index += 1
            process.update(1)
            # print("Editing Frame {} / {}".format(frame_index, frame_length))

            
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        # cv2.destroyAllWindows()
        print('done')
        return cover