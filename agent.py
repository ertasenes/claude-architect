import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()


def hesapla(islem, a, b):
    """İki sayı üzerinde dört işlemden birini yapar."""
    if islem == "topla":
        return a + b
    elif islem == "cikar":
        return a - b
    elif islem == "carp":
        return a * b
    elif islem == "bol":
        return a / b
    else:
        return "Bilinmeyen işlem"


hesap_araci = {
    "name": "hesapla",
    "description": "İki sayı üzerinde dört işlem (toplama, çıkarma, çarpma, bölme) yapar. Kesin aritmetik gerektiğinde kullan.",
    "input_schema": {
        "type": "object",
        "properties": {
            "islem": {
                "type": "string",
                "enum": ["topla", "cikar", "carp", "bol"],
                "description": "Yapılacak işlem"
            },
            "a": {
                "type": "number",
                "description": "Birinci sayı"
            },
            "b": {
                "type": "number",
                "description": "İkinci sayı"
            }
        },
        "required": ["islem", "a", "b"]
    }
}

soru = "Şunu tam olarak hesapla: 4837 çarpı 2916 kaç eder?"

mesajlar = [
    {"role": "user", "content": soru}
]

while True:
    cevap = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        tools=[hesap_araci],
        messages=mesajlar
    )

    if cevap.stop_reason == "tool_use":
        mesajlar.append({"role": "assistant", "content": cevap.content})

        for parca in cevap.content:
            if parca.type == "tool_use":
                print(f"[Claude aracı çağırdı: {parca.name}, girdiler: {parca.input}]")

                arac_sonucu = hesapla(
                    parca.input["islem"],
                    parca.input["a"],
                    parca.input["b"]
                )
                print(f"[Aracın sonucu: {arac_sonucu}]")

                mesajlar.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": parca.id,
                            "content": str(arac_sonucu)
                        }
                    ]
                })
    else:
        print("\nClaude'un nihai cevabı:")
        print(cevap.content[0].text)
        break