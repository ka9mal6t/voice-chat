import pyaudio
import socket
import threading
import tkinter as tk
from tkinter import messagebox

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 512
SERVER_IP = '4.tcp.eu.ngrok.io'  # Адрес сервера
SERVER_PORT = 13509  # Порт сервера

p = None
stream = None
sock = None
recv_thread = None
send_thread = None
send_thread_running = True


def receive_audio():
    global stream_active
    while True:
        try:
            data = sock.recv(CHUNK)
            stream.write(data)
        except Exception as e:
            print("Error receiving audio:", e)
            break


def send_audio():
    global stream_active, send_thread_running
    while send_thread_running:
        try:
            data = stream.read(CHUNK)
            sock.sendall(data)
        except Exception as e:
            print("Error sending audio:", e)
            break


def start_audio():
    global p, stream, sock, stream_active, recv_thread, send_thread
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_IP, SERVER_PORT))
    except Exception as e:
        print("Error connecting to server:", e)
        return

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)

    stream_active = True  # После успешного открытия потока устанавливаем флаг активности

    recv_thread = threading.Thread(target=receive_audio)
    recv_thread.start()

    send_thread = threading.Thread(target=send_audio)
    send_thread.start()


def stop_audio():
    global p, stream, sock, stream_active, recv_thread, send_thread
    sock.close()


def start_button_clicked():
    start_audio()
    messagebox.showinfo("Info", "Аудио передача начата.")


def stop_button_clicked():
    stop_audio()
    messagebox.showinfo("Info", "Аудио передача остановлена.")


def mute_button_clicked():
    global send_thread_running, recv_thread
    if mute_button.cget("text") == "Mute":
        mute_button.config(text="Unmute")
        send_thread_running = False  # Устанавливаем флаг для остановки потока
        send_thread.join()
    else:
        mute_button.config(text="Mute")
        send_thread_running = True
        new_thread = threading.Thread(target=send_audio)
        new_thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Audio Transmission")
    root.geometry("400x600")

    start_button = tk.Button(root, text="Start", command=start_button_clicked, bg="green", fg="white")

    stop_button = tk.Button(root, text="Stop", command=stop_button_clicked, bg="red", fg="white")

    mute_button = tk.Button(root, text="Mute", command=mute_button_clicked, bg="yellow", fg="black")

    start_button.pack(side='top', expand=1, anchor='c', padx=10, pady=10)
    stop_button.pack(side='top', expand=1, anchor='c', padx=10, pady=1)
    mute_button.pack(side='top', expand=1, anchor='c', padx=10, pady=1)

    root.mainloop()
