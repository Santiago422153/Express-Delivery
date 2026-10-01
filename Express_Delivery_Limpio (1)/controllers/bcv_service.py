import json
import urllib.request
import urllib.error

class BCVService:
    @staticmethod
    def obtener_tasa_dolar():
        """
        Obtiene la tasa oficial del BCV a través de DolarApi Venezuela (ve.dolarapi.com).
        Busca en la lista el objeto con "fuente": "oficial" y retorna el valor "promedio".
        """
        url = "https://ve.dolarapi.com/v1/dolares"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    
                    # La API retorna una lista de objetos:
                    # [
                    #   {"fuente": "oficial", "nombre": "Oficial", "promedio": ...},
                    #   {"fuente": "paralelo", "nombre": "Paralelo", "promedio": ...}
                    # ]
                    if isinstance(data, list):
                        for cotizacion in data:
                            if cotizacion.get("fuente") == "oficial":
                                return float(cotizacion.get("promedio", 0.0))
                                
        except (urllib.error.URLError, json.JSONDecodeError, KeyError, ValueError, TypeError):
            pass
        
        # Valor de respaldo predeterminado en caso de falla de red o formato
        return 45.50