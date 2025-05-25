import os
import requests
from dotenv import load_dotenv
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from openai import OpenAI
from pathlib import Path

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generar_contenido(prompt):
    prompt = prompt.strip()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": (
                "Eres un generador profesional de presentaciones de PowerPoint. "
                "Cada diapositiva debe tener:\n"
                "- Un título claro y breve.\n"
                "- Un párrafo explicativo de 2 a 4 líneas.\n"
                "- Una imagen relevante entre tags [image: descripción]."
            )},
            {"role": "user", "content": prompt}
        ]
    )
    texto = response.choices[0].message.content
    slides = []

    for bloque in texto.split("\n\n"):
        if ":" in bloque:
            partes = bloque.split("\n")
            slide = {"titulo": "", "contenido": "", "imagen": ""}
            for linea in partes:
                if linea.lower().startswith("título:"):
                    slide["titulo"] = linea.split(":", 1)[1].strip()
                elif "[image:" in linea:
                    slide["imagen"] = linea.split("[image:", 1)[1].split("]")[0].strip()
                else:
                    slide["contenido"] += linea.replace("Párrafo:", "").strip() + " "
            slides.append(slide)

    return slides

def generar_imagen(prompt_img, filename):
    try:
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_img,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        url = image_response.data[0].url
        img_data = requests.get(url).content
        with open(filename, 'wb') as f:
            f.write(img_data)
        return True
    except Exception as e:
        print("❌ Error al generar imagen:", e)
        return False

def generar_pptx(slides, nombre):
    folder = Path("media/presentaciones")
    folder.mkdir(parents=True, exist_ok=True)
    ruta = folder / f"{nombre}.pptx"

    prs = Presentation()
    blank_slide_layout = prs.slide_layouts[6]

    # Diapositiva de título
    title_slide = prs.slides.add_slide(prs.slide_layouts[0])
    title_slide.shapes.title.text = nombre.replace("_", " ").capitalize()
    subtitle = title_slide.placeholders[1]
    subtitle.text = "Presentación generada automáticamente"
    subtitle.text_frame.paragraphs[0].font.size = Pt(20)

    for i, slide_data in enumerate(slides):
        slide = prs.slides.add_slide(blank_slide_layout)

        # Fondo claro
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(245, 245, 245)

        # Título
        left = Inches(0.5)
        top = Inches(0.4)
        width = Inches(8)
        height = Inches(1)
        title_box = slide.shapes.add_textbox(left, top, width, height)
        tf = title_box.text_frame
        p = tf.add_paragraph()
        p.text = slide_data["titulo"]
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = RGBColor(44, 62, 80)

        # Contenido
        top = Inches(1.5)
        height = Inches(2.5)
        content_box = slide.shapes.add_textbox(left, top, width, height)
        tf = content_box.text_frame
        p = tf.add_paragraph()
        p.text = slide_data["contenido"]
        p.font.size = Pt(20)
        p.font.color.rgb = RGBColor(60, 60, 60)

        # Imagen
        if slide_data["imagen"]:
            img_path = folder / f"{nombre}_img{i+1}.png"
            if generar_imagen(slide_data["imagen"], img_path):
                img_left = Inches(5.3)
                img_top = Inches(2.5)
                img_height = Inches(3.5)
                slide.shapes.add_picture(str(img_path), img_left, img_top, height=img_height)

        # Nota para transición
        slide.notes_slide.notes_text_frame.text = "Transición sugerida: fundido suave."

    prs.save(ruta)
    return str(ruta)
