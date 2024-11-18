from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image
from ..utils.validate_user import verify_firebase_token

router = APIRouter(
  #prefix="/load-image",
  #ags=["Load Image"]
)

@router.post("/image")
async def process_image(file: UploadFile = File(...), user: dict = Depends(verify_firebase_token)):

    content_file_list = ['image/png', 'image/jpeg']   
    content_file = file.content_type                  
    print(f'content fil: {content_file} user data: {user}')
    if(content_file_list.index(file.content_type) >= 0):
        image = Image.open(file.file)
        processed_image = image.convert("L")

        img_bytes = BytesIO()
        processed_image.save(img_bytes, format="JPEG")
        img_bytes.seek(0)

        # Retornar la imagen procesada
        return StreamingResponse(img_bytes, media_type=content_file)
    else:
        raise HTTPException(status_code=400, detail=f"Formato de archivo invalido")
    
