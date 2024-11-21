import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter


# 1. PDF 페이지를 가로로 반으로 나누기
def split_pdf_half(input_pdf_path, output_pdf_prefix):
    pdf_reader = PdfReader(input_pdf_path)
    pdf_writer_top = PdfWriter()
    pdf_writer_bottom = PdfWriter()

    for page_num, page in enumerate(pdf_reader.pages):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        # 상단 부분
        page_top = page
        page_top.mediabox.upper_left = (0, height / 2)
        page_top.mediabox.lower_right = (width, height)

        # 하단 부분
        page_bottom = page
        page_bottom.mediabox.upper_left = (0, 0)
        page_bottom.mediabox.lower_right = (width, height / 2)

        pdf_writer_top.add_page(page_top)
        pdf_writer_bottom.add_page(page_bottom)

    # 가로 반씩 자른 PDF 저장
    with open(f"{output_pdf_prefix}_top.pdf", "wb") as f_top:
        pdf_writer_top.write(f_top)
    with open(f"{output_pdf_prefix}_bottom.pdf", "wb") as f_bottom:
        pdf_writer_bottom.write(f_bottom)


# 2. '⑤' 기준으로 텍스트를 확인하고, 잘라 PNG로 저장
def extract_images_by_text(input_pdf_path, output_image_prefix):
    pdf_document = fitz.open(input_pdf_path)

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        blocks = page.get_text("blocks")  # 텍스트 블록 읽기

        # '⑤'를 기준으로 블록 찾기
        for block in blocks:
            if '⑤' in block[4]:  # 블록 텍스트 확인
                x0, y0, x1, y1 = block[:4]  # 블록의 좌표
                clip_rect = fitz.Rect(0, 0, x1, y0)  # '⑤' 위쪽을 자르기
                pix = page.get_pixmap(clip=clip_rect)
                pix.save(f"{output_image_prefix}_page{page_num + 1}.png")
                break


# 실행
input_pdf = "physics_exam.pdf"  # 입력 파일명
output_pdf_prefix = "physics_split"  # 출력 PDF 파일명
output_image_prefix = "physics_question"  # 출력 PNG 파일명

# 1단계: PDF를 상단과 하단으로 분리 (PDF 형식 유지)
split_pdf_half(input_pdf, output_pdf_prefix)

# 2단계: 상단 PDF에서 '⑤' 기준으로 자르고 PNG 저장
extract_images_by_text(f"{output_pdf_prefix}_top.pdf", output_image_prefix)
