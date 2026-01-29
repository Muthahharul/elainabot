from flask import Flask, request, jsonify, render_template, send_from_directory
from groq import Groq
from config import Config

import re
import math
import random

from sympy import symbols, diff, integrate
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)

app = Flask(__name__)
app.config.from_object(Config)

client = Groq(api_key=app.config["GROQ_API_KEY"])

x = symbols("x")
transformations = standard_transformations + (
    implicit_multiplication_application,
)

def small_talk(text):
    t = text.lower()

    small_talk_keywords = [
        "kamu siapa", "lagi apa", "ngobrol", "temenin",
        "capek", "ngantuk", "menurut kamu",
        "haha", "wkwk", "bosan"
    ]

    developer_keywords = [
        "siapa pembuat", "siapa developer", "siapa pengembang",
        "yang buat kamu", "yang bikin kamu",
        "developer website ini", "pembuat website ini"
    ]

    if any(k in t for k in developer_keywords):
        return random.choice([
            "Aku dikembangkan oleh developer yang lagi serius ngulik AI dan web nih, yaitu Abid🔥",
            "Website ini dibuat oleh developer yang suka eksperimen teknologi dan desain.",
            "Aku lahir dari tangan developer yang lagi belajar dan berkembang 💻✨"
        ])

    # small talk biasa
    if any(k in t for k in small_talk_keywords):
        return random.choice([
            "Aku di sini kok 😄 Mau ngobrol atau nanya hal berat?",
            "Santai, aku online. Gas tanya.",
            "Hehe, aku siap nemenin."
        ])

    return None


def calculate_math(text):
    try:
        expr = text.replace(" ", "")
        if re.fullmatch(r"[0-9+\-*/().]+", expr):
            return f"Hasilnya: {eval(expr, {'__builtins__': {}}, math.__dict__)}"
    except:
        pass
    return None


def derivative(text):
    t = text.lower().replace("^", "**")
    if not any(k in t for k in ["turunan", "d/dx", "dy/dx"]):
        return None

    match = re.search(r"(turunan|d/dx|dy/dx)\s*(.*)", t)
    if not match:
        return None

    expr = parse_expr(match.group(2), transformations=transformations)
    return f"Turunan dari {match.group(2)} adalah {diff(expr, x)}"


def integral(text):
    t = text.lower().replace("^", "**")
    if "integral" not in t and "∫" not in t:
        return None

    match = re.search(r"(integral|∫)\s*(.*)", t)
    if not match:
        return None

    expr = parse_expr(match.group(2), transformations=transformations)
    return f"Integral dari {match.group(2)} adalah {integrate(expr, x)} + C"


def dc_circuit(text):
    t = text.lower().replace(" ", "")
    if "v=" not in t or "r=" not in t:
        return None

    try:
        v = float(re.search(r"v=([\d.]+)", t).group(1))
        r_list = list(map(float, re.search(r"r=([\d.,]+)", t).group(1).split(",")))
    except:
        return None

    if "seri" in t:
        rt = sum(r_list)
        return f"I = {v/rt:.2f} A (R total = {rt} Ω)"

    if "paralel" in t:
        rt = 1 / sum(1/r for r in r_list)
        return f"I total = {v/rt:.2f} A (R total = {rt:.2f} Ω)"

    return None

@app.route('/google3f36c0c2a27a01e9.html')
def google_verify():
    return send_from_directory('.', 'google3f36c0c2a27a01e9.html')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Pesannya kosong 😅"})

    greetings = ["halo", "hai", "hi", "hello", "p", "tes"]
    if user_message.lower() in greetings:
        return jsonify({
            "reply": random.choice([
                "Hai 👋 mau ngobrol atau nanya?",
                "Yo! Ada yang bisa dibantu?",
                "Halo 😄"
            ])
        })

    for handler in [small_talk, derivative, integral, calculate_math, dc_circuit]:
        result = handler(user_message)
        if result:
            return jsonify({"reply": result})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Kamu adalah AI asisten yang santai, nyambung, dan realistis. "
                        "Bisa diajak ngobrol seperti teman. "
                        "Jawab ringan jika santai, teknis jika serius."
                    )
                },
                {"role": "user", "content": user_message}
            ],
            temperature=0.6
        )

        reply = response.choices[0].message.content

    except Exception as e:
        print("Groq error:", e)
        reply = "Aku lagi error sebentar 😅 coba ulangi ya."

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
