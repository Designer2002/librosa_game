import librosa
import pickle

HEIGHT = 600  # высота экрана
circle_speed = 3  # скорость круга

# Рассчитайте расстояние до третьей части экрана
third_distance = HEIGHT / 3 / circle_speed / 10

# Рассчитайте время, необходимое для достижения третьей части экрана
time_to_reach = third_distance / circle_speed

def make_frequency(self):
    y, sr = librosa.load('resources/psy-gangnam-style.mp3')
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    beat_frames = librosa.frames_to_time(librosa.util.fix_frames(librosa.beat.beat_track(y=y, sr=sr)[1]), sr=sr)
    adjusted_beat_frames = [beat_frames - time_to_reach for beat_frame in beat_frames]
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    adjusted_onset_times = [a - time_to_reach for a in onset_times]
    frequency = {
    "beat" : adjusted_beat_frames,
    "onset" : adjusted_onset_times
    }
    serialized = pickle.dumps(freq)
    with open("resources/frequency", "wb") as file:
        file.write(serialized)