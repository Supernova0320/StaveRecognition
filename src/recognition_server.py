import uvicorn

from pydantic import BaseModel
from fastapi import FastAPI
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(r'F:/OCR/GOT-OCR2.0/GOT-OCR-2.0-master/ckpts/GOT-OCR2_0',
                                          trust_remote_code=True)  # 允许加载自定义模型
model = AutoModel.from_pretrained(r'F:/OCR/GOT-OCR2.0/GOT-OCR-2.0-master/ckpts/GOT-OCR2_0',
                                  trust_remote_code=True,
                                  low_cpu_mem_usage=True,
                                  device_map='cuda', use_safetensors=True, pad_token_id=tokenizer.eos_token_id)
model = model.eval().cuda()

# 服务端
app = FastAPI()


class OcrRequest(BaseModel):
    image_path: str
    ocr_type: str = 'ocr'
    ocr_box: str = None
    ocr_color: str = None
    render: bool = False
    save_render_file: str = None


@app.post('/ocr')
async def ocr(request: OcrRequest):
    image_path = request.image_path  # 获取路径
    ocr_type = request.ocr_type
    ocr_box = request.ocr_box
    ocr_color = request.ocr_color
    render = request.render
    save_render_file = request.save_render_file

    res = model.chat(tokenizer, image_path, ocr_type=ocr_type, ocr_box=ocr_box,
                     ocr_color=ocr_color, render=render, save_render_file=save_render_file)
    return res


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8848)
# input your test image
# image_file = 'F:/OCR/GOT-OCR2.0/GOT-OCR-2.0-master/test/stave_test.png'

# plain texts OCR
# res = model.chat(tokenizer, image_file, ocr_type='ocr')

# format texts OCR:
# res = model.chat(tokenizer, image_file, ocr_type='format')

# fine-grained OCR:
# res = model.chat(tokenizer, image_file, ocr_type='ocr', ocr_box='')
# res = model.chat(tokenizer, image_file, ocr_type='format', ocr_box='')
# res = model.chat(tokenizer, image_file, ocr_type='ocr', ocr_color='')
# res = model.chat(tokenizer, image_file, ocr_type='format', ocr_color='')

# multi-crop OCR:
# res = model.chat_crop(tokenizer, image_file, ocr_type='ocr')
# res = model.chat_crop(tokenizer, image_file, ocr_type='format')

# render the formatted OCR results:
# res = model.chat(tokenizer, image_file, ocr_type='format', render=True, save_render_file = './demo.html')

# print(res)
