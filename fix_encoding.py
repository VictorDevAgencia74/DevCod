import os

def remove_bom(file_path):
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        
        if content.startswith(b'\xef\xbb\xbf'):
            content = content[3:]
            with open(file_path, 'wb') as f:
                f.write(content)
            print(f"BOM removido de: {file_path}")
        else:
            print(f"Sem BOM em: {file_path}")
            
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")

if __name__ == "__main__":
    files_to_check = [
        "app.py",
        "src/controllers/home_controller.py",
        "templates/index.html"
    ]
    
    for file in files_to_check:
        remove_bom(file)
