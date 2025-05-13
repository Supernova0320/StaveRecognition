from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
from transformers import AutoModel, AutoTokenizer
import uvicorn
import shutil
import uuid

# 模型加载
tokenizer = AutoTokenizer.from_pretrained(
    pretrained_model_name_or_path=r'/home/bygpu/Desktop/ocr_server/GOT-OCR2.0/GOT-OCR-2.0-master/ckpts/GOT-OCR2_0/',
    trust_remote_code=True
)
model = AutoModel.from_pretrained(
    pretrained_model_name_or_path=r'/home/bygpu/Desktop/ocr_server/GOT-OCR2.0/GOT-OCR-2.0-master/ckpts/GOT-OCR2_0/',
    trust_remote_code=True,
    low_cpu_mem_usage=True,
    device_map='cuda',
    use_safetensors=True,
    pad_token_id=tokenizer.eos_token_id
).eval().cuda()

app = FastAPI()


@app.post("/ocr")
async def ocr(
        file: UploadFile = File(...),
        ocr_type: str = Form('format'),
        ocr_box: str = Form(''),
        ocr_color: str = Form(''),
        render: bool = Form(False),
):
    # 保存上传的文件到临时路径
    temp_filename = f"temp_{uuid.uuid4().hex}.png"
    temp_path = os.path.join("temp", temp_filename)
    os.makedirs("temp", exist_ok=True)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # OCR 识别
    res = model.chat(tokenizer, temp_path, ocr_type=ocr_type, ocr_box=ocr_box,
                     ocr_color=ocr_color, render=render, save_render_file=temp_path)

    # 清理临时文件
    os.remove(temp_path)

    return JSONResponse(content=res)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
