import cv2
import time
import datetime
from deepface import DeepFace
import numpy as np
import os
import pygame

# =========================
# Audio setup (musik sesuai mood)
# =========================
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
pygame.mixer.set_num_channels(8)
BGM_CHANNEL = pygame.mixer.Channel(0)

# Ganti path file mp3 sesuai lokasi kamu
EMOTION_SONGS = {
    'happy':    'happy.mp3',
    'neutral':  'neutral.mp3',
    'surprise': 'surprise.mp3',
    'sad':      'sad.mp3',
    'angry':    'angry.mp3',
    'fear':     'fear.mp3',
    'disgust':  'disgust.mp3',
}

EMOTION_SOUNDS = {}
for emo, path in EMOTION_SONGS.items():
    if os.path.isfile(path):
        try:
            s = pygame.mixer.Sound(path)
            s.set_volume(0.7)
            EMOTION_SOUNDS[emo] = s
        except Exception as e:
            print(f"[AUDIO] gagal load {path}: {e}")
    else:
        print(f"[AUDIO] tidak ditemukan: {path}")

current_playing_emotion = None
last_switch_ts = 0.0
SWITCH_COOLDOWN = 3.0
FADE_MS = 500

def play_emotion_audio(emotion: str):
    global current_playing_emotion, last_switch_ts
    if emotion is None:
        return
    emotion = emotion.lower()
    if emotion not in EMOTION_SOUNDS:
        emotion = 'neutral'
    now = time.time()
    # jangan ganti terlalu sering
    if current_playing_emotion == emotion and BGM_CHANNEL.get_busy():
        return
    if current_playing_emotion is not None and (now - last_switch_ts) < SWITCH_COOLDOWN:
        return
    new_sound = EMOTION_SOUNDS.get(emotion)
    if new_sound is None:
        return
    try:
        if BGM_CHANNEL.get_busy():
            BGM_CHANNEL.fadeout(FADE_MS)
            time.sleep(min(FADE_MS/1000.0, 0.05))
        BGM_CHANNEL.play(new_sound, loops=-1, fade_ms=FADE_MS)
        current_playing_emotion = emotion
        last_switch_ts = now
    except Exception as e:
        print("[AUDIO] error play:", e)

def stop_audio():
    try:
        if BGM_CHANNEL.get_busy():
            BGM_CHANNEL.fadeout(FADE_MS)
            time.sleep(min(FADE_MS/1000.0, 0.05))
        pygame.mixer.stop()
        pygame.mixer.quit()
    except Exception as e:
        print("[AUDIO] error stop:", e)

# =========================
# UI & DeepFace
# =========================
EMOTION_COLORS = {
    'happy':    (0, 200, 200),
    'neutral':  (200, 200, 200),
    'surprise': (180, 0, 180),
    'sad':      (220, 100, 0),
    'angry':    (0, 0, 200),
    'fear':     (0, 150, 220),
    'disgust':  (0, 200, 0),
}
DEFAULT_COLOR = (120, 120, 120)
EMOTION_ORDER = ['happy', 'neutral', 'surprise', 'sad', 'angry', 'fear', 'disgust']

def safe_str_gender(result):
    candidates = []
    if isinstance(result, dict):
        for key in ('gender', 'dominant_gender', 'dominant_gender_name'):
            v = result.get(key)
            if v is None:
                continue
            if isinstance(v, dict):
                try:
                    k = max(v.items(), key=lambda x: float(x[1]))[0]
                    candidates.append(str(k))
                except:
                    pass
            else:
                candidates.append(str(v))
    if candidates:
        for c in candidates:
            if c and c.lower() not in ('none', 'nan'):
                return c
    return None  # return None when unknown (we'll hide it)

def safe_name(result):
    if not isinstance(result, dict):
        return None
    for k in ('identity', 'name'):
        v = result.get(k)
        if isinstance(v, str) and v.strip():
            return os.path.splitext(os.path.basename(v))[0]
    return None

def get_mood_color(emotion):
    return EMOTION_COLORS.get(emotion.lower(), DEFAULT_COLOR)

def luminance(bgr):
    # compute perceived luminance to choose text color (BGR input)
    b, g, r = bgr
    return 0.299*r + 0.587*g + 0.114*b

def pick_text_color(bg_bgr):
    # return (0,0,0) or (255,255,255) based on bg
    return (0,0,0) if luminance(bg_bgr) > 150 else (255,255,255)

def draw_label_simple(img, text, x, y, bg_color=(0,0,0), text_color=(255,255,255), padding=8, font_scale=0.9, thickness=2):
    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
    x2 = x + tw + padding
    y2 = y - th - padding//2
    x = max(0, x)
    y = max(th + padding, y)
    # ensure within width
    img_h, img_w = img.shape[:2]
    if x2 > img_w - 4:
        x2 = img_w - 4
        tw = x2 - x - padding
    cv2.rectangle(img, (x, y2), (x2, y + 4), bg_color, -1)
    cv2.putText(img, text, (x + 6, y - 4), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, thickness, cv2.LINE_AA)

def draw_emotion_stats_panel(frame, emotion_scores, x, y, panel_w=220):
    n = len(EMOTION_ORDER)
    bar_h = 18
    gap = 8
    header_h = 36
    panel_h = header_h + n * (bar_h + gap) + 10
    cv2.rectangle(frame, (x, y), (x + panel_w, y + panel_h), (10,10,10), -1)
    cv2.rectangle(frame, (x, y), (x + panel_w, y + header_h), (30,30,30), -1)
    cv2.putText(frame, "Emotion Stats", (x + 10, y + 24),
                cv2.FONT_HERSHEY_DUPLEX, 0.6, (255,255,255), 1, cv2.LINE_AA)
    dominant = None
    if emotion_scores:
        try:
            dominant = max(emotion_scores.items(), key=lambda kv: float(kv[1]))[0]
        except:
            dominant = None
    for i, emo in enumerate(EMOTION_ORDER):
        val = float(emotion_scores.get(emo, 0.0)) if emotion_scores else 0.0
        yy = y + header_h + 8 + i * (bar_h + gap)
        cv2.rectangle(frame, (x + 8, yy), (x + panel_w - 12, yy + bar_h), (45,45,45), -1)
        max_w = panel_w - 8 - 12
        fill_w = int((val / 100.0) * max_w)
        color = get_mood_color(emo)
        cv2.rectangle(frame, (x + 8, yy), (x + 8 + fill_w, yy + bar_h), color, -1)
        label = f"{emo}: {val:.1f}%"
        cv2.putText(frame, label, (x + 10, yy + 14), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (240,240,240), 1, cv2.LINE_AA)
        if emo == dominant:
            cv2.rectangle(frame, (x + 6, yy - 2), (x + panel_w - 10, yy + bar_h + 2), (255,255,255), 1)

# =========================
# Main
# =========================
def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Kamera tidak terbuka.")
        stop_audio()
        return

    analyze_every = 5
    frame_idx = 0
    last_box = None
    last_age = "..."
    last_gender = None
    last_name = None
    last_emotion = "neutral"
    last_scores = {}

    print("Tekan 'q' untuk keluar.")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            h, w = frame.shape[:2]
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if frame_idx % analyze_every == 0:
                try:
                    res = DeepFace.analyze(img_path=rgb,
                                           actions=['emotion', 'age', 'gender'],
                                           detector_backend='opencv',
                                           enforce_detection=False)
                    result = res[0] if isinstance(res, list) else res

                    # dominant emotion
                    dom = result.get('dominant_emotion') or last_emotion
                    dom = dom.lower() if isinstance(dom, str) else last_emotion
                    if dom not in EMOTION_COLORS:
                        dom = 'neutral'
                    last_emotion = dom

                    # age
                    age_val = result.get('age', None)
                    try:
                        if age_val is not None:
                            last_age = str(int(float(age_val)))
                    except:
                        last_age = str(age_val) if age_val is not None else "..."

                    # gender & name (may return None)
                    last_gender = safe_str_gender(result)
                    last_name = safe_name(result)

                    # scores
                    raw_scores = result.get('emotion', {})
                    if isinstance(raw_scores, dict):
                        last_scores = {k.lower(): float(v) for k, v in raw_scores.items()}
                    else:
                        last_scores = {}

                    # region
                    region = result.get('region', {}) or {}
                    rx = int(region.get('x', 0))
                    ry = int(region.get('y', 0))
                    rw = int(region.get('w', 0))
                    rh = int(region.get('h', 0))
                    if rw > 0 and rh > 0 and rw < int(0.9*w):
                        rx = max(0, min(rx, w-1))
                        ry = max(0, min(ry, h-1))
                        rw = min(rw, w-rx)
                        rh = min(rh, h-ry)
                        last_box = (rx, ry, rw, rh)
                    else:
                        last_box = None

                    # play audio for dominant emotion (if available)
                    play_emotion_audio(last_emotion)

                except Exception as e:
                    print("DeepFace warn:", str(e))

            # header
            title = "Politeknik AI Budi Mulia Dua"
            timestr = datetime.datetime.now().strftime("%A, %d %B %Y %H:%M:%S")
            cv2.putText(frame, title, (14, 28), cv2.FONT_HERSHEY_DUPLEX, 0.75, (10,10,10), 4, cv2.LINE_AA)
            cv2.putText(frame, title, (14, 28), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, timestr, (16, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (210,210,210), 1, cv2.LINE_AA)

            # face rectangle + labels
            if last_box is not None:
                bx, by, bw, bh = last_box
                mood_color = get_mood_color(last_emotion)
                text_col = pick_text_color(mood_color)
                cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), mood_color, 2)

                # build top label components but hide unknown parts
                parts = []
                if last_name:
                    parts.append(last_name)
                if last_gender:
                    parts.append(str(last_gender))
                if last_age:
                    parts.append(str(last_age))
                label_top = " | ".join(parts) if parts else ""

                # bigger font for labels
                if label_top:
                    draw_label_simple(frame, label_top, bx, by - 14, bg_color=mood_color, text_color=text_col, font_scale=0.95, thickness=2)
                # bottom: emotion (bigger)
                label_bot = last_emotion.capitalize()
                draw_label_simple(frame, label_bot, bx, by + bh + 30, bg_color=mood_color, text_color=text_col, font_scale=0.95, thickness=2)

            # emotion stats panel
            panel_x = w - 240
            panel_y = 40
            draw_emotion_stats_panel(frame, last_scores, panel_x, panel_y, panel_w=220)

            cv2.imshow("Emotion UI - Politeknik AI", frame)
            frame_idx += 1
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        stop_audio()

if __name__ == "__main__":
    main()

