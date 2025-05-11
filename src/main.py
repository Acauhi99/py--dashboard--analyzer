import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.services.data_processing import load_data, process_data
from src.services.dashboard import create_dashboard


def main():
    data_path = os.path.join(project_root, "data", "custo_usinas_termicas.csv")
    
    print("Carregando dados...")
    raw_data = load_data(data_path)
    
    print("Processando dados...")
    processed_data = process_data(raw_data)
    
    print("Inicializando dashboard...")
    app = create_dashboard(processed_data)
    
    app.run(debug=True, port=8080)
    print("http://localhost:8080/")


if __name__ == "__main__":
    main()